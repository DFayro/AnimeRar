from flask import Blueprint, render_template

from animerar.core import NavBar

blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def index():
	navbar = NavBar.default_bar(active_page="Home")
	return render_template("home.html", navbar=navbar)
