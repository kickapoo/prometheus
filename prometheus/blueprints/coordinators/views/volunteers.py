from prometheus import db
from .. import coordinator
from flask import render_template, url_for, redirect, flash

from prometheus.models.auth import User, Role
from prometheus.models.core import Volunteer, Country, Team
from ..forms import VolunteerForm


@coordinator.route('/volunteers')
def volunteers():
    obj_list = Volunteer.query.all()
    page = dict(title="Volunteer", add_url='coordinator.update_volunteer',
                delete_url='coordinator.delete_volunteer',
                edit_url='coordinator.update_volunteer')
    return render_template('coordinators/volunteers/volunteer_list.html',
                            obj_list=obj_list, page=page)

@coordinator.route('/volunteer/update', methods=['GET', 'POST'])
@coordinator.route('/volunteer/<int:id>/update', methods=['GET', 'POST'])
def update_volunteer(id=None):
    page = dict(title="Add Volunteer", back=url_for('coordinator.volunteers'))
    if Role.query.filter_by(name="volunteer").first() is None:
        role_volunteer = Role(name='volunteer')
        db.session.add(role_volunteer)
        db.session.commit()
    role_volunteer = Role.query.filter_by(name="volunteer").first()
    role_coordinator = Role.query.filter_by(name="coordinator").first()
    user_volunteer = User()
    volunteer = Volunteer()
    form = VolunteerForm()
    if id != None:
        volunteer = Volunteer.query.get(id)
        user_volunteer = User.query.filter_by(email=volunteer.email).first()
        form = VolunteerForm(obj=volunteer)
    form.is_coordinator.checked = False
    if role_coordinator in user_volunteer.roles:
        form.is_coordinator.checked = True
    form.access.checked = user_volunteer.active
    form.country_id.choices = [(c.id, c.name) for c in Country.query.order_by('name')]
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    if form.validate_on_submit():
        volunteer.import_data(form.data)
        if user_volunteer.email is None:
            # Register Volunteer as User
            user_volunteer.email = form.email.data
            user_volunteer.set_password(form.email.data)
            user_volunteer.active = form.access.data
            user_volunteer.roles.append(role_volunteer)
            if form.is_coordinator.data:
                user_volunteer.roles.append(role_coordinator)
            else:
                if role_coordinator in user_volunteer.roles:
                    user_volunteer.roles.remove(role_coordinator)
            db.session.add(user_volunteer)
            db.session.commit()
        else:
            #  Update access
            user_volunteer.active = form.access.data
            if form.is_coordinator.data:
                user_volunteer.roles.append(role_coordinator)
            else:
                if role_coordinator in user_volunteer.roles:
                    user_volunteer.roles.remove(role_coordinator)
            db.session.add(user_volunteer)
            db.session.add(user_volunteer)
            db.session.commit()
        db.session.add(volunteer)
        db.session.commit()
        flash("<i class='fa fa-smile-o'></i> Success, form is submitted")
        return redirect(url_for('coordinator.volunteers'))
    return render_template('coordinators/volunteers/volunteer_form.html',
                           page=page, form=form)

@coordinator.route('/volunteer/delete/<int:id>')
def delete_volunteer(id):
    volunteer = Volunteer.query.get(id)
    db.session.delete(volunteer)
    db.session.commit()
    return redirect(url_for('coordinator.volunteers'))
