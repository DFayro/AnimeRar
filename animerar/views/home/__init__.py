from flask import Blueprint, render_template
from flask_login import current_user, login_required

from animerar.core import NavBar
from animerar.models import CarouselImage
from animerar.models.anime import Anime

blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def index():
	recently_added_anime = Anime.query.order_by(Anime.title.desc()).limit(3).all()

	carousel = CarouselImage.query.all()

	navbar = NavBar.default_bar(active_page="Home")
	return render_template("home.html", navbar=navbar, recently_added_anime=recently_added_anime, caroucel=carousel)


@blueprint.route("/profile")
@login_required
def profile():
	navbar = NavBar.default_bar()

	collected_anime = current_user.collected_anime[:5]
	anime_collected_count = len(current_user.collected_anime)

	anime_comment_count = len(current_user.anime_comments)

	return render_template(
		"profile.html",
		navbar=navbar,
		collected_anime=collected_anime,
		anime_collected_count=anime_collected_count,
		anime_comment_count=anime_comment_count
	)


@blueprint.route("/profile/collected")
def profile_collected_anime():
	navbar = NavBar.default_bar()

	collected_anime = current_user.collected_anime

	return render_template("profile_collected.html", navbar=navbar, collected_anime=collected_anime)
