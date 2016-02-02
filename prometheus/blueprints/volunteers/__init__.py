import pytz
from datetime import datetime
from flask import Blueprint, abort, g, current_app
from flask.ext.login import login_required, current_user, current_app
from prometheus.models.auth import User, Role

volunteer = Blueprint('volunteer', __name__)

# all auth routes require user authentication
@volunteer.before_request
@login_required
def before_request():
    g.now = datetime.now(pytz.timezone('Europe/Athens'))
    g.lat = float(current_app.config['MAP_LAT_CENTER'])
    g.lon = float(current_app.config['MAP_LON_CENTER'])
    # If current_user.roles not contains Role.volunteer, redirect to 401
    role_volunteer = Role.query.filter_by(name='volunteer').first()
    if role_volunteer not in current_user.roles:
        # TODO: Redirect to Unauthorized Custom Page
        return abort(401)
    else:
        pass

from . import views
