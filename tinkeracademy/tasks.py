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
from pageutils import isadminuser
from environment import updatetokens

class EmailTask(webapp2.RequestHandler):
	def get(self):
		emailservice = EmailService()
		emailservice.sendnext()

class DatabaseUpdateTask(webapp2.RequestHandler):
	def get(self):
		ipaddress = self.request.remote_addr
		if isadminuser:
			try:
				databaseservice = DatabaseService()
				databaseservice.updategeoip(ipaddress)
			except:
				logging.error("database update from admin user from ipaddress=" + str(ipaddress))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])
		else:
			logging.error("database update from non-admin user from ipaddress=" + str(ipaddress))

class TokenUpdateTask(webapp2.RequestHandler):
	def get(self):
		updatetokens()
