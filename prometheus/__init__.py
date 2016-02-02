from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
import pyowm

app = Flask(__name__, instance_relative_config=True)
# config.default
app.config.from_object('config.default')
# config.prometheues-settings.py
app.config.from_object('config.prometheus-settings')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
owm = pyowm.OWM(app.config['OWM_KEY'])

# Landing_page hold a single view
from blueprints.landing_page import landing_page as landing_page_blueprint
app.register_blueprint(landing_page_blueprint, url_prefix='/')

# Auth holds all login/logout/registration actions.
# Auth uses 'User' model with NO relation mapping to app.models.core
# Authentication is made with the help of Flask-Login
from blueprints.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Coordinator holds an 'admin' panel for coordinators
# A coordinator can create/edit/delete (CRUD),
# Team/Voluntter/Needs to database
from blueprints.coordinators import coordinator as coordinator_blueprint
app.register_blueprint(coordinator_blueprint, url_prefix='/coordinator')

# Volunter holds a single page in order potential volunteer to select his/her
# daily contribution in Needs.
from blueprints.volunteers import volunteer as volunteer_blueprint
app.register_blueprint(volunteer_blueprint, url_prefix='/volunteer')

# Flatpages holds terms-of-use, policy etc
from blueprints.flatpages import flatpages as flatpages_blueprint
app.register_blueprint(flatpages_blueprint, url_prefix='/flatpages')

# Prometheus api using Basic AuthO Authentication
from blueprints.api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api/v1')
