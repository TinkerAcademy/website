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
from pageutils import extractkeyfromrequest
from pageutils import isinsession
from pageutils import issessionrequest
from pageutils import isadminuser
from pageutils import createloginurl

from environment import JINJA_ENVIRONMENT

from services import UserService
from services import CoursesService
from services import SignUpService
from services import ForgotStudentIDService
from services import ValidationService

class AboutPage(webapp2.RequestHandler):
	def get(self):
		uid = extractkeyfromrequest(self.request, 'u')
		insession = isinsession(uid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		template = JINJA_ENVIRONMENT.get_template('about.html')
		self.response.write(template.render(template_values))

class AllCoursesPage(webapp2.RequestHandler):
	def get(self):
		uid = extractkeyfromrequest(self.request, 'u')
		insession = isinsession(uid)
		coursesservice = CoursesService()
		courses = coursesservice.listcourses()
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		course_template_values = buildallcoursestemplatevalues(insession, courses)
		template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('allcourses.html')
		self.response.write(template.render(template_values))

class ForgotPage(webapp2.RequestHandler):
	def get(self):
		uid = extractkeyfromrequest(self.request, 'u')
		insession = isinsession(uid)
		emailid = extractkeyfromrequest(self.request, 'e')
		if emailid is None:
			emailid = ''
		returnvalue = extractkeyfromrequest(self.request, 'r')
		hasreturnvalue = True
		if returnvalue is None:
			hasreturnvalue = False	
		template_values = {	
			'emailid' : emailid,
			'hasreturnvalue': hasreturnvalue,
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
		uid = extractkeyfromrequest(self.request, 'u')
		insession = isinsession(uid)
		coursesservice = CoursesService()
		userservice = UserService()
		studentid = userservice.getstudentidforsession(uid)
		usercourses = coursesservice.listusercourses(uid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		course_template_values = buildmycoursestemplatevalues(insession, uid, usercourses)
		template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('mycourses.html')
		self.response.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):
	def get(self):
		uid = extractkeyfromrequest(self.request, 'u')
		insession = isinsession(uid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class SignInPage(webapp2.RequestHandler):
	def get(self):
		uid = extractkeyfromrequest(self.request, 'u')
		insession = isinsession(uid)
		emailid = extractkeyfromrequest(self.request, 'e')
		if emailid is None:
			emailid = ''
		template_values = {	
			'emailid' : emailid,
			'forgoturl' : '/forgot?e='+str(emailid),
			'forgoturllinktext' : 'Forgot Student ID' 
		}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		template = JINJA_ENVIRONMENT.get_template('signin.html')
		self.response.write(template.render(template_values))
	def post(self):
		emailid = self.request.get('emailid')
		studentid = self.request.get('studentid')
		userservice = UserService()
		uid = userservice.registersession(emailid, studentid)
		if uid:
			self.redirect('/?u=' + str(uid))
		else:
			self.redirect('/signin?e='+str(emailid))

class SignOutPage(webapp2.RequestHandler):
	def get(self):
		userservice = UserService()
		uid = extractkeyfromrequest(self.request, 'u')
		if not userservice.deregistersession(uid):
			logging.error('error deregistering ' + str(uid))
		self.redirect('/')

class SignUpPage(webapp2.RequestHandler):
	def get(self):
		uid =extractkeyfromrequest(self.request, 'u')
		insession = issessionrequest(self.request)
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
		template = JINJA_ENVIRONMENT.get_template('signup.html')
		self.response.write(template.render(template_values))
	def post(self):
		emailid = self.request.get('emailid')
		if emailid:
			emailid = emailid.strip()
		zipcode = self.request.get('zipcodeid')
		if zipcode:
			zipcode = zipcode.strip()
		validationservice = ValidationService()
		isvalidemail = validationservice.isvalidemail(emailid)
		isvalidzipcode = validationservice.isvalidzipcode(zipcode)
		if not isvalidemail or not isvalidzipcode:
			returnvalue = 0			
			if not isvalidemail:
				returnvalue |= constants.INPUT_INVALID_ZIPCODE
			if not isvalidzipcode:
				returnvalue |= constants.INPUT_INVALID_EMAILID
			q = 'r='+str(returnvalue)
			if emailid:
				q += '&'
				q += 'e='+str(emailid)
			if zipcode:
				q += '&'
				q += 'z='+str(zipcode)
			self.redirect('/signup?'+q)
		else:
			signupservice = SignUpService()
			returnvalue = signupservice.signup(emailid, zipcode)		
			self.redirect('/signupstatus?r='+str(returnvalue)+'&e='+str(emailid))

class SignUpStatusPage(webapp2.RequestHandler):
	def get(self):
		uid =extractkeyfromrequest(self.request, 'u')
		insession = issessionrequest(self.request)
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
