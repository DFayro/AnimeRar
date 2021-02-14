from flask import Blueprint, render_template, request

from animerar.core import NavBar

blueprint = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/", methods=['GET', 'POST'])
def index():
	navbar = NavBar.default_bar()

	if request.method == "POST":

		print(request)
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
		repeat_password = request.form.get('repeat_password')

		if not email:
			errors['email_error'] = "Not a valid address"
			valid = False

		if not display_name:
			errors['display_name_error'] = "Not a valid address"
			valid = False

		if not first_name:
			errors['first_name_error'] = "Not a valid address"
			valid = False

		if not last_name:
			errors['last_name_error'] = "Not a valid address"
			valid = False

		if not password:
			errors['password_error'] = "Not a valid address"
			valid = False

		if not repeat_password:
			errors['repeat_password_error'] = "Not a valid address"
			valid = False

		if valid:
			pass

		return render_template("register.html", navbar=navbar, posted=True, **errors)

	return render_template("register.html", navbar=navbar)
