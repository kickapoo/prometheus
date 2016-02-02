from . import api
import pytz
from datetime import datetime
from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth

from prometheus.models.auth import User
from prometheus.models.core import Spot, Need

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    g.user = User.query.filter_by(email=email).first()
    if g.user is None:
        return False
    return g.user.verify_password(password)

@api.before_request
@auth.login_required
def before_request():
    g.now = datetime.now(pytz.timezone('Europe/Athens'))

@auth.error_handler
def unauthorized():
    response = jsonify(dict(status=401, error='Unauthorized',
                            message='Please Authenticate'))
    response.status_code = 401
    return response

@api.route('/authenticate', methods=['POST'])
@auth.login_required
def authenticate():
    # Authenticate is a wrapper for third party apps to aunthenticate
    user = g.user.email
    return jsonify(dict(message="Authenticated", user=user))

@api.route('/spots/needs/today', methods=['GET'])
def get_spots_needs_summary():
    needs = Need.query.filter_by(date=g.now.date())
    spots = set([n.spots for n in needs])
    return jsonify(dict(spots=[s.export_data() for s in spots]))

@api.route('/spots/<int:id>/needs/today', methods=['GET'])
def get_spot_needs(id):
    spot = Spot.query.get(id)
    return jsonify(dict(spot=spot.export_needs(g.now.date())))
