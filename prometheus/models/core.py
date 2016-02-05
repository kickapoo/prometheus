from .. import db
import pytz
from datetime import datetime

class ValidationError(ValueError):
    pass

def now():
    return datetime.now(pytz.timezone('Europe/Athens'))

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    international_phone = db.Column(db.String(120), default="+30-555-555-555")
    local_phone = db.Column(db.String(120), default="+30-555-555-555")
    availiable_from = db.Column(db.Date, default=now)
    availiable_to = db.Column(db.Date, default=now)
    notes = db.Column(db.Text, default=u'Add your Notes')
    # Relations
    volunteer = db.relationship('Volunteer', backref='teams', lazy='dynamic')
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    # Timestamp
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now,
                           onupdate=now)

    def import_data(self, data):
        try:
            self.name = data['name']
            self.email = data['email']
            self.international_phone = data['international_phone']
            self.local_phone = data['local_phone']
            self.availiable_from = data['availiable_from']
            self.availiable_to = data['availiable_to']
            self.country_id = data['country_id']
            self.notes = data['notes']
        except KeyError as e:
            raise ValidationError('Invalid Team: missing' + e.args[0])

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    international_phone = db.Column(db.String(120), default="+30-555-555-555")
    local_phone = db.Column(db.String(120), default="+30-555-555-555")
    gender = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.Date, default=now)
    availiable_from = db.Column(db.Date, default=now)
    availiable_to = db.Column(db.Date, default=now)
    day_choices = db.Column(db.String(120), nullable=True)
    hour_choices = db.Column(db.String(120), nullable=True)
    language_choices = db.Column(db.String(120), nullable=True)
    skills_choices = db.Column(db.String(120), nullable=True)
    notes = db.Column(db.Text, default=u'Add your Notes')
    # Relations
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    need_id = db.Column(db.Integer, db.ForeignKey('needs.id'))
    # Timestamp
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now,
                           onupdate=now)

    def import_data(self, data):
        try:
            self.fullname = data['fullname']
            self.email = data['email']
            self.gender = data['gender']
            self.international_phone = data['international_phone']
            self.local_phone = data['local_phone']
            self.availiable_from = data['availiable_from']
            self.availiable_to = data['availiable_to']
            self.birthday = data['birthday']
            self.country_id = data['country_id']
            self.team_id = data['team_id']
            self.notes = data['notes']
            self.skills_choices = str(data['skills_choices'])
            self.day_choices = str(data['day_choices'])
            self.hour_choices = str(data['hour_choices'])
            self.language_choices = str(data['language_choices'])

        except KeyError as e:
            raise ValidationError('Invalid Team: missing' + e.args[0])

    def __repr__(self):
        return 'Volunteer {}'.format(self.fullname)


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    # Relations
    team = db.relationship('Team', backref='country', lazy='dynamic')
    volunteer = db.relationship('Volunteer', backref='country', lazy='dynamic')
    name = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return '<Country {}>'.format(self.name)


class Spot(db.Model):
    __tablename__ = 'spots'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lat = db.Column(db.Float(), nullable=False)
    lon = db.Column(db.Float(), nullable=False)
    status = db.Column(db.Boolean, default=False)
    capacity = db.Column(db.Integer, default='0')
    notes = db.Column(db.Text, default=u'Add your Notes')
    # Relations
    spottype_id = db.Column(db.Integer, db.ForeignKey('spottypes.id'))
    need = db.relationship('Need', backref='spots', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now,
                           onupdate=now)

    def import_data(self, data):
        try:
            self.name = data['name']
            self.lat = data['lat']
            self.lon = data['lon']
            self.status = data['status']
            self.spottype_id = data['spottype_id']
            self.notes = data['notes']
            self.capacity = data['capacity']
        except KeyError as e:
            raise ValidationError('Invalid Team: missing' + e.args[0])

    def export_data(self):
        return dict(
            id=self.id, name=self.name, lat=self.lat, lon=self.lon,
            type=self.type.name, last_update=self.updated_at,
            current_estimated_capacity=self.capacity,
            needs_today=len([ n.export_data() for n in self.need.all()])
        )

    def export_needs(self, date):
        return dict(
            self.export_data(),
            needs=[ n.export_data() for n in self.need.all() if n.date == date]
        )

    def __repr__(self):
        return '<Spot {}>'.format(self.name)


class SpotType(db.Model):
    __tablename__ = 'spottypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    # Relations
    spot = db.relationship('Spot', backref='type', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now,
                           onupdate=now)


    def __repr__(self):
        return '<SpotType {}>'.format(self.name)


class Need(db.Model):
    __tablename__ = 'needs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date(), default=datetime.today)
    hour_choices = db.Column(db.String(120), nullable=True)
    number_of_volunters = db.Column(db.Integer, nullable=False)
    # Relations
    spot_id = db.Column(db.Integer, db.ForeignKey('spots.id'))
    volunteer = db.relationship('Volunteer', backref='need', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now,
                           onupdate=now)

    def import_data(self, data):
        try:
            self.name = data['name']
            self.hour_choices = str(data['hour_choices'])
            self.spot_id = data['spot_id']
            self.number_of_volunters = data['number_of_volunters']
        except KeyError as e:
            raise ValidationError('Invalid Team: missing' + e.args[0])

    def export_data(self):
        HOUR_CHOICES = (
            ('0', 'Morning'),
            ('1', 'Evening'),
            ('2', 'Night'),
            ('3', 'Flexible-All Day'),
        )
        return dict(
            name=self.name, number_of_volunters_needed=self.number_of_volunters,
            hour_choices=HOUR_CHOICES[int(self.hour_choices)][1],
            self_assigned_volunters=[v.fullname for v in self.volunteer.all()],
            last_update=self.updated_at,
        )

    def __repr__(self):
        return '<Need {}>'.format(self.name)


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, default=u'Add Main Text')
    announcement_choices = db.Column(db.String(120), nullable=True)
    # Timestamp
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now,
                           onupdate=now)

    def import_data(self, data):
        try:
            self.title = data['title']
            self.body = data['body']
            self.announcement_choices = str(data['announcement_choices'])
        except KeyError as e:
            raise ValidationError('Invalid Team: missing' + e.args[0])

    def __repr__(self):
        return '<Announcement {}>'.format(self.title)
