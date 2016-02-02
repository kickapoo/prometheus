from .. import coordinator
from flask import render_template

from prometheus.blueprints.auth.forms import ChangePassword
from prometheus.models.core import Spot

@coordinator.route('/')
def overview():
    spots = Spot.query.all()
    spots_open_count = Spot.query.filter_by(status=True).count()
    spots_close_count = Spot.query.filter_by(status=False).count()
    return render_template('coordinators/overview.html', spots=spots,
                            spots_open_count=spots_open_count,
                            spots_close_count=spots_close_count)

@coordinator.route('/change-password')
def change_password():
    page = dict(title="Change Password")
    form = ChangePassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password changed')
        return redirect(url_for('coordinator.overview'))
    return render_template('coordinators/change_password.html',
                            page=page,
                            form=form)
