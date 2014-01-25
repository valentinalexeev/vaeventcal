import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import cgi

from dbmodel import CalendarSource as CalendarSourceDb
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
				self.response.headers['Content-type'] = "text/calendar; charset=utf-8"
				self.response.write(src.get_calendar(cal))
				return
			raise error("No calendar found")
		raise error("Malformed request")

class AddCalendarHandler(webapp2.RequestHandler):
	def get(self):
		type = cgi.escape(self.request.get('type'))
		url = cgi.escape(self.request.get('url'))
		hash = cgi.escape(self.request.get('hash'))

		src = CalendarSourceDb()
		src.type = type
		src.url = url
		src.hash = hash
		src.put()

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/cal', CalendarHandler),
	('/add', AddCalendarHandler)
	])