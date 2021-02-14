import animerar


def main():
	app = animerar.build_app()

	app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
	main()
