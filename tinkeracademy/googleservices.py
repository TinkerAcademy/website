import logging
import os
import sys
import uuid
import constants
import traceback

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
	def getfiletitle(self, fileresource):
		title = None
		if fileresource:
			title = fileresource['title']
		return title
	def getfilecontents(self, fileresource, contenttype):
		content = None
		if fileresource:
			# from pprint import PrettyPrinter
			# pp = PrettyPrinter(indent=4)
			# content = pp.pformat(fileresource)
			# logging.info(content)
			exportLinks = fileresource['exportLinks']
			downloadurl = exportLinks[contenttype]
			resp, content = GOOGLE_DRIVE_SERVICE._http.request(downloadurl)
			if resp.status != 200:
				logging.warning('GoogleDriveService.getfilecontents got response.status='+response.status+', for id='+str(fileid))
		else:
			logging.warning('GoogleDriveService.getfile could not find file using id='+str(fileid))
		return content
	def getfile(self, fileid):
		try:
			googlefiles = GOOGLE_DRIVE_SERVICE.files()
			fileresource = googlefiles.get(fileId=fileid).execute()
			return fileresource
		except:
			logging.error('GoogleDriveService.getfile unable to retrieve file using id='+str(fileid))
			stacktrace = traceback.format_exc()
			logging.error("%s", stacktrace)
		return None



