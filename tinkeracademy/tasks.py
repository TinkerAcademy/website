import os
import sys
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

class DatabaseUpdateTask(webapp2.RequestHandler):
	def get(self):
		ipaddress = self.request.remote_addr
		if isadminuser:
			try:
				databaseservice = DatabaseService()
				databaseservice.updategeoip(ipaddress)
			except:
				logging.error("database update from " + str(ipaddress))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])
		else:
			logging.error("database update from non-admin user from " + str(ipaddress))


