import logging
import os
import sys
import uuid
import constants
import json

from servicesutils import processstr, processtext, processint, processboolean, readtextfilecontents

from datetime import datetime
from dateutil import parser

from google.appengine.api import memcache
from google.appengine.api import mail

from google.appengine.ext import db

from validate_email import validate_email
from geoip import loadgeoip

from googleservices import GoogleDriveService \
							, GoogleSpreadsheetService

from models import User, \
				   UserCourse, \
				   SignUp, \
				   Course, \
				   CourseContent, \
				   CourseHandout, \
				   CourseHomework, \
				   CourseStarterPack, \
				   CourseVideo, \
				   CourseQuiz, \
				   Email, \
				   ChannelPartner, \
				   Staff, \
				   OtherCities

class GeoService(object):
	ipdatabase = loadgeoip()
	def getcountryname(self, ipaddress):
		countrname = None
		try:
			countryname = GeoService.ipdatabase.country_name_by_addr(ipaddress)
		except:
			countryname = None
		return countryname
	def getcitydetails(self, ipaddress):
		cityname = None
		latitude = None
		longitude = None
		try:
			citylookup = GeoService.ipdatabase.record_by_addr(ipaddress)
			cityname = citylookup['city']		
			latitude = citylookup['latitude']
			longitude = citylookup['longitude']
		except:
			cityname = None
			latitude = None
			longitude = None
		return (cityname, latitude, longitude)

class DatabaseService(object):
	def updategeoip(self, ipaddress):
		geoservice = GeoService()		
		countryname = geoservice.getcountryname(ipaddress)
		cityname, latitude, longitude = geoservice.getcitydetails(ipaddress)
		logging.info('databaseupdate requested from ipaddress=' + str(ipaddress) \
						+ ', countryname=' + str(countryname) \
						+ ', cityname=' + str(cityname) \
						+ ', latitude=' + str(latitude) \
						+ ', longitude=' + str(longitude))
		query = SignUp.all()
		query.filter("ipupdated = ", False)
		p = None
		for p in query.run(limit=100):
			ipaddress = str(p.ipaddress)
			countryname = geoservice.getcountryname(ipaddress)
			cityname, latitude, longitude = geoservice.getcitydetails(ipaddress)
			othercities = OtherCities()
			othercities.countryname = countryname
			othercities.cityname = cityname
			othercities.latitude = latitude
			othercities.longitude = longitude
			try:
				othercities.put()
			except:
				logging.error('error putting OtherCities ipaddress=' + str(ipaddress) \
						+ ', countryname=' + str(countryname) \
						+ ', cityname=' + str(cityname) \
						+ ', latitude=' + str(latitude) \
						+ ', longitude=' + str(longitude))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])
			try:
				p.ipupdated = True			
				p.put()
			except:
				logging.error('error updating SignUp ipaddress=' + str(ipaddress))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])

class EmailService(object):
	def register(self, emailtype, senderid, receiveremailid, subject, body, attachment=None):
		senderemailid = str(senderid) + '@' + constants.EMAIL_DOMAIN_APPSPOT
		email = Email()
		email.senderemailid = senderemailid
		email.receiveremailid = receiveremailid
		email.typeid = emailtype
		email.emailupdated = False
		email.subject = db.Text(subject)
		email.body = db.Text(body)
		if attachment:
			email.filename = attachment.filename
		logging.info('adding emailtype=' + str(emailtype) \
			+ ', receiveremailid=' + str(receiveremailid) \
			+ ', subject=' + str(subject))
		email.put()
		return 1
	def sendnext(self):
		query = Email.all()
		query.filter("emailupdated = ", False)
		p = None
		for p in query.run(limit=1):
			senderemailid = str(p.senderemailid)
			receiveremailid = str(p.receiveremailid)
			subject = str(p.subject)
			body = str(p.body)
			filename = str(p.filename)
			attachment = None
			if filename:
				googledriveservice = GoogleDriveService()
				fileresource = googledriveservice.getfile(filename)
				if fileresource:
					filecontents = googledriveservice.getfilecontents(fileresource, constants.GOOGLE_DRIVE_EMAIL_ATTACHMENT_PDF_CONTENT_TYPE)
					filetitle = googledriveservice.getfiletitle(fileresource)
					fileroot, ext = os.path.splitext(filetitle)
					filetitle = fileroot + '.pdf'
					if filecontents:
						attachment = mail.Attachment(filetitle, filecontents)
			try:
				message = mail.EmailMessage(sender=senderemailid, subject=subject)
				message.to = receiveremailid
				message.html = body
				if attachment:
					message.attachments = [attachment]
				message.send()
				logging.info('sent email senderemailid=' + str(senderemailid) \
					+ ', toaddress=' + str(receiveremailid) \
					+ ', with subject=' + str(subject))				
			except:
				logging.error('error sending email to ' + str(receiveremailid))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])
			try:
				p.emailupdated = True
				p.put()
			except:
				logging.error('error updating Email.emailupdated ' + str(receiveremailid))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])				
		return 0

