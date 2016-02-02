import pytz
from datetime import datetime
from flask import Blueprint, g, current_app

landing_page = Blueprint('/', __name__)

@landing_page.before_request
def before_request():
    g.now = datetime.now(pytz.timezone('Europe/Athens'))
    g.lat = float(current_app.config['MAP_LAT_CENTER'])
    g.lon = float(current_app.config['MAP_LON_CENTER'])

from . import views
