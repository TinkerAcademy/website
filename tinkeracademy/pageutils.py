import os
import urllib
import jinja2
import logging
import webapp2
import pageutils
import logging
import json

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

def evaluateanswer(studentdict, answerdict):
	#{ "quiz":2, "answers":{"quiz":2 , "source":"ap" , "s":"ccb5eca7f5baff157d911dbe67ed3a38e75a170f" , "q1":2 , "submit":1} }
	correct = 0
	for i in range(1,10):
		key = "q" + str(i)
		if key in answerdict:
			if key in studentdict:
				try:
					if int(answerdict[key]) == int(studentdict[key]):
						correct = correct + 1
				except ValueError:
					pass
	return correct

def extractkeyvaluesfromrequest(request):
	kvget = json.dumps(request.GET.items())
	kvpost = json.dumps(request.POST.items())
	kvpairs = "{" + "get:" + str(kvget) + ",post:" + str(kvpost) + "}"
	return kvpairs

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

def translateclaztosource(claz):
	if "(AP)" in claz:
		return "ap"
	return "pj"

def quizanswers(source):
	answersdict = {
			"ap": [
					{},{},
					{
						"q1":1, "q2":2, "q3":1, "q4":2, "q5":2, "free" : 1
					},
					{
						"q1":1, "q2":1, "q3":2, "q4":2, "q5":2, "q6": 1, "q7": 1
					},
					{
						"q1":1, "q2":1, "q3":2, "q4":1, "q5":2, "q6": 1
					},
					{
						"q1":3, "q2": 3, "q3": 2, "q4": 3, "q5": 3
					},
					{
						"q1":4, "q2": 1, "q3": 4, "q4": 3, "q5": 3
					},
					{
						"q1":3, "q2": 2, "q3": 4, "q4": 2, "q5": 3
					}
				],
			"pj": [
					{}, {},
					{
						"q1":2, "q2":1, "q3":2, "q4":2 
					}
				]
		}
	return answersdict[source]

def hwanswers(source):
	answersdict = {
			"ap": [
					{},{},{},{},
					{
						"q1":-46672, "q2":7497032
					}, 
					{
						"q1":9, "q2":1440000
					}, 					
					{
						"q1":9998, "q2":46368
					}, 					
					{
						"q1":-1824255374, "q2":-1406625280
					} 					
				]
		}
	return answersdict[source]	

