import datetime
from models import (
    db,
    URL,
    Stats
)

def now() -> datetime.datetime:
    """what time is now"""
    return datetime.datetime.now()


def create_tables() -> None:
    """Creates tables"""
    db.create_tables([URL, Stats])


def drop_tables() -> None:
    """Drops tables"""
    map(lambda m: m.drop_table(), [URL, Stats])


def insert_url(url:str, code:str) -> int:
    """Inserts a new URL"""
    q = URL.insert(url=url, code=code)
    url_id = q.execute()
    Stats.insert(url=url_id, usage_count=0).execute()

    return url_id
