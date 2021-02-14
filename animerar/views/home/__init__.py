from flask import Blueprint, render_template

from animerar.core import NavBar
from animerar.models import Anime

blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def index():
	animes = Anime.query.all()

	for anime in animes:
		print(f"Name: {anime.name}, VA's: {[a.name for a in anime.voice_actors]}")

	navbar = NavBar.default_bar(active_page="Home")
	return render_template("home.html", navbar=navbar)
