
![](http://chios.prometheus.online/static/imgs/logo-prometheus.png)


### Description
Prometheus is a web app to support Teams/Volunteer with their Needs management. It separates users to two roles, Coordinators and Volunteer. Any Volunteer can be a Coordinator and a Coordinator must be a Volunteer. 

A Coordinator can register Volunteers and grand them access to the system or change Volunteer role to Coordinator. Cordinators can also add a Spot, which are the geolocations that Teams operate. Finally, a Coordinator can add daily Needs with the number of volunteers needed and time period requested (morning, evening etc)

After a Need is submitted, all Volunteers with access can select to contribute to a specific Need and listed to that specific Need. If Volunteer fill the number that is needed, Need is closed for further selection. 

As a sequence of the above, Coordinators know which the Need cycle and from which Volunteers this Need will be fullfilled.

### Screenshots

![Prometheus](http://demo.prometheus.online/static/imgs/PrometheusScreenShots.png)


### Demo and Real Case

Demo case : [demo.prometheus.online](http://demo.prometheus.online/)

Chios island: [chios.prometheus.online](http://demo.prometheus.online/)

### How this project started?
Prometheus started as part of [Informatics & Communications Technologies for Development, Aid, Support and Collaboration (ICT4dascgr)](http://groupspaces.com/ICT4dascgr/) actions to support Volunteers that take part on helping refugees across Aegean, Greek islands. There are other tools that serve the same goal but Prometheus wants to stand among them through the simplicity it offers. Prometheus, does what it says and say what is does, nothing more or nothing else.

### Build with
Prometheus is a [Flask](http://flask.pocoo.org/) web application with Sqlite3 database. The choice of [SQLite](https://www.sqlite.org/) is crusial as requires no special settings. Also the single database file can be shared easily supporting the main operation center. 

### Setup at localhost 

Requirements:

1. Computer with python 2.7 [installed](http://docs.python-guide.org/en/latest/starting/installation/)
2. Virtualenv [installed](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref)
3. [OpenWeatherMaps.org](http://openweathermap.org/api) API KEY

Assuming that the reader has some pre-knowledge using ternimal and command line, the next standard steps much be followed in order: 

	1. Download/Extract repository zip file or clone repository
	2. $ cd prometheus
	3. Edit the following 'configs/prometheus-settings.py'
		- OWM_KEY , openweathermaps.org API KEY
		- AREA, the installation area name ex. 'CHIOS'
		- MAP_LAT_CENTER,
		- MAP_LON_CENTER, 
	4. virtualenv venv
	5. $ /venv/bin/pip install -r requirement.txt
	6. $ /venv/bin/python manager.py init_prometheus
	7. $ /venv/bin/python manager.py runserver
	8. Go to 127.0.0.1:5000 or localhost:5000i
	9. Enter system using the credentials: 
	    email: admin@prometheus.online
	    pass: admin

### Prometheus File structure
	- config
		- default.py # Basic Flask config options
		- prometheus-settings.py # Special settings like lat or lon coordinates
	- prometheus
		- __init__.py 
		- blueprints
			- landing_page # Single Page 
			- auth # Login/Logout
			- coordinators 
			- volunteers 
			- api # Using AuthO to authenticate
		- models
			- auth.py # User and UserRoles
			- core.py # Team Volunteer Spot Need 
		- static
		- templates 

### Extensions and Frontend libs
Prometheus as native Flask app take the advantage of the following extentions:

1. [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
2. [Flask-Script](https://flask-script.readthedocs.org/en/latest/)
3. [Flask-Moment](https://github.com/miguelgrinberg/Flask-Moment)
4. [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
5. [Flask-Login](https://flask-login.readthedocs.org/en/latest/)

Also, openweathermaps.org are used through [PyOWM - A Python wrapper around the OpenWeatherMap web API](https://github.com/csparpa/pyowm)leaf

For front-end the following are used:

1. SB-Admin 2 as the bootstrap theme for the admin panel
2. [Leaflet.js](http://leafletjs.com/) maps
3. [MakiMarker](https://github.com/jseppi/Leaflet.MakiMarkers) for more pointer icons options
4. [Datatables](http://datatables.net/) for listing and searchin database records
5. [Font-Awesome](https://fortawesome.github.io/Font-Awesome/) for more icons options

### TODO

1. Support database migrations with Flask-Migrate
2. Support mutlilanguage with Flask-Babel
3. Overhaul front end from someone who actually knows more html,css than backend coding.
4. Find funding to continue adding features like Materials (Wharehouse) management or mobile application.

### Contribute

Feel free to contribute by using github issues and pull requests or just by sharing this project to others. The rule is simple, if a contribution rather than mine exists, a page in footer will be added to list Contributor name with a link to their personal page. By Coordibution does't mean only coding.

### Licence 
[GNU GENERAL PUBLIC LICENSE Version 3](http://www.gnu.org/licenses/gpl-3.0.en.html)