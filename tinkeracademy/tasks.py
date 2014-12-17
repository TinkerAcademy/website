import os
import urllib
import jinja2
import logging
import time
import webapp2
import httplib2

from services import DatabaseService
from pageutils import isadminuser

class EmailTask(webapp2.RequestHandler):
	def get(self):
		pass

class UpdateCoursesDatabaseTask(webapp2.RequestHandler):
	def get(self):
		databaseservice = DatabaseService()
		databaseservice.updatecourses()
