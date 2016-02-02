#!/usr/bin/python
import re
import getpass

from flask.ext.script import Manager
from sqlalchemy import or_

from prometheus import app, db
from prometheus.models.auth import User, Role
from prometheus.models.core import (Team, Volunteer, Spot, SpotType, Country,
                                    Need)

manager = Manager(app)

@manager.command
def create_db():
    # Create database and populate db
    db.create_all()
    db.session.add_all([
        Role(name='sudo'), Role(name='coordinator'), Role(name='volunteer'),
        Team(name='Default: Local Team', email='team@prometheus.online'),
        User.register(email='volunteern@prometheus.online', password='volunteer'),
        Volunteer(fullname='Default Volunteer', email='volunteer@prometheus.online',
                  gender='1'),
        SpotType(name='Camp'), SpotType(name='Volunteer Registration'),
        Spot(name='Chios Town', lat='38.3709813', lon='26.1363457',
                  status=True, spottype_id='1'),
        Country(name='Other'), Country(name='Greece'), Country(name='Germany'),
        Need(name='Example Need', number_of_volunters=1, hour_choices='0',
             spot_id='1')
    ])
    db.session.commit()
    return "All db tables are Created, with Prometheus default values"

@manager.command
def init_prometheus():
    create_db()
    user = User.register('admin@prometheus.online', 'admin')
    role_coordinator = Role.query.filter_by(name='coordinator').first()
    role_volunteer = Role.query.filter_by(name='volunteer').first()
    user.roles.append(role_coordinator)
    user.roles.append(role_volunteer)
    db.session.add(user)
    db.session.commit()
    return "{} sudo user created".format(user.email)

@manager.command
def drop_db():
    db.drop_all()
    return "All db tables are Droped, you are in deleting madness"

@manager.command
def create_sudo():
    # Sudo user is just a that has both coordinator, volunteer rules
    # This give the ability to nagivate through all app views (or routes)
    # Also, if you like 'superuser' term ... that ok but in prometheus
    # superuser is sudo user.

    # Checking if Roles are created using create_db command
    if Role.query.filter(or_(Role.name == v for v in
                         ('sudo', 'coordinator', 'volunteer'))).first() is None:
        return """
        You need run 'python manager.py create_db'
        in order to create default user Roles
        """
    email = raw_input("Please enter a valid email:" )
    email_match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)
    if not email_match:
        return "You typed a invalid email address, Please try again"
    if User.query.filter_by(email=email).first() is not None:
        return "A user allready exists with that email address"
    password1 = getpass.getpass(prompt="Please type your password: ")
    password2 = getpass.getpass(prompt="Please re-type your password: ")
    if not password1 == password2:
        return "Your don't match, Please try again"
    user = User.register(email, password1)
    role_sudo = Role.query.filter_by(name='sudo').first()
    role_coordinator = Role.query.filter_by(name='coordinator').first()
    role_volunteer = Role.query.filter_by(name='volunteer').first()
    user.roles.append(role_sudo)
    user.roles.append(role_coordinator)
    user.roles.append(role_volunteer)
    db.session.add(user)
    db.session.commit()
    return "{} sudo user created".format(email)

if __name__ == '__main__':
    manager.run()
