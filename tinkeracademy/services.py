import logging
import os
import sys
import uuid
import constants
import json
import hashlib

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
				   OtherCities, \
				   TinkerAcademyUser				  

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
			# if filename:
			# 	googledriveservice = GoogleDriveService()
			# 	fileresource = googledriveservice.getfile(filename)
			# 	if fileresource:
			# 		filecontents = googledriveservice.getfilecontents(fileresource, constants.GOOGLE_DRIVE_EMAIL_ATTACHMENT_PDF_CONTENT_TYPE)
			# 		filetitle = googledriveservice.getfiletitle(fileresource)
			# 		fileroot, ext = os.path.splitext(filetitle)
			# 		filetitle = fileroot + '.pdf'
			# 		if filecontents:
			# 			attachment = mail.Attachment(filetitle, filecontents)
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
	def buildstorekey(self, uid):
		store_key = uid + "keys"
		return store_key		
	def getstore(self, uid):
		store_key = self.buildstorekey(uid)
		store = memcache.get(store_key)
		if not store:
			store = {}
		memcache.set(store_key, store)
		return store		
	def putinsession(self, uid, key, value):
		store = self.getstore(uid)
		store[key] = value
		store_key = self.buildstorekey(uid)
		memcache.set(store_key, store)
	def getfromsession(self, uid, key):
		store = self.getstore(uid)
		if store and key in store:
			return store[key]
		return None
	def clearfromsession(self, uid, key):
		store = self.getstore(uid)
		if key in store:
			store[key] = None		
		store_key = self.buildstorekey(uid)
		memcache.set(store_key, store)
	def getsessionuser(self, uid):
		return memcache.get(uid, namespace = 'Session')
	def setsessionuser(self, uid, user):
		memcache.set(uid, user, namespace = 'Session')
	#@deprecated
	def hassession(self, uid):
		studentid = memcache.get(uid, namespace = 'Session')
		if studentid:
			return True
		return False
	#@deprecated
	def getstudentidforsession(self, uid):
		if uid:
			return memcache.get(uid, namespace = 'Session')
		return None
	#@deprecated
	def getemailidforsession(self, uid):
		if uid:
			return memcache.get(uid, namespace = 'SessionEmail')
		return None
	#@deprecated
	def registersession(self, emailid, studentid):
		uid = str(uuid.uuid4())
		memcache.set(uid, studentid, namespace = 'Session')
		memcache.set(uid, emailid, namespace = 'SessionEmail')
		return uid
	#@deprecated
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
	def listusercourses(self, emailid):
		courses = self.listcourses()
		userservice = UserService()
		user = userservice.getuserdetails(emailid)
		logging.info('user.courseid1='+str(user.courseid1))
		usercourses = []
		for course in courses:
			logging.info('course.courseid='+str(course.courseid))
			if course.courseid == user.courseid1:
				usercourses.append(course)
			elif course.courseid == user.courseid2:
				usercourses.append(course)
			elif course.courseid == user.courseid3:
				usercourses.append(course)
			elif course.courseid == user.courseid4:
				usercourses.append(course)
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
			course.coursename = processstr(entry, 'coursename')
			course.coursedescription = processstr(entry, 'coursedescription')
			course.coursedetails = processstr(entry, 'coursedetails')
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
				user.courseid1 = processstr(entry, 'courseid1')
				user.courseid2 = processstr(entry, 'courseid2')
				user.courseid3 = processstr(entry, 'courseid3')
				user.courseid4 = processstr(entry, 'courseid4')
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
		return None
	def getemailidforsession(self, uid):
		if uid:
			cacheservice = MemcacheService()
			return cacheservice.getemailidforsession(uid)
		return None

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

class TinkerAcademyUserService(object):
	def findusersinclaz(self, user):
		query = TinkerAcademyUser.all()
		query.filter("claz = ", user.claz)
		users = []
		for p in query.run():
			users.append(p)
		return users
	def finduserbystudentid(self, studentid):
		query = TinkerAcademyUser.all()
		query.filter("studentid = ", studentid)
		p = None
		for p in query.run(limit=1):
			break
		return p
	def login(self, user):
		sessionid = self.createsessionid(user.studentid)
		cacheservice = MemcacheService()
		cacheservice.setsessionuser(sessionid, user)
		return sessionid
	def anonlogin(self):
		sessionid = None
		sessionid = self.createanonsessionid()
		if sessionid:
			user = TinkerAcademyUser()
			cacheservice = MemcacheService()
			cacheservice.setsessionuser(sessionid, user)
		return sessionid
	def register(self, studentname, emailid, claz, favmod, zipcode):
		query = TinkerAcademyUser.all()
		query.filter("emailid1 = ", emailid)
		p = None
		for p in query.run(limit=1):
			break
		if not p or p.claz != claz:
			p = TinkerAcademyUser()
			p.emailid1 = emailid
			studentid = 2015000
			query = TinkerAcademyUser.all()
			for e in query.run():
				if studentid < e.studentid:
					studentid = e.studentid
			studentid = studentid + 1;
			p.studentid = studentid
			p.studentname = studentname
			p.emailid2 = None
			p.emailid3 = None
			p.scholarship = False
			p.userstatus = 1
			p.stripe_customer_id = None
			p.claz = claz
		if favmod:
			p.favmod = favmod
		if zipcode:
			p.zipcode = zipcode
		p.put()
		# isfutureclaz = claz == 'Future Sessions'
		# isrecservicesclaz = claz == 'Sep 2015 - Nov 2015' or claz == 'Sep 2015 - Nov 2015 (AP)'
		# if not isfutureclaz and not isrecservicesclaz:
		# 	emailservice = EmailService()
		# 	emailbody = readtextfilecontents(constants.EMAIL_TA_REGISTER_FILENAME)
		# 	emailbody = emailbody.replace('$EMAILID$', emailid)
		# 	emailbody = emailbody.replace('$STUDENTNAME$', studentname)
		# 	emailbody = emailbody.replace('$STUDENTID$', str(p.studentid))
		# 	emailservice.register(constants.EMAIL_TA_REGISTER_TYPE, constants.EMAIL_TA_REGISTER_ID, emailid, constants.EMAIL_TA_REGISTER_SIGNUP_SUBJECT, emailbody)
		# 	emailservice.sendnext()
		return self.login(p)
	def subscribe(self, emailid):
		query = TinkerAcademyUser.all()
		query.filter("emailid1 = ", emailid)
		p = None
		for p in query.run(limit=1):
			break
		if not p:
			p = TinkerAcademyUser()
			p.emailid1 = emailid
			studentid = 2015000
			query = TinkerAcademyUser.all()
			for e in query.run():
				if studentid < e.studentid:
					studentid = e.studentid
			studentid = studentid + 1;
			p.studentid = studentid
			p.studentname = None
			p.emailid2 = None
			p.emailid3 = None
			p.scholarship = False
			p.userstatus = 1
			p.stripe_customer_id = None
			p.claz = None
		p.put()
		return self.login(p)
	def createanonsessionid(self):
		return hashlib.sha1('anon').hexdigest()
	def createsessionid(self, studentid):
		return hashlib.sha1(str(studentid)).hexdigest()

class ValidationService(object):
	def isvalidemail(self, emailid):
		isvalid = False
		if emailid:
			isvalid = validate_email(emailid)
		return isvalid

