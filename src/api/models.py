#! src/api/models.py

from src import db
import datetime

class Url(db.Model):
    __tablename__ = "url"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(256), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    last_usage = db.Column(db.DateTime, nullable=True)
    usage_count = db.Column(db.Integer, default=0, nullable=False)

    def to_json(self):
        return {
            'url': self.url,
            'code': self.code
        }

    def stats_to_json(self):
        result = {
            'created_at': self.created_at.isoformat(),
            'usage_count': self.usage_count
        }

        if self.last_usage is not None:
            result['last_usage'] = self.last_usage.isoformat()
        
        return result

    def save(self):
        db.session.add(self)
        db.session.commit()


def get_url_by_code(value):
    if already_existant_code(value) == False:
        return False

    url = Url.query.filter_by(code=value).first()
    url.last_usage = datetime.datetime.utcnow()
    url.usage_count = url.usage_count + 1
    url.save()

    return url


def get_url_stats_by_code(value):
    if already_existant_code(value) == False:
        return False

    url = Url.query.filter_by(code=value).first()
    return url


def already_existant_code(value):
    url = Url.query.filter_by(code=value).first()

    return (url is not None)
