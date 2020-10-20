from time import time
from spider.util.orm_util import db


class Image(db.Model):

    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    class_name = db.Column(db.String(40))
    url = db.Column(db.String(512))
    hash_code = db.Column(db.String(40), index=True)
    create_time = db.Column(db.Integer, index=True, default=time)
    index = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('class_name', 'hash_code', name='class_hash_code_unix'),
    )

