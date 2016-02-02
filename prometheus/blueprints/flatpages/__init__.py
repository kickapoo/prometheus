from flask import Blueprint

flatpages = Blueprint('flatpages', __name__)

from . import views
