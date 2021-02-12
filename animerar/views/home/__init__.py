from animerar.db.db_short import *
from animerar.models import Anime
from flask import Blueprint, render_template, url_for
from animerar.core import NavBar

blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def index():
	animes = Anime.query.all()

	for anime in animes:
		print(f"Name: {anime.name}, VA's: {[a.name for a in anime.voice_actors]}")

	navbar = NavBar.default_bar(active_page="Home")
	return render_template("home.html", navbar=navbar)
