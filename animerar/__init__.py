from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

import animerar.db

SHARED_TEMPLATE_FOLDER = "views/sh_templates"
SHARED_STATIC_FOLDER = "views/sh_static"
DATABASE_URI = "sqlite:///./animerar.db"


def page_not_found(e):
	return render_template("404.html"), 404


def general_error(e):
	return render_template("bad_request.html")


def build_app():
	app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)
	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
	app.config['SECRET_KEY'] = "DonkeysWriteBadCode"
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# ###############################################################################################################
	# Generally, inline import statements are to be avoided. However in this instance it is recommended to only load
	# the views and models after the database has been instantiated. Database instantiation only happens on app
	# creation, therefore we need to import them later to avoid circular dependencies. The same applies for flask
	# extensions like flask-sqlalchemy, flask-login and flask-wtforms.
	# ###############################################################################################################

	# Init database and flask extensions
	animerar.db.init_db(app)
	from animerar.core import auth_handler
	auth_handler.init(app)

	app.register_error_handler(404, page_not_found)
	app.register_error_handler(HTTPException, general_error)

	# Collect and attach Blueprints
	from animerar.views import home, auth, anime

	app.register_blueprint(home.blueprint)
	app.register_blueprint(auth.blueprint, url_prefix="/auth")
	app.register_blueprint(anime.blueprint, url_prefix="/anime")

	return app
