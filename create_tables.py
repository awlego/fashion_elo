from app import app, db
from models import Comparison, Image

with app.app_context():
    db.create_all()
