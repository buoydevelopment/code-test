from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from shorter_app.database import Base
from datetime import datetime


class Shorter(Base):
    __tablename__ = "shorter"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)

    def __init__(self, url, code):
        self.url = url
        self.code = code

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Stats(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    code = Column(String, ForeignKey("shorter.code"), nullable=False)
    usage_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True, dt_format='rfc822')
    last_usage = Column(DateTime, default=datetime.utcnow, nullable=True, dt_format='rfc822')

    def __init__(self, code, created_at):
        self.code = code
        self.created_at = created_at
        self.last_usage = created_at
        self.usage_count = 0
