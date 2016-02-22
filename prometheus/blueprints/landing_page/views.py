from prometheus import owm
from . import landing_page
from flask import g, render_template, current_app

from prometheus.models.core import Spot, Need, Announcement

@landing_page.route('/')
def index():
    # User can view the latest 20 records there is no need for more can that
    island = {'name': current_app.config['AREA']}
    announcements = Announcement.query.order_by(
                    Announcement.created_at.desc()).all()[:20]
    weather = owm.weather_at_coords(g.lat, g.lon).get_weather()
    needs = Need.query.filter_by(date=g.now.date()).all()
    for need in needs:
        need.remaining = int(need.number_of_volunters) - need.volunteer.count()
    spots = Spot.query.all()
    spots_open_count = Spot.query.filter_by(status=True).count()
    spots_close_count = Spot.query.filter_by(status=False).count()
    spot_latest = Spot.query.order_by(Spot.updated_at.desc()).first()
    need_latest = Need.query.order_by(Need.updated_at.desc()).first()
    last_updated = max(need_latest.updated_at, spot_latest.updated_at)
    return render_template('landing_page/index.html',
                            needs=needs,
                            spots = spots,
                            spots_open_count=spots_open_count,
                            spots_close_count=spots_close_count,
                            last_updated=last_updated,
                            announcements=announcements,
                            weather=weather,
                            island=island)
