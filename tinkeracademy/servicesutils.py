import logging
import os
import sys
import uuid
import constants
import json

from datetime import datetime
from dateutil import parser

def processstr(entry, field):
	text = entry.custom[field].text
	return text
def processint(entry, field):
	text = processstr(entry, field)
	if text:
		return int(text)
	return 0
def processboolean(entry, field):
	int_ = processint(entry, field)
	return int_ != 0



