import logging
import os
import sys
import uuid
import constants
import json

from datetime import datetime
from dateutil import parser

from google.appengine.ext import db

def processstr(entry, field):
	text = entry.custom[field].text
	return text
def processtext(entry, field):
	text = entry.custom[field].text
	return db.Text(text)	
def processint(entry, field):
	text = processstr(entry, field)
	if text:
		return int(text)
	return 0
def processboolean(entry, field):
	int_ = processint(entry, field)
	return int_ != 0
def readtextfilecontents(filename):
	contents = None
	file_ = open(filename, 'r')
	try:
		contents = file_.read()
	finally:
		if file_:
			file_.close()
	return contents



