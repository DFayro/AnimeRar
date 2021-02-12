from flask import Flask
from flask_login import LoginManager


def _load_user(id):
	pass


def init(app: Flask):
	login_manager = LoginManager()
	login_manager.login_view = "auth.index"

	login_manager.user_loader(_load_user)

	login_manager.init_app(app)
