from animerar.db.db_short import *


class Anime(Model):
	__tablename__ = "anime"

	id = Column(Integer, primary_key=True, autoincrement=True)

	name = Column(String(100))
	voice_actors = relationship("VoiceActor")


class VoiceActor(Model):
	__tablename__ = "voice_actor"

	id = Column(Integer, primary_key=True, autoincrement=True)
	anime_id = Column(Integer, ForeignKey('anime.id'))

	name = Column(String(100))
