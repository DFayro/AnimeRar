from flask import Flask, render_template
from werkzeug.exceptions import BadRequest

import animerar.db
from animerar.core import auth_handler

SHARED_TEMPLATE_FOLDER = "views/sh_templates"
SHARED_STATIC_FOLDER = "views/sh_static"
DATABASE_URI = "sqlite:///./test.db"


def page_not_found(e):
	return render_template("404.html"), 404


def bad_request(e):
	return render_template("bad_request.html")


def init():
	app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)
	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
	app.config['SECRET_KEY'] = "DonkeysWriteBadCode"

	animerar.db.init_db(app)
	auth_handler.init(app)

	app.register_error_handler(404, page_not_found)
	app.register_error_handler(BadRequest, bad_request)

	# Blueprints
	from animerar.views import home, auth

	app.register_blueprint(home.blueprint)
	app.register_blueprint(auth.blueprint, url_prefix="/auth")

	return app
