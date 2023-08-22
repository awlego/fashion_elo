from datetime import datetime
from . import db

class Comparison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unselected_image_uid = db.Column(db.String, db.ForeignKey('image.uid'), nullable=False)
    selected_image_uid = db.Column(db.String, db.ForeignKey('image.uid'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Image(db.Model):
    uid = db.Column(db.String, primary_key=True)  # MD5 hash as UID
    filepath = db.Column(db.String, unique=True, nullable=False)

class EloDB(db.Model):
    uid = db.Column(db.String, primary_key=True)
    elo = db.Column(db.Integer)