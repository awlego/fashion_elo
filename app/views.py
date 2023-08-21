# app/views.py

from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes  # this will ensure routes are imported after the blueprint is defined
