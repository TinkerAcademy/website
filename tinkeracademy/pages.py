import os
import urllib
import jinja2
import logging
import time
import webapp2
import constants

from pageutils import buildheadertemplatevalues
from pageutils import buildallcoursestemplatevalues
from pageutils import buildmycoursestemplatevalues
from pageutils import buildcoursetemplatevalues
from pageutils import buildcoursecontenttemplatevalues
from pageutils import buildchannelpartnertemplatevalues
from pageutils import buildstafftemplatevalues
from pageutils import extractkeyfromrequest
from pageutils import isinsession
from pageutils import issessionrequest
from pageutils import isadminuser
from pageutils import createloginurl
from pageutils import attemptlogin

from environment import JINJA_ENVIRONMENT

from services import UserService
from services import CoursesService
from services import SignUpService
from services import ForgotStudentIDService
from services import ValidationService
from services import ChannelPartnersService
from services import StaffService

class AboutPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		staffservice = StaffService()
		staff = staffservice.getstaff()
		channelpartnersservice = ChannelPartnersService()
		channelpartners = channelpartnersservice.getchannelpartners()
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		staff_template_values = buildstafftemplatevalues(insession, staff)
		template_values.update(staff_template_values)
		channelpartner_template_values = buildchannelpartnertemplatevalues(insession, channelpartners)
		template_values.update(channelpartner_template_values)
		logging.info('template_values='+str(template_values))
		template = JINJA_ENVIRONMENT.get_template('about.html')
		self.response.write(template.render(template_values))

class AllCoursesPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		coursesservice = CoursesService()
		courses = coursesservice.listcourses()
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		course_template_values = buildallcoursestemplatevalues(insession, courses)
		template_values.update(course_template_values)
		# logging.info('template_values='+str(template_values))
		template = JINJA_ENVIRONMENT.get_template('allcourses.html')
		self.response.write(template.render(template_values))

class CoursePage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		courseid = extractkeyfromrequest(self.request, 'c')
		coursesservice = CoursesService()
		course = coursesservice.getcourse(courseid)	
		coursecontents = coursesservice.getcoursecontents(courseid)
		# coursehandouts = coursesservice.getcoursehandouts(courseid)
		# coursehomeworks = coursesservice.getcoursehomeworks(courseid)
		# coursevideos = coursesservice.getcoursevideos(courseid)
		# coursestarterpacks = coursesservice.getcoursestarterpacks(courseid)		
		# coursequizzes = coursesservice.getcoursequizzes(courseid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		course_template_values = buildcoursetemplatevalues(insession, course, coursecontents)
		template_values.update(course_template_values)		
		logging.info('template_values='+str(template_values))
		template = JINJA_ENVIRONMENT.get_template('course.html')
		self.response.write(template.render(template_values))			

class CourseContentsPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		courseid = extractkeyfromrequest(self.request, 'c')
		coursecontentid = extractkeyfromrequest(self.request, 'cc')
		coursesservice = CoursesService()
		course = coursesservice.getcourse(courseid)	
		coursecontents = coursesservice.getcoursecontents(courseid)
		coursehandouts = coursesservice.getcoursehandouts(courseid)
		coursehomeworks = coursesservice.getcoursehomeworks(courseid)
		coursevideos = coursesservice.getcoursevideos(courseid)
		coursestarterpacks = coursesservice.getcoursestarterpacks(courseid)		
		coursequizzes = coursesservice.getcoursequizzes(courseid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		coursecontent_template_values = buildcoursecontenttemplatevalues(insession, courseid, coursecontentid, course, coursecontents, coursehandouts, coursehomeworks, coursevideos, coursestarterpacks, coursequizzes)
		template_values.update(coursecontent_template_values)		
		logging.info('template_values='+str(template_values))
		template = JINJA_ENVIRONMENT.get_template('coursecontent.html')
		self.response.write(template.render(template_values))			

class ForgotPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		emailid = extractkeyfromrequest(self.request, 'e')
		if emailid is None:
			emailid = ''
		returnvalue = extractkeyfromrequest(self.request, 'r')
		if returnvalue is None:
			returnvalue = 0
		else:
			returnvalue = int(returnvalue)
		template_values = {	
			'emailid' : emailid,
			'returnvalue': returnvalue,
		}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		template = JINJA_ENVIRONMENT.get_template('forgot.html')
		self.response.write(template.render(template_values))
	def post(self):
		emailid = self.request.get('emailid')
		forgotservice = ForgotStudentIDService()
		returnvalue = forgotservice.sendemail(emailid)
		self.redirect('/forgot?e='+str(emailid)+'&r='+str(returnvalue))

class MyCoursesPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		coursesservice = CoursesService()
		userservice = UserService()
		studentid = userservice.getstudentidforsession(uid)
		usercourses = coursesservice.listusercourses(studentid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		course_template_values = buildmycoursestemplatevalues(insession, uid, usercourses)
		template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('mycourses.html')
		self.response.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		coursesservice = CoursesService()
		courses = coursesservice.listupcomingcourses()
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		course_template_values = buildallcoursestemplatevalues(insession, courses)
		template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class SignInPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		emailid = extractkeyfromrequest(self.request, 'e')
		iserror = extractkeyfromrequest(self.request, 'x') != None
		errormsg = ''
		if iserror:
			errormsg = 'Unable to signin'
		if emailid is None:
			emailid = ''
		template_values = {	
			'errormsg': errormsg,
			'emailid' : emailid,
			'forgoturl' : '/forgot?e='+str(emailid),
			'forgoturllinktext' : 'Forgot Student ID?' 
		}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		template = JINJA_ENVIRONMENT.get_template('signin.html')
		self.response.write(template.render(template_values))
	def post(self):
		emailid = self.request.get('emailid')
		uid, insession = attemptlogin(self.request)
		if uid:
			self.redirect('/?u=' + str(uid))
		else:
			self.redirect('/signin?e='+str(emailid)+'&x=1')

class SignOutPage(webapp2.RequestHandler):
	def get(self):
		userservice = UserService()
		uid = extractkeyfromrequest(self.request, 'u')
		if not userservice.deregistersession(uid):
			logging.error('error deregistering ' + str(uid))
		self.redirect('/')

class SignUpPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		emailid = extractkeyfromrequest(self.request, 'e')
		if emailid is None:
			emailid = ''
		zipcode = extractkeyfromrequest(self.request, 'z')
		if zipcode is None:
			zipcode = ''
		returnvalue = extractkeyfromrequest(self.request, 'r')	
		if returnvalue is None:
			returnvalue = 0		
		returnvalue = int(returnvalue)
		template_values = {
			'emailid': emailid,
			'zipcode': zipcode,
			'returnvalue': returnvalue,			
		}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)		
		channelpartnersservice = ChannelPartnersService()
		channelpartners = channelpartnersservice.getchannelpartners()
		channelpartner_template_values = buildchannelpartnertemplatevalues(insession, channelpartners)
		template_values.update(channelpartner_template_values)
		template = JINJA_ENVIRONMENT.get_template('signup.html')
		self.response.write(template.render(template_values))
	def post(self):
		emailid = self.request.get('emailid')
		if emailid:
			emailid = emailid.strip()
		validationservice = ValidationService()
		isvalidemail = validationservice.isvalidemail(emailid)
		if not isvalidemail:
			returnvalue = 0			
			if not isvalidemail:
				returnvalue |= constants.INPUT_INVALID_EMAILID
			q = 'r='+str(returnvalue)
			if emailid:
				q += '&'
				q += 'e='+str(emailid)
			self.redirect('/signup?'+q)
		else:
			signupservice = SignUpService()
			ipaddress = self.request.remote_addr
			returnvalue = signupservice.signup(emailid, ipaddress)		
			self.redirect('/signupstatus?r='+str(returnvalue)+'&e='+str(emailid))

class SignUpStatusPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		returnvalue = extractkeyfromrequest(self.request, 'r')
		hasreturnvalue = True
		if returnvalue is None:
			hasreturnvalue = False		
		emailid = extractkeyfromrequest(self.request, 'e')	
		template_values = {	
			'emailid' : emailid,
			'hasreturnvalue': hasreturnvalue,
		}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)		
		template = JINJA_ENVIRONMENT.get_template('signupstatus.html')
		self.response.write(template.render(template_values))

