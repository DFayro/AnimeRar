from flask import Blueprint, render_template, url_for, current_app, Flask, request

from animerar.core import NavBar

blueprint = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/", methods=['GET', 'POST'])
def index():
	try:
		if request.method == "POST":
			print(request)
			# email = request.form['email']
			# password = request.form['password']
			print(request.form)
		# print(f"Login attempted with: {email}, {password}")
	except BaseException as e:
		print(e)

	navbar = NavBar.default_bar()
	return render_template("login.html", navbar=navbar)
