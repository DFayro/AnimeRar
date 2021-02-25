import argparse
import json

import animerar


def main(test_data=False):
	app = animerar.build_app()

	if test_data:
		ensure_test_data()

	app.run(debug=True, host="0.0.0.0")


def ensure_test_data():
	from animerar.db import db_inst as db
	from animerar.models import User
	from animerar.models.anime import Anime

	db.drop_all()
	db.create_all()

	print("Building test database")

	with open("tests/data.json", encoding='UTF-8') as csv_file:
		data = json.loads(csv_file.read())

		# Users
		for user in data['users']:
			new_user = User(
				email=user["email"],
				first_name=user["first_name"],
				last_name=user["last_name"],
				display_name=user["display_name"],
				password=User.secure_password(user["password"])
			)

			db.session.add(new_user)

		# Anime
		cover_folder_path = "tests/cover_arts/"
		for anime in data["anime"]:
			with open(cover_folder_path + anime["cover_art"], 'rb') as image:
				cover_art_data = image.read()

			new_anime = Anime(
				title=anime["title"],
				jp_title=anime["jp_title"],
				en_title=anime["en_title"],
				synopsis=anime["synopsis"],
				episodes=anime["episodes"],
				premiered=anime["premiered"],
				cover_art=cover_art_data
			)

			db.session.add(new_anime)

		db.session.commit()


if __name__ == '__main__':
	parser = argparse.ArgumentParser("Run AnimeRar test server")
	parser.add_argument(
		'--test-data',
		action='store_true',
		help="Run the server with only test data. WARNING, this drops all existing data and rebuilds "
			 "the database with just the test data.")

	args = parser.parse_args()

	main(args.test_data)
