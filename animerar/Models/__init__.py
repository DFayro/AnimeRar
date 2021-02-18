from flask_login import UserMixin

from animerar.db.db_short import *


class User(Model, UserMixin):
	__tablename__ = "user"

	def __init__(self, *args, **kwargs):
		Model.__init__(self, *args, **kwargs)
		UserMixin.__init__(self)

	id = Column(Integer, primary_key=True, nullable=False)

	email = Column(String(28))
	display_name = Column(String(28))
	first_name = Column(String(28))
	last_name = Column(String(28))

	password = Column(String(64))

	@classmethod
	def user_exists(cls, email):
		return bool(cls.get(email))

	@classmethod
	def get(cls, email):
		return cls.query.filter_by(email=email).first()