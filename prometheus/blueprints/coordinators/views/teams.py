from prometheus import db
from .. import coordinator
from flask import render_template, url_for, redirect, flash

from prometheus.models.core import Team, Country

from ..forms import TeamForm

@coordinator.route('/teams')
def teams():
    obj_list = Team.query.all()
    page = dict(title="Teams", add_url='coordinator.update_team',
                delete_url='coordinator.delete_team',
                edit_url='coordinator.update_team')
    return render_template('coordinators/teams/team_list.html',
                            obj_list=obj_list, page=page)

@coordinator.route('/team/update', methods=['GET', 'POST'])
@coordinator.route('/team/<int:id>/update', methods=['GET', 'POST'])
def update_team(id=None):
    page = dict(title="Add Team", back=url_for('coordinator.teams'))
    team = Team()
    form = TeamForm()
    if id != None:
        team = Team.query.get(id)
        form = TeamForm(obj=team)
    form.country_id.choices = [(c.id, c.name)
                               for c in Country.query.order_by('name')]
    if form.validate_on_submit():
        team.import_data(form.data)
        db.session.add(team)
        db.session.commit()
        flash("<i class='fa fa-smile-o'></i> Success, form is submitted")
        return redirect(url_for('coordinator.teams'))
    return render_template('coordinators/teams/team_form.html', page=page,
                            form=form)

@coordinator.route('/team/delete/<int:id>')
def delete_team(id):
    team = Team.query.get(id)
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for('coordinator.teams'))
