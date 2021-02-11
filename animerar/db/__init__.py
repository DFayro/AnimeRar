from flask_sqlalchemy import SQLAlchemy

db_inst: SQLAlchemy = None


def init_db(flask_app):
	global db_inst

	db_inst = SQLAlchemy(flask_app)

	# Ensure schema is declared by importing each module containing them
	from animerar import Models

	# Actually create the schema
	db_inst.create_all()

	print("DB Initialized", db_inst)
