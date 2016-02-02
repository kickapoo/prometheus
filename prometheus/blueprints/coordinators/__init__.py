import pytz
from datetime import datetime
from flask import Blueprint, abort, g
from flask.ext.login import login_required, current_user, current_app
from prometheus.models.auth import User, Role
coordinator = Blueprint('coordinator', __name__)

# all auth routes require user authentication
@coordinator.before_request
@login_required
def before_request():
    g.now = datetime.now(pytz.timezone('Europe/Athens'))
    g.lat = float(current_app.config['MAP_LAT_CENTER'])
    g.lon = float(current_app.config['MAP_LON_CENTER'])
    # If current_user.roles not contains Role.coordinator, redirect to 401
    role_coordinator = Role.query.filter_by(name='coordinator').first()
    if role_coordinator not in current_user.roles:
        # TODO: Redirect to Unauthorized Custom Page
        return abort(401)
    else:
        pass

from .views import overview, teams, announcements, volunteers, spots, needs
