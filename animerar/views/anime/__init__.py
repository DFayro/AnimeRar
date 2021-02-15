from flask import Blueprint, render_template
from flask_login import login_required

from animerar.core import NavBar

blueprint = Blueprint("anime", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
@login_required
def index():
	navbar = NavBar.default_bar(active_page="Anime")
	return render_template("anime.html", navbar=navbar)
