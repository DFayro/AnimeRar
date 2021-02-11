from flask import Flask

from animerar.views import home

SHARED_TEMPLATE_FOLDER = "views/sh_templates"
SHARED_STATIC_FOLDER = "views/sh_static"


def init():
	app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)

	# Blueprints
	app.register_blueprint(home.blueprint)

	return app
