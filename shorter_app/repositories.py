from shorter_app.database import db_session
from shorter_app.models import Shorter, Stats


class BaseRespository:
    @classmethod
    def commit(cls):
        db_session.commit()


class ShorterRepository(BaseRespository):
    @classmethod
    def add(cls, shorter):
        db_session.add(shorter)
        db_session.commit()

    @classmethod
    def get(cls, code):
        return Shorter.query.filter(Shorter.code == code).first()

    @classmethod
    def get_all(cls):
        return db_session.query(Shorter).all()


class StatsRepository(BaseRespository):
    @classmethod
    def add(self, stats):
        db_session.add(stats)
        db_session.commit()

    @classmethod
    def get(self, code):
        return Stats.query.filter(Stats.code == code).first()

    @classmethod
    def get_all(self):
        return db_session.query(Stats).all()
