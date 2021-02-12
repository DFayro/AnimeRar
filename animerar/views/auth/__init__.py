from flask import Blueprint, render_template, url_for, current_app, Flask, request

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


	nav_elements = [("Home", "#"), ("Anime", "#"), ("Utattemita", "#"), ("404", "http://localhost:5000/404")]
	return render_template("login.html", nav_elements=nav_elements)
