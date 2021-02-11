from flask import Flask, url_for, render_template

from animerar.views import home

SHARED_TEMPLATE_FOLDER = "views/sh_templates"
SHARED_STATIC_FOLDER = "views/sh_static"


def page_not_found(e):
	return render_template("404.html"), 404


def init():
	app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)

	app.register_error_handler(404, page_not_found)

	# Blueprints
	app.register_blueprint(home.blueprint)

	return app
