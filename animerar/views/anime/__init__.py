from flask import Blueprint, abort, render_template
from flask_login import login_required

from animerar.core import NavBar
from animerar.models.anime import Anime

blueprint = Blueprint("anime", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
@login_required
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
