from flask import Blueprint, render_template, url_for

blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def index():
	nav_elements = [("Home", "#"), ("Anime", "#"), ("Utattemita", "#"), ("404", "http://localhost:5000/404")]
	return render_template("home.html", nav_elements=nav_elements)