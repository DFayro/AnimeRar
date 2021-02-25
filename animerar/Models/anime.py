import base64

from flask import url_for

from animerar.db.db_short import *


class Anime(Model):
	__tablename__ = "anime"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(100), nullable=False)
	jp_title = Column(String(100))
	en_title = Column(String(100))
	synopsis = Column(String(500))
	premiered = Column(String(20))
	episodes = Column(Integer)

	cover_art = Column(BLOB())

	comments = relationship('AnimePageComment')

	@classmethod
	def get(cls, *_, **kwargs):
		return cls.query.filter_by(**kwargs).first()

	@classmethod
	def get_all(cls, *_, **kwargs):
		return cls.query.filter_by(**kwargs).all()

	def cover_art_src(self):
		if self.cover_art:
			return "data:;base64," + base64.b64encode(self.cover_art).decode('ascii')
		else:
			return url_for('anime.static', filename='img/default_cover_art.jpg')


class AnimePageComment(Model):
	__tablename__ = "anime_page_comment"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	id = Column(Integer, primary_key=True, autoincrement=True)
	anime_id = Column(Integer, ForeignKey('anime.id'))
	author_id = Column(Integer, ForeignKey('user.id'))
	text = Column(String(100))
	placed_on = Column(DateTime)
