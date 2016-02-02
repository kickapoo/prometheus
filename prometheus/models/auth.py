from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from prometheus.models.core import Volunteer

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(email, password):
        user = User(email=email)
        user.set_password(password)
        user.active = True
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id',
                                                    ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id',
                                                    ondelete='CASCADE'))

    def __repr__(self):
        return '<UserRoles {}>'.format(self.user_id)
