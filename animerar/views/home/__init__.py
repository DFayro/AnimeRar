from flask import Blueprint, render_template

blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def index():
	nav_elements = [("Home", "#"), ("Anime", "#"), ("Utattemita", "#")]
	return render_template("index.html", nav_elements=nav_elements)
