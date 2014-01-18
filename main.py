import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import cgi

from dbmodel import *
from calendarsource import *

class MainHandler(webapp2.RequestHandler):
	def get(self):
		return

class CalendarHandler(webapp2.RequestHandler):
	def get(self):
		calendarHash = cgi.escape(self.request.get('cal'))

		if calendarHash:
			cal = db.GqlQuery('SELECT * FROM CalendarSource WHERE hash = :1', calendarHash).get();

			if cal:
				src = CalendarSource().get_source(cal.type)
				self.response.write(src.get_calendar(cal))
				return
			raise error("No calendar found")
		raise error("Malformed request")



app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/cal', CalendarHandler)
	])