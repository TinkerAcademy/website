import logging
import os
import sys
import uuid
import constants

from environment import GOOGLE_DRIVE_SERVICE \
						, GOOGLE_SPREADSHEETS_SERVICE

class GoogleSpreadsheetService(object):
	def getrows(self, spreadsheetid, worksheetid):
		rows = GOOGLE_SPREADSHEETS_SERVICE.GetListFeed(spreadsheetid, worksheetid)
		return rows
	# def getworksheets(self, spreadsheetid, worksheetid=None):
	# 	worksheets = GOOGLE_SPREADSHEETS_SERVICE.GetWorksheetsFeed(spreadsheetid, worksheetid)
	# 	return worksheets

class GoogleDriveService(object):
	def getfile(self, title):
		try:
			param = {}
			files = GOOGLE_DRIVE_SERVICE.files().list(**param).execute()
			# logging.info('GoogleService.getfile #items=' + str(len(files['items'])))
			items = files['items']
			item = None
			for item in items:
				if item['title'] == title:
					break
			return item
		except:
			logging.error('GoogleDriveService.list_files error')
			sys_err = sys.exc_info()
			logging.error(sys_err[1])
		return None



