from flask import Blueprint, redirect, render_template, request, url_for

from animerar.core import NavBar, validation
from animerar.db import db_inst as db
from animerar.models import User

blueprint = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/", methods=['GET', 'POST'])
def index():
	navbar = NavBar.default_bar()

	if request.method == "POST":

		email = request.form['email']
		password = request.form['password']

		error = "Login failed"

		if error:
			return render_template("login.html", navbar=navbar, login_error=error)

	return render_template("login.html", navbar=navbar)


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
	navbar = NavBar.default_bar()

	if request.method == "POST":
		valid = True

		errors = {}

		# Validate
		email = request.form.get('email')
		display_name = request.form.get('display_name')
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		password = request.form.get('password')
		password_repeat = request.form.get('password_repeat')

		if not email:
			errors['email_error'] = "Enter an email address"
			valid = False
		else:
			if len(email) < 6:
				errors['email_error'] = "Invalid email length"
				valid = False
			else:
				if not validation.is_email(email):
					errors['email_error'] = "Incorrect email address format"
					valid = False
				else:
					if User.user_exists(email):
						errors['email_error'] = "Email already in use"
						valid = False

		if not display_name:
			errors['display_name_error'] = "Enter a display name"
			valid = False

		if not first_name:
			errors['first_name_error'] = "Enter a first name"
			valid = False

		if not password:
			errors['password_error'] = "Enter a password"
			valid = False

		if password:
			if not password_repeat:
				errors['repeat_password_error'] = "Repeat your password"
				valid = False
			else:
				if password_repeat != password:
					errors['password_repeat_error'] = "Passwords do not match"
					valid = False

		print(request.form)

		if valid:
			new_user = User(
				email=email,
				display_name=display_name,
				first_name=first_name,
				last_name=last_name,
				password=password
			)

			db.session.add(new_user)
			db.session.commit()

			return redirect(url_for("auth.index"))

		return render_template("register.html", navbar=navbar, posted=True, **errors)

	return render_template("register.html", navbar=navbar)
