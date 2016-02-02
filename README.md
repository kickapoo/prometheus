Prometheus is simple Team/Volunteer Need management tool, initially started to
support Volunteer Teams that operate on Aegean Islands, Greece.
Prometheus tries to fill the gap of daily needs management with simplicity as
primary key. It does what is says and says what is does.


A quick start guide if you are familiar with Python and Flask:

1. `$ git clone ... && cd ...`

2. Edit `/config/prometheus-settings.py`

    OWM_KEY = ''         # http://openweathermap.org/ API Key
    AREA = ''            # Installation Aegean ex 'Chios'
    MAP_LAT_CENTER = ''  # Center Map ex '38.3709813'
    MAP_LON_CENTER = ''  # Center Map ex '26.1363457'

3. `$ virtualenv venv`
4. `$ /venv/bin/pip install -r requirement.txt`
5. `$ /venv/bin/python manager.py init_prometheus`
6. `$ /venv/bin/python manager.py runserver`
7.  Test it on: `127.0.0.1:5000` or `localhost:5000`
    using initial admin credentials: `admin@prometheus.online, admin`

Soon details will be added...
