from prometheus import db
from .. import coordinator
from flask import g, render_template, url_for, redirect, flash

from prometheus.models.core import Spot, SpotType, SpotTrace
from ..forms import SpotForm


@coordinator.route('/spots')
def spots():
    obj_list = Spot.query.all()
    page = dict(title="Spot", add_url='coordinator.update_spot',
                delete_url='coordinator.delete_spot',
                edit_url='coordinator.update_spot')
    return render_template('coordinators/spots/spot_list.html',
                            obj_list=obj_list, page=page)

@coordinator.route('/spot/update', methods=['GET', 'POST'])
@coordinator.route('/spot/<int:id>/update', methods=['GET', 'POST'])
def update_spot(id=None):
    page = dict(title="Add Spot", back=url_for('coordinator.spots'))
    spot = Spot()
    form = SpotForm()
    if id != None:
        spot = Spot.query.get(id)
        form = SpotForm(obj=spot)
    form.spottype_id.choices = [(c.id, c.name)
                                for c in SpotType.query.order_by('name')]
    if form.validate_on_submit():
        spot.import_data(form.data)
        db.session.add(spot)
        db.session.commit()
        # Trace Spot capacity
        st = SpotTrace(spot_id=spot.id, capacity=spot.capacity, timestamp=g.now)
        db.session.add(st)
        db.session.commit()
        flash("<i class='fa fa-smile-o'></i> Success, form is submitted")
        return redirect(url_for('coordinator.spots'))
    return render_template('coordinators/spots/spot_form.html',
                            page=page, form=form)

@coordinator.route('/spot/delete/<int:id>')
def delete_spot(id):
    spot = Spot.query.get(id)
    db.session.delete(spot)
    db.session.commit()
    return redirect(url_for('coordinator.spots'))