class ForgotStudentIDService(object):
	def sendemail(self, emailid):
		fromid = constants.EMAIL_ID_PASSWORD_RECOVERY
		userservice = UserService()
		isvalidemailid = userservice.isvalidemailid(emailid)
		if isvalidemailid:
			user = userservice.getuserdetails(emailid)
			if user.emailid is None:
				user.emailid = ''
			if user.emailid2 is None:
				user.emailid2 = ''
			logging.info('got valid email id')
			emailservice = EmailService()
			emailbody = readtextfilecontents(constants.EMAIL_PASSWORD_RECOVERY_BODY_FILENAME)
			emailbody = emailbody.replace('$EMAILID$', user.emailid)
			emailbody = emailbody.replace('$EMAILID2$', user.emailid2)
			emailbody = emailbody.replace('$USERNAME$', user.username)
			emailbody = emailbody.replace('$STUDENTID$', user.studentid)
			emailservice.register(constants.EMAIL_TYPE_PASSWORD_RECOVERY, constants.EMAIL_ID_PASSWORD_RECOVERY, emailid, constants.EMAIL_PASSWORD_RECOVERY_SUBJECT, emailbody)
			return 2
		return 1

class MemcacheService(object):
	def hassession(self, uid):
		studentid = memcache.get(uid, namespace = 'Session')
		if studentid:
			return True
		return False
	def getstudentidforsession(self, uid):
		if uid:
			return memcache.get(uid, namespace = 'Session')
		return None
	def registersession(self, emailid, studentid):
		uid = str(uuid.uuid4())
		memcache.set(uid, studentid, namespace = 'Session')
		return uid
	def deregistersession(self, uid):
		if uid:
			return memcache.delete(uid, namespace = 'Session')
		return False

class StaffService(object):
	def getstaff(self):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_STAFF_WORKSHEET_KEY)
		staff = self._processstaffrows(rows)
		return staff
	def _processstaffrows(self, rows):
		staffs = []
		entries = rows.entry
		for entry in entries:
			staff = Staff()
			staff.staffid = processstr(entry, 'staffid')
			staff.staffname = processstr(entry, 'staffname')
			staff.staffrole = processstr(entry, 'staffrole')
			staff.staffdescription = processstr(entry, 'staffdescription')
			staff.staffemail = processstr(entry, 'staffemail')
			staffs.append(staff)
		return staffs	

class ChannelPartnersService(object):
	def getchannelpartners(self):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_CHANNELPARTNERS_WORKSHEET_KEY)
		channelpartners = self._processchannelpartnerrows(rows)
		return channelpartners
	def _processchannelpartnerrows(self, rows):
		channelpartners = []
		entries = rows.entry
		for entry in entries:
			channelpartner = ChannelPartner()
			channelpartner.channelpartnerid = processstr(entry, 'channelpartnerid')
			channelpartner.channelpartnercity = processstr(entry, 'channelpartnercity')
			channelpartner.channelpartnerstate = processstr(entry, 'channelpartnerstate')
			channelpartner.channelpartnername = processstr(entry, 'channelpartnername')
			channelpartner.channelpartnerwebsite = processstr(entry, 'channelpartnerwebsite')
			channelpartner.channelpartnerregsite = processstr(entry, 'channelpartnerregsite')
			channelpartners.append(channelpartner)
		return channelpartners	

