import os
import sys
import urllib
import jinja2
import logging
import time
import webapp2
import httplib2

from services import EmailService
from services import DatabaseService
from services import TinkerAcademyUserService
from pageutils import isadminuser
from environment import updatetokens

class EmailTask(webapp2.RequestHandler):
	def get(self):
		emailservice = EmailService()
		emailservice.sendnext()

class DatabaseUpdateTask(webapp2.RequestHandler):
	def get(self):
		userservice = TinkerAcademyUserService()
		studentid = "2015035"
		studentname = "Timothy Liu"
		user = userservice.finduserbystudentid(studentid)
		if user:
			try:
				user.studentname = studentname
				user.put()
			except:
				logging.error("error updating user=" + str(studentid))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])
		else:
			logging.error("user not found=" + str(studentid))

class TokenUpdateTask(webapp2.RequestHandler):
	def get(self):
		updatetokens()
