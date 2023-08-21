from app import create_app, db
from app.models.models import Comparison, Image

app = create_app()

with app.app_context():
    db.create_all()