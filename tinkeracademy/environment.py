import os
import urllib
import jinja2
import logging
import webapp2
import httplib2
import constants
import httplib2

from google.appengine.api import memcache
from google.appengine.api import app_identity

from gdata.spreadsheet.service import SpreadsheetsService

# from oauth2client.appengine import AppAssertionCredentials
from apiclient.discovery import build

from oauth2client.client import SignedJwtAssertionCredentials

from google.appengine.api import urlfetch

urlfetch.set_default_fetch_deadline(60)

oldfetch =urlfetch.fetch

###############################################################################
## Code below sets the templating environment
###############################################################################

JINJA_ENVIRONMENT = jinja2.Environment(
		loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
		extensions = ['jinja2.ext.autoescape'],
		autoescape = True
	)


###############################################################################
## Code below Updates URL Fetch & socket timeouts
###############################################################################

def newfetch(url, payload=None, method=urlfetch.GET, headers={},
				allow_truncated=False, follow_redirects=True,
				deadline=None, *args, **kwargs):
	return oldfetch(url, payload, method, headers, allow_truncated, 
				follow_redirects, 60.0, *args, **kwargs)

urlfetch.fetch = newfetch

import socket

socket.setdefaulttimeout(60)
socket._GLOBAL_DEFAULT_TIMEOUT = 60

###############################################################################
## Code below Authenticates - However drive files() need to be able to specify 
## a sub email account below
###############################################################################

# googleserviceaccount = app_identity.get_service_account_name()
# logging.info('googleserviceaccount='+str(googleserviceaccount))

# googleapicredentials = AppAssertionCredentials(scope=constants.GOOGLE_DRIVE_SCOPE)
# googlehttp = googleapicredentials.authorize(httplib2.Http(memcache))
# googlehttp.debuglevel = True

# GOOGLE_DRIVE_SERVICE = build('drive', 'v2', http=googlehttp)

# GOOGLE_SPREADSHEETS_SERVICE = SpreadsheetsService()
# GOOGLE_SPREADSHEETS_SERVICE.additional_headers = {'Authorization': 'Bearer %s' % googlehttp.request.credentials.access_token}

###############################################################################
## Code below Uses SignedJwtAssertionCredentials
###############################################################################

SERVICE_ACCOUNT_EMAIL='456961407722-i6ic6h60him7hioc2mo9iv42qsd116t5@developer.gserviceaccount.com'
PROJECT_NUMBER='456961407722'

pemfile = file('tinkeracademy.pem', 'rb')
key = pemfile.read()
pemfile.close()

credentials=None

googlehttp=None

GOOGLE_DRIVE_SERVICE = None

GOOGLE_SPREADSHEETS_SERVICE = SpreadsheetsService()

###############################################################################
## Code below updates the tokens
###############################################################################

def updatetokens():
	global credentials
	credentials = SignedJwtAssertionCredentials(
	SERVICE_ACCOUNT_EMAIL,
	key,
	scope=[constants.GOOGLE_DRIVE_SCOPE,constants.GOOGLE_SPREADSHEETS_SCOPE],
	sub='admin@tinkeracademy.com'
	)
	global googlehttp
	googlehttp = httplib2.Http(memcache)
	googlehttp=credentials.authorize(googlehttp)
	global GOOGLE_DRIVE_SERVICE
	GOOGLE_DRIVE_SERVICE = build('drive', 'v2', http=googlehttp)
	GOOGLE_SPREADSHEETS_SERVICE.additional_headers = {'Authorization': 'Bearer %s' % googlehttp.request.credentials.access_token}

