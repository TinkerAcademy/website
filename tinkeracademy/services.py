import logging
import os
import sys
import uuid
import constants
import json

from datetime import datetime
from dateutil import parser

from google.appengine.api import memcache
from google.appengine.api import mail

from validate_email import validate_email
from validate_zipcode import validate_zipcode

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
				   Email

class DatabaseService(object):
	def getcourses(self):
		# googledriveservice = GoogleDriveService()
		# dbfile = googledriveservice.getfile(constants.GOOGLE_DRIVE_SPREADSHEET_TITLE)		
		# logging.info('dbfile='+str(dbfile))
		googlespreadsheetservice = GoogleSpreadsheetService()
		# coursesworksheet = googlespreadsheetservice.getworksheets(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSES_WORKSHEET_KEY)
		# logging.info('DatabaseService.updatecourses coursesworksheet='+str(coursesworksheet))
		coursesrows = googlespreadsheetservice.getrows(constants.GOOGLE_DRIVE_SPREADSHEET_KEY, constants.GOOGLE_DRIVE_COURSES_WORKSHEET_KEY)
		logging.info('DatabaseService.updatecourses courses rows='+str(coursesrows))

class EmailService(object):
	def register(self, emailtype, senderid, receiveremailid, subject, body, attachment=None):
		senderemailid = str(fromid) + '@' + constants.EMAIL_DOMAIN_APPSPOT
		email = Email()
		email.senderemailid = senderemailid
		email.receiveremailid = receiveremailid
		email.typeid = emailtype
		email.counter = 0
		email.subject = Text(subject)
		email.body = Text(body)
		if attachment:
			email.filename = attachment.filename
		email.put()
		return 1
	def sendnext(self):
		query = Email.all()
		query.filter("counter = ", 0)
		p = None
		for p in query.run(limit=1):
			senderemailid = str(p.senderemailid)
			receiveremailid = str(p.receiveremailid)
			subject = str(p.subject)
			body = str(p.body)
			filename = str(p.filename)
			if filename:
				pass
			try:
				mail.send_mail(fromaddress, toaddress, subject, body)
				return 1
			except:
				logging.error("error sending email to " + str(toaddress))
				sys_err = sys.exc_info()
				logging.error(sys_err[1])
		return 0

