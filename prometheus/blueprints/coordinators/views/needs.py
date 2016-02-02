from prometheus import db
from .. import coordinator
from flask import g, render_template, url_for, redirect, flash

from prometheus.models.core import Need, Spot
from ..forms import NeedForm, SingleDateForm

@coordinator.route('/needs')
def needs():
    needs = Need.query.filter_by(date=g.now.date())
    page = dict(title="Needs", add_url='coordinator.update_need',
                delete_url='coordinator.delete_need',
                edit_url='coordinator.update_need')
    return render_template('coordinators/needs/need_list.html',
                            obj_list=needs, page=page)

@coordinator.route('/need/update', methods=['GET', 'POST'])
@coordinator.route('/need/<int:id>/update', methods=['GET', 'POST'])
def update_need(id=None):
    page = dict(title="Add Need", back=url_for('coordinator.needs'))
    need = Need()
    form = NeedForm()
    if id != None:
        need = Need.query.get(id)
        form = NeedForm(obj=need)
    form.spot_id.choices = [(s.id, s.name)
                            for s in Spot.query.filter_by(status=True)]
    if form.validate_on_submit():
        need.import_data(form.data)
        db.session.add(need)
        db.session.commit()
        flash("<i class='fa fa-smile-o'></i> Success, form is submitted")
        return redirect(url_for('coordinator.needs'))
    return render_template('coordinators/needs/need_form.html',
                            page=page, form=form)

@coordinator.route('/need/delete/<int:id>')
def delete_need(id):
    need = Need.query.get(id)
    db.session.delete(need)
    db.session.commit()
    return redirect(url_for('coordinator.needs'))

@coordinator.route('/need/history/', methods=['GET', 'POST'])
@coordinator.route('/need/history/<date>', methods=['GET', 'POST'])
def history_needs(date=None):
    page = dict(title="Needs History", delete_url='coordinator.delete_need',
                edit_url='coordinator.update_need')
    form = SingleDateForm()
    if date is None:
        date = str(g.now.date())
        obj_list = Need.query.filter_by(date=g.now.date()).all()
    if form.validate_on_submit():
        date = str(form.date.data)
        obj_list = Need.query.filter_by(date=form.date.data).all()
    return render_template('coordinators/needs/history.html',
                            obj_list=obj_list, page=page,
                            date=date, form=form)
