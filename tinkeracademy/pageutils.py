import os
import urllib
import jinja2
import logging
import webapp2
import pageutils
import logging

from environment import JINJA_ENVIRONMENT
from google.appengine.api import users

from services import UserService
from services import CoursesService
from services import SignUpService

def buildheadertemplatevalues(insession, uid):
	template_values = {}
	if insession:
		template_values['abouturl'] = '/about?u=' + str(uid)
		template_values['abouturllinktext'] = 'About'
	else:
		template_values['abouturl'] = '/about'
		template_values['abouturllinktext'] = 'About'		
	if insession:
		template_values['allcoursesurl'] = '/allcourses?u='+str(uid)
		template_values['allcoursesurllinktext'] = 'All Courses'
	else:
		template_values['allcoursesurl'] = '/allcourses'
		template_values['allcoursesurllinktext'] = 'All Courses'
	if insession:
		template_values['mycoursesurl'] = '/mycourses?u=' + str(uid)
		template_values['mycoursesurllinktext'] = 'My Courses'
	if not insession:
		template_values['signinurl'] = '/signin'
		template_values['signinurllinktext'] = 'Sign In'
	if not insession:
		template_values['signupurl'] = '/signup'
		template_values['signupurllinktext'] = 'Sign Up'
	if insession:
		template_values['signouturl'] = '/signout?u=' + str(uid)
		template_values['signouturllinktext'] = 'Sign Out'
	return template_values

def buildallcoursestemplatevalues(insession, allcourses):
	template_values = {}
	courses_values = template_values['allcourses'] = []
	for course in allcourses:
		course_value = {}
		course_value['courseurl'] = '/course?c=' + str(course.id)
		course_value['courseurllinktext'] = course.name
		courses_values.append(course_value)
	template_values.update(courses_values)
	return template_values

def buildmycoursestemplatevalues(insession, uid, mycourses):
	template_values = {}
	courses_values = template_values['mycourses'] = []
	for course in mycourses:
		course_value = {}
		course_value['courseurl'] = '/course?c=' + str(course.id) + "&u=" + str(uid)
		course_value['courseurllinktext'] = course.name
		course_values.append(course_value)
	template_values.update(courses_values)
	return template_values

def extractkeyfromrequest(request, key):
	uid = None
	if request.params and len(request.params) > 0:
		if key in request.params:
			uid = request.params[key]
	return uid

def createloginurl():
	return users.create_login_url('/')

def isadminuser():
	user = users.get_current_user()
	logging.info('admin user is ' + str(user))
	if user:
		return users.is_current_user_admin()
	return False

def isinsession(uid):
	insession = False
	userservice = UserService()
	if userservice.hassession(uid):
		insession = True
	return insession

def issessionrequest(request):
	uid = extractkeyfromrequest(request, 'u')
	insession = isinsession(uid)
	return insession