class CoursesService(object):
	def getcourse(self, courseid):
		courses = self.listcourses()
		for course in courses:
			if course.courseid == courseid:
				return course
		return None
	def getcoursecontents(self, courseid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSECONTENTS_WORKSHEET_KEY)
		coursecontents = self._processcoursecontentrows(rows)
		results = []
		for coursecontent in coursecontents:
			if coursecontent.courseid == courseid:
				results.append(coursecontent)
		return results
	def getcoursehandouts(self, courseid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSEHANDOUTS_WORKSHEET_KEY)
		coursehandouts = self._processcoursehandoutrows(rows)
		results = []
		for coursehandout in coursehandouts:
			if coursehandout.courseid == courseid:
				results.append(coursehandout)
		return coursehandouts
	def getcoursehomeworks(self, courseid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSEHOMEWORKS_WORKSHEET_KEY)
		coursehomeworks = self._processcoursehomeworkrows(rows)
		results = []
		for coursehomework in coursehomeworks:
			if coursehomework.courseid == courseid:
				results.append(coursehomework)
		return coursehomeworks
	def getcoursevideos(self, courseid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSEVIDEOS_WORKSHEET_KEY)
		coursevideos = self._processcoursevideorows(rows)
		results = []
		for coursevideo in coursevideos:
			if coursevideo.courseid == courseid:
				results.append(coursevideo)
		return coursevideos
	def getcoursestarterpacks(self, courseid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSESTARTERPACKS_WORKSHEET_KEY)
		coursestarterpacks = self._processcoursestarterpackrows(rows)
		results = []
		for coursestarterpack in coursestarterpacks:
			if coursestarterpack.courseid == courseid:
				results.append(coursestarterpack)
		return coursestarterpacks
	def getcoursequizzes(self, courseid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSEQUIZS_WORKSHEET_KEY)
		coursequizs = self._processcoursequizrows(rows)
		results = []
		for coursequiz in coursequizs:
			if coursequiz.courseid == courseid:
				results.append(coursequiz)
		return coursequizs
	def listcourses(self):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSES_WORKSHEET_KEY)
		courses = self._processcourserows(rows)
		return courses
	def listupcomingcourses(self):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSES_WORKSHEET_KEY)
		courses = self._processcourserows(rows)
		results = []
		present = datetime.now()
		for course in courses:
			coursestartdate = parser.parse(course.coursestartdate)
			delta = coursestartdate - present
			deltadays = delta.days
			if deltadays <= 28 and deltadays >= -7:
				results.append(course)
		return results
	def listusercourses(self, studentid):
		courses = self.listcourses()
		return usercourses
	def _processcoursestarterpackrows(self, rows):
		coursestarterpacks = []
		entries = rows.entry
		for entry in entries:
			coursestarterpack = CourseStarterPack()
			coursestarterpack.courseid = processstr(entry, 'courseid')
			coursestarterpack.coursecontentid = processstr(entry, 'coursecontentid')
			coursestarterpack.coursestarterpackid = processstr(entry, 'coursestarterpackid')
			coursestarterpack.coursestarterpackname = processstr(entry, 'coursestarterpackname')
			coursestarterpack.coursestarterpackdescription = processtext(entry, 'coursestarterpackdescription')
			coursestarterpack.coursestarterpackdownloadurl = processstr(entry, 'coursestarterpackdownloadurl')
			coursestarterpacks.append(coursestarterpack)
		return coursestarterpacks
	def _processcoursevideorows(self, rows):
		coursevideos = []
		entries = rows.entry
		for entry in entries:
			coursevideo = CourseVideo()
			coursevideo.courseid = processstr(entry, 'courseid')
			coursevideo.coursecontentid = processstr(entry, 'coursecontentid')
			coursevideo.coursevideoid = processstr(entry, 'coursevideoid')
			coursevideo.coursevideoname = processstr(entry, 'coursevideoname')
			coursevideo.coursevideodescription = processtext(entry, 'coursevideodescription')
			coursevideo.coursevideodownloadurl = processstr(entry, 'coursevideodownloadurl')
			coursevideos.append(coursevideo)
		return coursevideos
	def _processcoursehomeworkrows(self, rows):
		coursehomeworks = []
		entries = rows.entry
		for entry in entries:
			coursehomework = CourseHomework()
			coursehomework.courseid = processstr(entry, 'courseid')
			coursehomework.coursecontentid = processstr(entry, 'coursecontentid')
			coursehomework.coursehomeworkid = processstr(entry, 'coursehomeworkid')
			coursehomework.coursehomeworkname = processstr(entry, 'coursehomeworkname')
			coursehomework.coursehomeworkdescription = processtext(entry, 'coursehomeworkdescription')
			coursehomework.coursehomeworkdownloadurl = processstr(entry, 'coursehomeworkdownloadurl')
			coursehomeworks.append(coursehomework)
		return coursehomeworks
	def _processcoursehandoutrows(self, rows):
		coursehandouts = []
		entries = rows.entry
		for entry in entries:
			coursehandout = CourseHandout()
			coursehandout.courseid = processstr(entry, 'courseid')
			coursehandout.coursecontentid = processstr(entry, 'coursecontentid')
			coursehandout.coursehandoutid = processstr(entry, 'coursehandoutid')
			coursehandout.coursehandoutname = processstr(entry, 'coursehandoutname')
			coursehandout.coursehandoutdescription = processtext(entry, 'coursehandoutdescription')
			coursehandout.coursehandoutdownloadurl = processstr(entry, 'coursehandoutdownloadurl')
			coursehandouts.append(coursehandout)
		return coursehandouts
	def _processcoursequizrows(self, rows):
		coursequizs = []
		entries = rows.entry
		for entry in entries:
			coursequiz = CourseQuiz()
			coursequiz.courseid = processstr(entry, 'courseid')
			coursequiz.coursecontentid = processstr(entry, 'coursecontentid')
			coursequiz.coursequizid = processstr(entry, 'coursequizid')
			coursequiz.coursequizname = processstr(entry, 'coursequizname')
			coursequiz.coursequizdescription = processtext(entry, 'coursequizdescription')
			coursequiz.coursequizdownloadurl = processstr(entry, 'coursequizdownloadurl')
			coursequizs.append(coursequiz)
		return coursequizs
	def _processcoursecontentrows(self, rows):
		coursecontents = []
		entries = rows.entry
		for entry in entries:
			coursecontent = CourseContent()
			coursecontent.courseid = processstr(entry, 'courseid')
			coursecontent.coursecontentid = processstr(entry, 'coursecontentid')
			coursecontent.coursecontentname = processstr(entry, 'coursecontentname')
			coursecontent.coursecontentdescription = processstr(entry, 'coursecontentdescription')
			coursecontent.coursecontenturl = '/coursecontent?c='+str(coursecontent.courseid)+'&cc='+str(coursecontent.coursecontentid)
			coursecontents.append(coursecontent)
		return coursecontents
	def _processcourserows(self, rows):
		courses = []
		entries = rows.entry
		for entry in entries:
			course = Course()
			course.courseid = processstr(entry, 'courseid')
			course.coursetag = processstr(entry, 'coursetag')
			course.coursename = processstr(entry, 'coursename')
			course.coursedescription = processstr(entry, 'coursedescription')
			course.courseyear = processint(entry, 'courseyear')
			course.coursestartdate = processstr(entry, 'coursestartdate')
			course.courseenddate = processstr(entry, 'courseenddate')
			course.coursesession = processstr(entry, 'coursesession')
			course.coursepartner = processstr(entry, 'coursepartner')
			course.courseminage = processint(entry, 'courseminage')
			course.coursemaxage = processint(entry, 'coursemaxage')
			course.coursenumclasses = processint(entry, 'coursenumclasses')
			course.courseclassdurationmins = processint(entry, 'courseclassdurationmins')
			course.courseisonline = processboolean(entry, 'courseisonline')
			courses.append(course)
		return courses
	def _processstr(self, entry, field):
		text = entry.custom[field].text
		return text
	def _processint(self, entry, field):
		text = processstr(entry, field)
		if text:
			return int(text)
		return 0
	def _processboolean(self, entry, field):
		int_ = processint(entry, field)
		return int_ != 0


