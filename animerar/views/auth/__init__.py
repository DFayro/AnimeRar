from flask import Blueprint, render_template, url_for, current_app, Flask, request
from animerar.core import validation
from animerar.core import NavBar

blueprint = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/", methods=['GET', 'POST'])
def index():
	navbar = NavBar.default_bar()

	if request.method == "POST":

		errors = []

		print(request)
		email = request.form['email']
		password = request.form['password']

		if not validation.is_email(email):
			errors.append("Email invalid")

		if not validation.is_password(password):
			errors.append("Password invalid format")

		print(request.form)

		if errors:
			return render_template("login.html", navbar=navbar, login_errors=errors)

	return render_template("login.html", navbar=navbar)

@blueprint.route("/register", methods=['GET', 'POST'])
def register():
	navbar = NavBar.default_bar()
	return render_template("register.html", navbar=navbar)

