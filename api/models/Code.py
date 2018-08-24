from api.core import Mixin, generate_code
from .base import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
import re


class Code(Mixin, db.Model):
    """Code Table."""

    __tablename__ = "codes"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    url = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False, unique=True)
    usage = db.Column(db.Integer, nullable=True, default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    last_usage = db.Column(db.DateTime, nullable=True, onupdate=func.now())

    def __init__(self, url=None, code=None):
        self.url = url
        self.code = code

    def __repr__(self):
        return f"<Url {self.url}>"


    @validates('url')
    def validate_url(self, key, url):
        if not url:
            raise AssertionError('Url must be present', 400)

        return url

    @validates('code')
    def validate_code(self, key, code):
        if not code:
            return generate_code()

        if len(code) != 6 or not re.match('[A-Za-z0-9]', code):
            raise AssertionError('Shortcode must have 6 Alphanumeric Characters', 422)

        if Code.query.filter(Code.code == code).first():
            raise AssertionError('Shortcode is already in use', 409)

        return code
