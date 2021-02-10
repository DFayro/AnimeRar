from flask import Blueprint, render_template

blueprint = Blueprint("index", __name__)


@blueprint.route("/")
def index():
	nav_elements = [("Home", "#"), ("About", "#")]
	return render_template("base.html", nav_elements=nav_elements)
