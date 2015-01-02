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

def attemptlogin(request):
	uid = extractkeyfromrequest(request, 'u')
	emailid = request.get('e')
	studentid = request.get('s')	
	if emailid and studentid:
		userservice = UserService()
		uid = userservice.registersession(emailid, studentid)
	insession = isinsession(uid)
	return (uid, insession)

def buildheadertemplatevalues(insession, uid):
	template_values = {}
	if insession:
		template_values['UID']=uid	
	else:
		template_values.pop('UID', None)
	template_values['abouturl'] = '/about'
	template_values['abouturllinktext'] = 'About'
	template_values['allcoursesurl'] = '/allcourses'
	template_values['allcoursesurllinktext'] = 'All Courses'	
	if insession:
		template_values['mycoursesurl'] = '/mycourses'
		template_values['mycoursesurllinktext'] = 'My Courses'
	if not insession:
		template_values['signinurl'] = '/signin'
		template_values['signinurllinktext'] = 'Sign In'	
	if not insession:
		template_values['signupurl'] = '/signup'
		template_values['signupurllinktext'] = 'Register'	
	if insession:
		template_values['signouturl'] = '/signout'
		template_values['signouturllinktext'] = 'Sign Out'
	return template_values

def buildstafftemplatevalues(insession, staff):
	template_values = {}
	template_values['staff'] = staff
	return template_values

def buildchannelpartnertemplatevalues(insession, channelpartners):
	template_values = {}
	template_values['channelpartners'] = channelpartners
	return template_values	

def buildallcoursestemplatevalues(insession, allcourses):
	template_values = {}
	template_values['courses'] = allcourses
	return template_values

def buildmycoursestemplatevalues(insession, uid, mycourses):
	template_values = {}
	template_values['courses'] = mycourses
	return template_values

def buildcoursetemplatevalues(insession, course, coursecontents):
	template_values = {}
	template_values['course'] = course
	template_values['coursecontents'] = coursecontents
	# template_values['coursehandouts'] = coursehandouts
	# template_values['coursehomeworks'] = coursehomeworks
	# template_values['coursevideos'] = coursevideos
	# template_values['coursestarterpacks'] = coursestarterpacks
	# template_values['coursequizs'] = coursequizzes
	return template_values	

def buildcoursecontenttemplatevalues(insession, courseid, coursecontentid, course, coursecontents, coursehandouts, coursehomeworks, coursevideos, coursestarterpacks, coursequizs):
	template_values = {}
	template_values['COURSE'] = courseid
	template_values['COURSECONTENT'] = coursecontentid
	template_values['course'] = course
	template_values['coursecontents'] = coursecontents
	for coursecontent in coursecontents:
		if coursecontent.coursecontentid == coursecontentid:
			template_values['coursecontent'] = coursecontent
	template_values['coursehandouts'] = []
	for coursehandout in coursehandouts:
		if coursehandout.coursecontentid == coursecontentid:
			template_values['coursehandouts'].append(coursehandout)
	template_values['coursehomeworks'] = []
	for coursehomework in coursehomeworks:
		if coursehomework.coursecontentid == coursecontentid:
			template_values['coursehomeworks'].append(coursehomework)
	template_values['coursestarterpacks'] = []
	for coursestarterpack in coursestarterpacks:
		if coursestarterpack.coursecontentid == coursecontentid:
			template_values['coursestarterpacks'].append(coursestarterpack)
	template_values['coursequizs'] = []
	for coursequiz in coursequizs:
		if coursequiz.coursecontentid == coursecontentid:
			template_values['coursequizs'].append(coursequiz)
	template_values['coursevideos'] = []
	for coursevideo in coursevideos:
		if coursevideo.coursecontentid == coursecontentid:
			template_values['coursevideos'].append(coursevideo)
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

