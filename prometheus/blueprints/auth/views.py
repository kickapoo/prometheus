from prometheus import login_manager
from . import auth
from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import login_user, logout_user, login_required

from prometheus.models.auth import User, Role
from .forms import LoginForm

login_manager.login_view = 'auth.login'
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash("Wrong credentials ... please try again")
            return redirect(url_for('auth.login', **request.args))
        if not user.active:
            flash("You don't have access, please contact coordinator")
            return redirect(url_for('auth.login', **request.args))
        login_user(user, form.remember_me.data)
        role_coordinator = Role.query.filter_by(name='coordinator').first()
        role_volunteer = Role.query.filter_by(name='volunteer').first()
        # Handling User Roles
        if role_coordinator in user.roles:
            return redirect(request.args.get('next') or url_for('coordinator.overview'))
        elif role_volunteer in user.roles:
            return redirect(request.args.get('next') or url_for('volunteer.index'))
        else:
            flash("You are not authorized to access... ")
            return redirect(url_for('auth.login', **request.args))
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')
