import argparse
import csv

import animerar


def main(test_data=False):
	app = animerar.build_app()

	if test_data:
		ensure_test_data()

	app.run(debug=True, host="0.0.0.0")


def ensure_test_data():
	from animerar.db import db_inst as db
	from animerar.models import anime
	db.drop_all()
	db.create_all()

	print("Building test database")

	with open("tests/test_data.csv", newline='', encoding='UTF-8') as csv_file:
		reader = csv.DictReader(csv_file)

		for row in reader:

			with open(f"tests/cover_arts/{row['cover_art_filename']}", 'rb') as image:
				img_data = image.read()

			new_anime = anime.Anime(
				title=row['title'],
				jp_title=row['jp_title'],
				en_title=row['en_title'],
				synopsis=row['synopsis'],
				premiered=row['premiered'],
				cover_art=img_data
			)

			db.session.add(new_anime)

		db.session.commit()


if __name__ == '__main__':
	parser = argparse.ArgumentParser("Run AnimeRar test server")
	parser.add_argument(
		'--test-data',
		action='store_true',
		help="Run the server with only test data. WARNING, this drops all existing data and rebuils "
			 "the database with just the test data.")

	args = parser.parse_args()

	main(args.test_data)
