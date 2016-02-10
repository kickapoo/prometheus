from flask.ext.wtf import Form
from wtforms import widgets
from wtforms import (StringField, SelectField, DateField, TextAreaField,
                     FloatField, SelectMultipleField, BooleanField,
                     IntegerField, RadioField)
from wtforms.widgets import TextArea
from wtforms.validators import Required, Length, Email, Optional

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class TeamForm(Form):
    name = StringField(u'Name', validators=[Required(), Length(6, 120)])
    email = StringField(u'Email', validators=[Required(), Email()])
    international_phone = StringField(u'International')
    local_phone = StringField(u'Local')
    country_id = SelectField(u'Country', coerce=int, validators=[Optional()])
    availiable_from = DateField(u'Availiable From:', format='%d/%m/%Y',
                                validators=[Optional()])
    availiable_to = DateField(u'Availiable To:', format='%d/%m/%Y',
                                validators=[Optional()])
    notes = TextAreaField(u'Notes', widget=TextArea(),validators=[Optional()])


class VolunteerForm(Form):
    GENDER_CHOICES = (
        ('0', 'Male'),
        ('1', 'Female'),
    )
    DAY_CHOICES = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Firday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    )
    HOUR_CHOICES = (
        ('0', 'Morning'),
        ('1', 'Evening'),
        ('2', 'Night'),
        ('3', 'Flexible-All Day'),
    )
    LANGUAGES_CHOICES = (
        ('0', 'Arabic'),
        ('1', 'Farsi'),
        ('2', 'Greek'),
        ('3', 'Other'),
    )
    SKILLS_CHOICES = (
        ('0', 'First Aid'),
        ('1', 'Cooking'),
        ('2', 'Lifting'),
        ('3', 'Building'),
        ('4', 'Electorical Circits'),
        ('5', 'Diving'),
        ('6', 'Driving Car'),
        ('7', 'Driving Motor'),
    )
    day_choices = MultiCheckboxField('Days', choices=DAY_CHOICES,
                                      validators=[Optional()])
    hour_choices = MultiCheckboxField('Day periods', choices=HOUR_CHOICES,
                                       validators=[Optional()])
    skills_choices = MultiCheckboxField('Skills', choices=SKILLS_CHOICES,
                                       validators=[Optional()])
    language_choices = MultiCheckboxField('Languages', choices=LANGUAGES_CHOICES,
                                           validators=[Optional()])
    fullname = StringField('Name', validators=[Required(), Length(4, 120)])
    international_phone = StringField(u'International')
    local_phone = StringField(u'Local')
    email = StringField(u'Email', validators=[Required(), Email()])
    country_id = SelectField(u'Country', coerce=int, validators=[Optional()])
    gender = SelectField(u'Gender', choices=GENDER_CHOICES,
                         validators=[Optional()])
    birthday = DateField(u'birthday:', format='%d/%m/%Y',
                         validators=[Optional()])
    availiable_from = DateField(u'Availiable From:', format='%d/%m/%Y',
                                validators=[Optional()])
    availiable_to = DateField(u'Availiable To:', format='%d/%m/%Y',
                              validators=[Optional()])
    notes = TextAreaField(u'Notes', widget=TextArea(),validators=[Optional()])
    team_id = SelectField('Team', coerce=int)
    access = BooleanField(u'System Access')
    is_coordinator = BooleanField(u'is Coordinator')

class SpotForm(Form):
    name = StringField(u'Spot', validators=[Required(), Length(4, 120)])
    lat = FloatField(u'lat', validators=[Required()])
    lon = FloatField(u'lon', validators=[Required()])
    spottype_id = SelectField(u'Type', coerce=int, validators=[Required()])
    status = BooleanField(u'Status')
    capacity = IntegerField(u'Hosts (number of refugees)')
    notes = TextAreaField(u'Notes', widget=TextArea(),validators=[Optional()])


class NeedForm(Form):
    HOUR_CHOICES = (
        ('0', 'Morning'),
        ('1', 'Evening'),
        ('2', 'Night'),
        ('3', 'Flexible-All Day'),
    )
    hour_choices = RadioField('hours', choices=HOUR_CHOICES,
                              validators=[Optional()])
    name = StringField(u'Need', validators=[Required(), Length(4, 120)])
    spot_id = SelectField(u'Spot', coerce=int)
    number_of_volunters = IntegerField(u'Volunteers needed')


class AnnouncementForm(Form):
    ANNOUN_TYPES = (
        ('0', 'General'),
        ('1', 'Need'),
        ('2', 'Emergency'),
    )
    title = StringField(u'Title', validators=[Required(), Length(4, 110)])
    body = TextAreaField(u'Main Body', widget=TextArea(),
                         validators=[Length(4, 10000), Optional()])
    announcement_choices = SelectField('Type', choices=ANNOUN_TYPES,
                                      validators=[Required()])

class SingleDateForm(Form):
    date = DateField(u'Availiable From:', format='%d/%m/%Y',
                                          validators=[Optional()])
