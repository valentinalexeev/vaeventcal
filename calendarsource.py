from pytz.gae import pytz
from icalendar import Calendar, Event
import datetime
import httplib2
from bs4 import BeautifulSoup as bs

class CalendarSource:
	def get_calendar(self, sourceObject):
		raise error("Abstract method call.")

	def get_source(self, type):
		if type == "bileter":
			return BileterSource()

class BileterSource(CalendarSource):
	base_url = "http://www.bileter.ru/afisha"

	def get_calendar(self, sourceObject):
		if sourceObject.url:
			print self.base_url + "/" + sourceObject.url + "/" + datetime.datetime.now().strftime("%Y-%m-%d") + "/"

			opener = httplib2.Http()
			#opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36')]
			#urllib2.install_opener(opener)
			response, content = opener.request(
				self.base_url + 
				"/" + 
				sourceObject.url + 
				"/" + 
				datetime.datetime.now().strftime("%Y-%m-%d") + "/")

			if response.status == 200:
				print content
				resp = bs(content)

				events = resp.find_all("div", {"class": "afisha_events_item"})

				icalCalendar = Calendar()
				for event in events:
					icalEvent = Event()
					icalEvent.add("summary", event.find("h4").text)
					dtstart = datetime.strptime(
						"%Y-%M-%d %H:%M", 
						datetime.datetime.now().strftime("%Y-%M-%d") + " " + event.find("p", {"class" : "first"}).text)
					icalEvent.add("dtstart", dtstart)

					dtend = dtstart
					dtend.replace(hour=dtstart.hour + 2)
					icalEvent.add("dtend", dtend)

					icalCalendar.add_component(icalEvent)

				return icalCalendar.to_ical()
			raise error("No data fetched")
		raise error("Invalid source object")