class UserService(object):
	def isvalidemailid(self, emailid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_STUDENTSMASTER_WORKSHEET_KEY)
		entries = rows.entry
		for entry in entries:
			entryemailid = processstr(entry, 'studentemail')
			if entryemailid == emailid:
				return True
			entryemailid = processstr(entry, 'studentemail2')
			if entryemailid == emailid:
				return True
		return False
	def getuserdetails(self, emailid):
		googlespreadsheetservice = GoogleSpreadsheetService()
		rows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_STUDENTSMASTER_WORKSHEET_KEY)
		entries = rows.entry
		user = User()
		for entry in entries:
			isuser = False
			entryemailid = processstr(entry, 'studentemail')
			if entryemailid == emailid:
				isuser = True
			entryemailid2 = processstr(entry, 'studentemail2')
			if entryemailid2 == emailid:
				isuser = True
			if isuser:
				user.username = processstr(entry, 'student')
				user.studentid = processstr(entry, 'studentid')
				user.emailid = entryemailid
				user.emailid2 = entryemailid2
				break
		return user
	def isuserindb(self, emailid, studentid):
		user = self.getuserdetails(emailid)
		if emailid is not None and studentid is not None:
			if studentid == user.studentid:
				if emailid == user.emailid or emailid == user.emailid2:					
					return True
		return False
	def hassession(self, uid):
		if uid:
			cacheservice = MemcacheService()
			return cacheservice.hassession(uid)
		return False
	def deregistersession(self, uid):
		if uid:
			cacheservice = MemcacheService()
			return cacheservice.deregistersession(uid)
		return False
	def registersession(self, emailid, studentid):
		if emailid and studentid:
			isuserindb = self.isuserindb(emailid, studentid)
			if isuserindb:
				cacheservice = MemcacheService()
				return cacheservice.registersession(emailid, studentid)
		return None
	def getstudentidforsession(self, uid):
		if uid:
			cacheservice = MemcacheService()
			return cacheservice.getstudentidforsession(uid)

class SignUpService(object):
	def signup(self, emailid, ipaddress):
		query = SignUp.all()
		query.filter("emailid = ", emailid)
		p = None
		for p in query.run(limit=1):
			break
		try:
			if not p:
				p = SignUp()
				p.counter = 0
				p.emailid = emailid
			p.counter += 1
			p.ipaddress = ipaddress
			p.ipupdated = False
			p.put()
			filename = constants.GOOGLE_DRIVE_EMAIL_ATTACHMENT_KEY
			attachment = mail.Attachment(filename, None)			
			emailservice = EmailService()	
			emailservice.register(constants.EMAIL_TYPE_SIGNUP, constants.EMAIL_ID_SIGNUP, emailid, constants.EMAIL_SIGNUP_SUBJECT, readtextfilecontents(constants.EMAIL_SIGNUP_BODY_FILENAME), attachment)
			return 1
		except Exception as e:
			logging.error("error signing up " + str(emailid))
			sys_err = sys.exc_info()
			logging.error(sys_err[1])
		return 0

class ValidationService(object):
	def isvalidemail(self, emailid):
		isvalid = False
		if emailid:
			isvalid = validate_email(emailid)
		return isvalid

