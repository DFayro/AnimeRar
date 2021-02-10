from flask import Flask

from animerar.views import index


def init():
	app = Flask(__name__, template_folder="views/sh_templates", static_folder="views/sh_static")

	# Blueprints
	app.register_blueprint(index.blueprint)

	return app
