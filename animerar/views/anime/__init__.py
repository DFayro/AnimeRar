from datetime import datetime

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import FileField, IntegerField, SelectField, StringField, TextAreaField, validators

from animerar.core import NavBar
from animerar.core.form import InlineValidatedForm
from animerar.db import db_inst as db
from animerar.models.anime import Anime, AnimePageComment

blueprint = Blueprint("anime", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/", methods=['GET', 'POST'])
def index():
	navbar = NavBar.default_bar(active_page="Anime")

	current_page = request.args.get('p', 1, type=int)

	if request.args.get('search'):
		# Straight from the form into the query, what can go wrong..
		query = Anime.query.filter(Anime.title.like(f"%{request.args['search']}%"))
	else:
		query = Anime.query

	animes = query.paginate(page=current_page, per_page=10, error_out=True)

	return render_template("anime_front.html", navbar=navbar, animes=animes)


class CommentForm(FlaskForm):
	text = TextAreaField("", render_kw={"class": "form-control", "placeholder": "Add a comment!"},
						 validators=[validators.DataRequired()])


@blueprint.route("/<int:anime_id>", methods=['GET', 'POST'])
def page(anime_id):
	anime = Anime.get(id=anime_id)

	if not anime:
		abort(404)

	is_liked = False

	if current_user.is_authenticated:
		if anime in current_user.collected_anime:
			is_liked = True

	navbar = NavBar.default_bar()
	comment_form = CommentForm()

	if comment_form.validate_on_submit():
		comment = AnimePageComment(anime_id=anime.id, author_id=current_user.id, text=comment_form.text.data,
								   placed_on=datetime.now())
		anime.comments.append(comment)
		db.session.commit()

	return render_template(
		"anime_page.html",
		navbar=navbar,
		anime=anime,
		liked=is_liked,
		comment_form=comment_form)


@blueprint.route("/<int:anime_id>/collect")
@login_required
def user_collect(anime_id):
	anime = Anime.get(id=anime_id)

	if not anime:
		abort(404)

	current_user.collected_anime.append(anime)
	db.session.commit()

	return redirect(url_for('anime.page', anime_id=anime_id))


@blueprint.route("/<int:anime_id>/uncollect")
@login_required
def user_remove(anime_id):
	anime = Anime.get(id=anime_id)

	if not anime:
		abort(404)

	if anime in current_user.collected_anime:
		current_user.collected_anime.remove(anime)

	db.session.commit()

	return redirect(url_for('anime.page', anime_id=anime_id))


@blueprint.route("/<int:anime_id>/delete")
@login_required
def delete(anime_id):
	anime = Anime.get(id=anime_id)

	if not anime:
		abort(404)

	db.session.delete(anime)
	db.session.commit()

	return redirect(url_for('anime.index'))


@blueprint.route("/<int:anime_id>/edit")
@login_required
def edit(anime_id):
	anime = Anime.get(id=anime_id)

	if not anime:
		abort(404)

	return redirect(url_for('anime.index'))


class AddAnimeForm(InlineValidatedForm):
	cover_art = FileField(
		render_kw={'accept': '.jpg,.png, application/vnd.sealedmedia.softseal.jpg,vnd.sealed.png'},
		validators=[validators.DataRequired("Please select a cover picture.")]
	)
	title = StringField(
		'Title',
		render_kw={"placeholder": "Title"},
		validators=[validators.DataRequired(message="Every Anime needs a title."), validators.Length(min=4, max=32)]
	)
	jp_title = StringField(
		'Japanese Title',
		render_kw={"placeholder": "Japanese title"},
		validators=[validators.Length(max=32)]
	)
	en_title = StringField(
		'English Title',
		render_kw={"placeholder": "English title"},
		validators=[validators.Length(max=32)]
	)
	synopsis = TextAreaField(
		'Synopsis',
		render_kw={"placeholder": "Synopsis..."},
		validators=[]
	)
	episodes = IntegerField(
		'Episodes',
		validators=[validators.NumberRange(min=1, max=999)],
		render_kw={"placeholder": "Amount of episodes.."}
	)
	premiered_season = SelectField('Select', choices=[
		("Spring", "Spring"),
		("Summer", "Summer"),
		("Autumn", "Autumn"),
		("Winter", "Winter")
	])
	premiered_year = IntegerField(
		'',
		validators=[validators.NumberRange(min=1990, max=2021, message="Enter a year between 1990 and 2021")],
		render_kw={"placeholder": "Year"}
	)


@blueprint.route("/add", methods=['GET', 'POST'])
@login_required
def add():
	form = AddAnimeForm()
	navbar = NavBar.default_bar()

	if form.validate_on_submit():
		img_data: bytes = form.cover_art.data.stream.read()

		# TODO: Ensure img_data is of image type through validator

		new_anime = Anime(
			title=form.title.data,
			jp_title=form.jp_title.data,
			en_title=form.en_title.data,
			synopsis=form.synopsis.data,
			premiered=f"{form.premiered_season.data} {form.premiered_year.data}",
			episodes=form.episodes.data,
			cover_art=img_data
		)

		db.session.add(new_anime)
		db.session.commit()

		alert = Markup(
			f"Added anime <b>{form.title.data}</b>. Go to <a href='{url_for('anime.page', anime_id=new_anime.id)}'>page</a>.")
		return render_template("anime_add.html", navbar=navbar, form=form, success_alert=alert)

	return render_template("anime_add.html", navbar=navbar, form=form)
