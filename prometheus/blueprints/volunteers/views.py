from prometheus import db
from . import volunteer
from flask import g,render_template, request, redirect, url_for, jsonify, flash
from flask.ext.login import current_user

from prometheus.models.core import Spot, Need, Volunteer
from prometheus.models.auth import User
from prometheus.blueprints.auth.forms import ChangePassword


@volunteer.route('/')
def index():
    page = dict(title="Needs Report")
    spots = Spot.query.all()
    spots_open_count = Spot.query.filter_by(status=True).count()
    spots_close_count = Spot.query.filter_by(status=False).count()
    volunteer = Volunteer.query.filter_by(email=current_user.email).first()
    spot_latest = Spot.query.order_by(Spot.updated_at).first()
    need_latest = Need.query.order_by(Need.updated_at).first()
    needs = Need.query.filter_by(date=g.now.date()).all()
    last_updated = max(need_latest.updated_at, spot_latest.updated_at)
    for need in needs:
        need.remaining = int(need.number_of_volunters) - need.volunteer.count()
        need.user_allready_in = False
        if volunteer in need.volunteer.all():
            need.user_allready_in = True
        need.show_selection = False
        if need.remaining > 0 and not need.user_allready_in:
            need.show_selection = True
    return render_template(
        'volunteers/index.html', spots=spots, obj_list=needs,
         spots_open_count=spots_open_count, spots_close_count=spots_close_count,
         last_updated=last_updated,page=page, volunteer=volunteer
    )


@volunteer.route('/change/password', methods=['GET', 'POST'])
def change_password():
    page = dict(title="Needs Report")
    form = ChangePassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password changed')
        return redirect(url_for('volunteer.index'))
    return render_template('volunteers/change_password.html',
                            page=page, volunteer=volunteer,
                            form=form)

#### Ajax calls on user selection #####
@volunteer.route('/selection/', methods=['POST'])
def volunteer_selections():
    # Add volunter to a specific listed Need.
    if request.method == 'POST':
        need = Need.query.get(request.json['need_id'])
        volunteer = Volunteer.query.get(request.json['volunteer_id'])
        need.volunteer.append(volunteer)
        db.session.add(need)
        db.session.commit()
        return jsonify({'message':'success'}), 201, {}
