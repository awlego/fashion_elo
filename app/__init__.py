# app/__init__.py

from flask import Flask

from app.models import db

def create_app():
    app = Flask(__name__)
    
    # any other initializations can go here, like configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fashion_elo.db'
    
    from app.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)
    
    return app