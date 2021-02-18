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

	comments = relationship('AnimePageComment')

	@classmethod
	def get(cls, *_, **kwargs):
		return cls.query.filter_by(**kwargs).first()

	@classmethod
	def get_all(cls, *_, **kwargs):
		return cls.query.filter_by(**kwargs).all()


class AnimePageComment(Model):

	__tablename__ = "anime_page_comment"

	id = Column(Integer, primary_key=True, autoincrement=True)
	anime = Column(Integer, ForeignKey('anime.id'))
	comment_text = Column(String(100))
	comment_author = Column(Integer, ForeignKey('user.id'))


class VoiceActor(Model):
	__tablename__ = "voice_actor"

	id = Column(Integer, primary_key=True, autoincrement=True)
	anime_id = Column(Integer, ForeignKey('anime.id'))

	name = Column(String(100))
