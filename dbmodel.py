from google.appengine.ext import db
from google.appengine.api import urlfetch

class CalendarSource(db.Model):
	url = db.StringProperty()
	type = db.StringProperty(default="bileter")
	hash = db.StringProperty()