class ForgotStudentIDService(object):
	def sendemail(self, emailid):
		fromid = constants.EMAIL_ID_PASSWORD_RECOVERY
		emailservice = EmailService()
		return emailservice.send(fromid, emailid, 'Password Recovery', 'Your Student ID is ######')

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
	def getcourses(self):
		courses = memcache.get('courses', namespace = 'Courses')
		return courses
	def setcourses(self, courses):
		memcache.set('courses', courses, namespace = 'Courses')
	def getusercourses(self, studentid):
		courses = []
		if studentid:
			courses = memcache.get(studentid, namespace = 'UserCourses')
		return courses
	def setusercourses(self, studentid, courses):
		if studentid:
			memcache.set(studentid, courses, namespace = 'UserCourses')

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
		cacheservice = MemcacheService()
		courses = self.listcourses()
		usercourses = cacheservice.getusercourses(studentid)
		if (not usercourses) or len(usercourses) == 0:
			usercourses = []			
			query = UserCourse.all()
			query.filter("studentid = ", studentid)
			for p in query.run(limit=100):
				usercourses.append(p)
			cacheservice.setusercourses(studentid, usercourses)
		return usercourses
	def _processcoursestarterpackrows(self, rows):
		coursestarterpacks = []
		entries = rows.entry
		for entry in entries:
			coursestarterpack = CourseStarterPack()
			coursestarterpack.courseid = self._processstr(entry, 'courseid')
			coursestarterpack.coursecontentid = self._processstr(entry, 'coursecontentid')
			coursestarterpack.coursestarterpackid = self._processstr(entry, 'coursestarterpackid')
			coursestarterpack.coursestarterpackname = self._processstr(entry, 'coursestarterpackname')
			coursestarterpacks.append(coursestarterpack)
		return coursestarterpacks
	def _processcoursevideorows(self, rows):
		coursevideos = []
		entries = rows.entry
		for entry in entries:
			coursevideo = CourseVideo()
			coursevideo.courseid = self._processstr(entry, 'courseid')
			coursevideo.coursecontentid = self._processstr(entry, 'coursecontentid')
			coursevideo.coursevideoid = self._processstr(entry, 'coursevideoid')
			coursevideo.coursevideoname = self._processstr(entry, 'coursevideoname')
			coursevideos.append(coursevideo)
		return coursevideos
	def _processcoursehomeworkrows(self, rows):
		coursehomeworks = []
		entries = rows.entry
		for entry in entries:
			coursehomework = CourseHomework()
			coursehomework.courseid = self._processstr(entry, 'courseid')
			coursehomework.coursecontentid = self._processstr(entry, 'coursecontentid')
			coursehomework.coursehomeworkid = self._processstr(entry, 'coursehomeworkid')
			coursehomework.coursehomeworkname = self._processstr(entry, 'coursehomeworkname')
			coursehomeworks.append(coursehomework)
		return coursehomeworks
	def _processcoursehandoutrows(self, rows):
		coursehandouts = []
		entries = rows.entry
		for entry in entries:
			coursehandout = CourseHandout()
			coursehandout.courseid = self._processstr(entry, 'courseid')
			coursehandout.coursecontentid = self._processstr(entry, 'coursecontentid')
			coursehandout.coursehandoutid = self._processstr(entry, 'coursehandoutid')
			coursehandout.coursehandoutname = self._processstr(entry, 'coursehandoutname')
			coursehandouts.append(coursehandout)
		return coursehandouts
	def _processcoursequizrows(self, rows):
		coursequizs = []
		entries = rows.entry
		for entry in entries:
			coursequiz = CourseQuiz()
			coursequiz.courseid = self._processstr(entry, 'courseid')
			coursequiz.coursecontentid = self._processstr(entry, 'coursecontentid')
			coursequiz.coursequizid = self._processstr(entry, 'coursequizid')
			coursequiz.coursequizname = self._processstr(entry, 'coursequizname')
			coursequizs.append(coursequiz)
		return coursequizs
	def _processcoursecontentrows(self, rows):
		coursecontents = []
		entries = rows.entry
		for entry in entries:
			coursecontent = CourseContent()
			coursecontent.courseid = self._processstr(entry, 'courseid')
			coursecontent.coursecontentid = self._processstr(entry, 'coursecontentid')
			coursecontent.coursecontentname = self._processstr(entry, 'coursecontentname')
			coursecontent.coursecontentdescription = self._processstr(entry, 'coursecontentdescription')
			coursecontents.append(coursecontent)
		return coursecontents
	def _processcourserows(self, rows):
		courses = []
		entries = rows.entry
		for entry in entries:
			course = Course()
			course.courseid = self._processstr(entry, 'courseid')
			course.coursetag = self._processstr(entry, 'coursetag')
			course.coursename = self._processstr(entry, 'coursename')
			course.coursedescription = self._processstr(entry, 'coursedescription')
			course.courseyear = self._processint(entry, 'courseyear')
			course.coursestartdate = self._processstr(entry, 'coursestartdate')
			course.courseenddate = self._processstr(entry, 'courseenddate')
			course.coursesession = self._processstr(entry, 'coursesession')
			course.coursepartner = self._processstr(entry, 'coursepartner')
			course.courseminage = self._processint(entry, 'courseminage')
			course.coursemaxage = self._processint(entry, 'coursemaxage')
			course.coursenumclasses = self._processint(entry, 'coursenumclasses')
			course.courseclassdurationmins = self._processint(entry, 'courseclassdurationmins')
			course.courseisonline = self._processboolean(entry, 'courseisonline')
			courses.append(course)
		return courses
	def _processstr(self, entry, field):
		text = entry.custom[field].text
		return text
	def _processint(self, entry, field):
		text = self._processstr(entry, field)
		if text:
			return int(text)
		return 0
	def _processboolean(self, entry, field):
		int_ = self._processint(entry, field)
		return int_ != 0


class UserService(object):
	def isuserindb(self, emailid, studentid):
		if emailid and studentid:
			query = User.all()
			query.filter("emailid = ", emailid)
			query.filter("studentid = ", studentid)
			for p in query.run(limit=1):
				return True
		#FIXME: return False
		return True
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
	def signup(self, emailid, zipcode):
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
				p.zipcode = zipcode
			p.counter += 1
			p.put()
			emailservice = EmailService()	
			emailservice.register(constants.EMAIL_ID_SIGNUP, emailid, 'You have been signed up', 'You have been signed up')
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
	def isvalidzipcode(self, zipcode):
		isvalid = False
		if zipcode:
			isvalid = validate_zipcode(zipcode)
		return isvalid

