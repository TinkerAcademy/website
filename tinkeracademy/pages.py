import os
import urllib
import jinja2
import logging
import webapp2

from pageutils import buildheadertemplatevalues
from pageutils import buildallcoursestemplatevalues
from pageutils import buildmycoursestemplatevalues
from pageutils import extractkeyfromrequest
from pageutils import isinsession
from pageutils import issessionrequest

from environment import JINJA_ENVIRONMENT

from services import UserService
from services import CoursesService
from services import SignUpService
from services import ForgotStudentIDService

class AboutPage(webapp2.RequestHandler):
	def get(self):
		uid = extractkeyfromrequest(self.request, 'u')
		insession = isinsession(uid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		template = JINJA_ENVIRONMENT.get_template('about.html')
		self.response.write(template.render(template_values))

class AdminPage(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('admin.html')
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
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)		
		template = JINJA_ENVIRONMENT.get_template('signup.html')
		self.response.write(template.render(template_values))
	def post(self):
		emailid = self.request.get('emailid')
		signupservice = SignUpService()
		returnvalue = signupservice.signup(emailid)
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

