from flask import Blueprint, abort, render_template, request
from wtforms import SelectField, StringField, TextAreaField, validators, FileField

from animerar.core import NavBar
from animerar.core.form import InlineValidatedForm
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
	cover_art = FileField()
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
	premiered_season = SelectField('Select', choices=[
		("spring", "Spring"),
		("summer", "Summer"),
		("autumn", "Autumn"),
		("w	inter", "Winter")
	])
	premiered_month = SelectField('Select', choices=[
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
		print("Validated")
		print(request.form)

	return render_template("anime_add.html", navbar=navbar, form=form)
