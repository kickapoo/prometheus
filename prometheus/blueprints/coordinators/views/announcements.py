from prometheus import db
from .. import coordinator
from flask import render_template, url_for, redirect, flash

from prometheus.models.core import Announcement
from ..forms import AnnouncementForm

@coordinator.route('/announcements/')
def announcements():
    announcements = Announcement.query.all()
    page = dict(title="announcements",
                add_url='coordinator.update_announcement',
                delete_url='coordinator.delete_announcement',
                edit_url='coordinator.update_announcement')
    return render_template('coordinators/announcements/announcement_list.html',
                            obj_list=announcements,
                            page=page)

@coordinator.route('/announcement/update', methods=['GET', 'POST'])
@coordinator.route('/announcement/<int:id>/update', methods=['GET', 'POST'])
def update_announcement(id=None):
    page = dict(title="Add Announcement",
                back=url_for('coordinator.announcements'))
    announcement = Announcement()
    form = AnnouncementForm()
    if id != None:
        announcement = Announcement.query.get(id)
        form = AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        announcement.import_data(form.data)
        db.session.add(announcement)
        db.session.commit()
        flash("<i class='fa fa-smile-o'></i> Success, form is submitted")
        return redirect(url_for('coordinator.announcements'))
    return render_template('coordinators/announcements/announcement_form.html',
                            page=page, form=form)

@coordinator.route('/announcement/delete/<int:id>')
def delete_announcement(id):
    announcement = Announcement.query.get(id)
    db.session.delete(announcement)
    db.session.commit()
    return redirect(url_for('coordinator.announcements'))
