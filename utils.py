import re
import secrets
import string
import datetime
from urllib.parse import urlparse
from models import (
    db,
    URL,
    Stats
)


def now() -> datetime.datetime:
    """what time is now"""
    return datetime.datetime.now()


def to_iso8601(dt: str) -> datetime.datetime:
    """Convert string to iso-8601"""
    return (datetime.datetime
            .strptime(str(dt), "%Y-%m-%d %H:%M:%S.%f")
            .isoformat())


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


def bump_stats(url_id: int) -> tuple:
    """Updates Stat records"""
    q = (Stats
         .update({
             Stats.usage_count: Stats.usage_count+1,
             Stats.last_usage: now()
         })
         .where(Stats.url_id==url_id)
         .execute())

    return q


def get_stats(code: str) -> tuple:
    """Returns Stats data"""
    q = (Stats
         .select(
             Stats.created_at,
             Stats.last_usage,
             Stats.usage_count
         )
         .join_from(Stats, URL)
         .where(URL.code==code)
         .execute())

    return q.cursor.fetchone()


def gen_code() -> str:
    """Generates a code"""
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    _, exists = code_exists(code)
    if exists:
        return gen_code()
    else:
        return code


def code_exists(code) -> tuple:
    """Checks if a code exists in DB"""
    q = (URL
         .select(URL.id, URL.code)
         .where(URL.code==code)
         .limit(1))
    return q, q.count() > 0


def is_valid_url(url: str) -> bool:
    """is this URL well formatted?
       (aka: does it looks like an url?)"""
    result = urlparse(url)
    return all([result.scheme, result.netloc, result.path])


def is_valid_code(code: str) -> bool:
    """check if a code complies with <=6 alphanumeric chr"""
    return (
        len(re.sub(r'[a-zA-Z0-9]', '', code)) == 0 and
        len(code) == 6
    )
