import datetime
from peewee import *
from os import environ as env

if env.get('FLASK_DEBUG', 0):
    db = SqliteDatabase(':memory:')
else:
    db = PostgresqlDatabase(
        env.get('POSTGRES_DB', 'postgres'),
        user=env.get('POSTGRES_USER', 'postgres'),
        password=env.get('POSTGRES_PASSWORD', 'postgres'),
        host=env.get('DB_HOST', 'localhost'),
    )


class BaseModel(Model):
    class Meta:
        database = db


class URL(BaseModel):
    url = CharField(max_length=35)
    code = CharField(max_length=6)

    class Meta:
        table_name = 'urls'

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'url': str(self.url).strip(),
            'code': str(self.code).strip(),
        }

        return data

    def __repr__(self):
        code = self.code
        url = self.url
        return f"{code} ({url})"


class Stats(BaseModel):
    url = ForeignKeyField(URL, backref='url')
    created_at = DateTimeField(default=datetime.datetime.now)
    last_usage = DateTimeField(null=True)
    usage_count = IntegerField()

    class Meta:
        table_name = 'stats'

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'url': str(self.url).strip(),
            'created_at': str(self.created_at).strip(),
            'last_usage': str(self.last_usage).strip(),
            'usage_count': str(self.usage_count).strip(),
        }

        return data

    def __repr__(self):
        url = self.url
        count = self.usage_count
        return f"{url} ({count})"
