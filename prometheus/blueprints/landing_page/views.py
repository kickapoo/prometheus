from prometheus import owm
from . import landing_page
from flask import g, render_template, current_app

from prometheus.models.core import Announcement

@landing_page.route('/')
def index():
    # User can view the latest 20 records there is no need for more can that
    island = {'name': current_app.config['AREA']}
    announcements = Announcement.query.order_by(
                    Announcement.created_at.desc()).all()[:20]
    weather = owm.weather_at_coords(g.lat, g.lon).get_weather()
    return render_template('landing_page/index.html',
                            announcements=announcements,
                            weather=weather, island=island)
