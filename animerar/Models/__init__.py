from flask_login import UserMixin
from werkzeug import security

from animerar.db.db_short import *

collected_anime = Table(
	'collected_anime',
	metadata,
	Column('user.id', Integer, ForeignKey('user.id')),
	Column('anime.id', Integer, ForeignKey('anime.id'))
)


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

	collected_anime = relationship('Anime', secondary=collected_anime)

	password = Column(String(64))

	@classmethod
	def user_exists(cls, email):
		return bool(cls.get(email))

	@classmethod
	def get(cls, email):
		return cls.query.filter_by(email=email).first()

	@staticmethod
	def secure_password(password: str):
		return security.generate_password_hash(password)

	def check_password(self, password: str):
		return security.check_password_hash(self.password, password)
