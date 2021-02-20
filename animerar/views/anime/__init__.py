from flask import Blueprint, abort, render_template, url_for
from markupsafe import Markup
from wtforms import FileField, IntegerField, SelectField, StringField, TextAreaField, validators

from animerar.core import NavBar
from animerar.core.form import InlineValidatedForm
from animerar.db import db_inst as db
from animerar.models.anime import Anime

blueprint = Blueprint("anime", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def index():
	navbar = NavBar.default_bar(active_page="Anime")
	return render_template("anime_front.html", navbar=navbar)


@blueprint.route("/<int:anime_id>")
def page(anime_id):
	anime = Anime.get(id=anime_id)

	if not anime:
		abort(404)

	navbar = NavBar.default_bar()
	return render_template("anime_page.html", navbar=navbar, anime=anime)


class AddAnimeForm(InlineValidatedForm):
	cover_art = FileField(
		render_kw={'accept': '.jpg,.png, application/vnd.sealedmedia.softseal.jpg,vnd.sealed.png'})
	title = StringField(
		'Title',
		render_kw={"placeholder": "Title"},
		validators=[validators.DataRequired(message="Every Anime needs a title"), validators.Length(min=4, max=32)]
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
	episodes = IntegerField('Episodes', validators=[validators.NumberRange(min=1, max=999)])
	premiered_season = SelectField('Select', choices=[
		("Spring", "Spring"),
		("Summer", "Summer"),
		("Autumn", "Autumn"),
		("Winter", "Winter")
	])
	premiered_year = SelectField('Select', choices=[
		("2013", "2013"),
		("2014", "2014"),
		("2015", "2015"),
		("2016", "2016"),
		("2017", "2017"),
		("2018", "2018"),
		("2019", "2019"),
	])


@blueprint.route("/add", methods=['GET', 'POST'])
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
			cover_art=img_data
		)

		db.session.add(new_anime)
		db.session.commit()

		alert = Markup(
			f"Added anime <b>{form.title.data}</b>. Go to <a href='{url_for('anime.page', anime_id=new_anime.id)}'>page</a>.")
		return render_template("anime_add.html", navbar=navbar, form=form, success_alert=alert)

	return render_template("anime_add.html", navbar=navbar, form=form)
