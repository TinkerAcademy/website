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
from pageutils import extractkeyvaluesfromrequest
from pageutils import evaluateanswer
from pageutils import isinsession
from pageutils import issessionrequest
from pageutils import isadminuser
from pageutils import createloginurl
from pageutils import attemptlogin
from pageutils import translateclaztosource
from pageutils import quizanswers
from pageutils import hwanswers

from environment import JINJA_ENVIRONMENT

from services import UserService
from services import CoursesService
from services import SignUpService
from services import ForgotStudentIDService
from services import ValidationService
from services import ChannelPartnersService
from services import StaffService
from services import TinkerAcademyUserService
from services import MemcacheService

class AchievementsPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'newuser' : False,
		}
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('achievements.html')
		self.response.write(template.render(template_values))

class AdminPage(webapp2.RequestHandler):
	def get(self):
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {}
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		self.response.write(template.render(template_values))

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
		# logging.error('template_values='+str(template_values))
		template = JINJA_ENVIRONMENT.get_template('about.html')
		self.response.write(template.render(template_values))

class AboutUsPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'newuser' : False,
		}
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('aboutus.html')
		self.response.write(template.render(template_values))

class APComputerSciencePage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		cacheservice = MemcacheService()
		if sessionid:
			user = cacheservice.getsessionuser(sessionid)				
		template_values = {
			'sessionid' : sessionid,
			'user' : user
		}
		for i in range(1,10):
			template_values['quiz' + str(i) + 'submitted'] = cacheservice.getfromsession(sessionid, 'quiz' + str(i) + 'submitted');	
			template_values['quiz' + str(i) + 'results'] = cacheservice.getfromsession(sessionid, 'quiz' + str(i) + 'results');	
			template_values['quiz' + str(i) + 'len'] = cacheservice.getfromsession(sessionid, 'quiz' + str(i) + 'len');	
		for i in range(1,10):
			template_values['hw' + str(i) + 'submitted'] = cacheservice.getfromsession(sessionid, 'hw' + str(i) + 'submitted');	
			template_values['hw' + str(i) + 'results'] = cacheservice.getfromsession(sessionid, 'hw' + str(i) + 'results');	
			template_values['hw' + str(i) + 'len'] = cacheservice.getfromsession(sessionid, 'hw' + str(i) + 'len');	
		logging.info("APComputerSciencePage template_values="+str(template_values))
		if sessionid:
			for i in range(1,10):				
				cacheservice.clearfromsession(sessionid, 'quiz' + str(i) + 'submitted')
				cacheservice.clearfromsession(sessionid, 'quiz' + str(i) + 'results')
				cacheservice.clearfromsession(sessionid, 'quiz' + str(i) + 'len')
			for i in range(1,10):				
				cacheservice.clearfromsession(sessionid, 'hw' + str(i) + 'submitted')
				cacheservice.clearfromsession(sessionid, 'hw' + str(i) + 'results')
				cacheservice.clearfromsession(sessionid, 'hw' + str(i) + 'len')
		template = JINJA_ENVIRONMENT.get_template('apcomputerscience.html')
		self.response.write(template.render(template_values))		
	def post(self):			
		userservice = TinkerAcademyUserService()
		sessionid = userservice.anonlogin()
		cacheservice = MemcacheService()
		self.redirect('/apcomputerscience.html?s='+str(sessionid))

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

# class CoursePage(webapp2.RequestHandler):
# 	def get(self):
# 		uid, insession = attemptlogin(self.request)
# 		courseid = extractkeyfromrequest(self.request, 'c')
# 		coursesservice = CoursesService()
# 		course = coursesservice.getcourse(courseid)	
# 		coursecontents = coursesservice.getcoursecontents(courseid)
# 		# coursehandouts = coursesservice.getcoursehandouts(courseid)
# 		# coursehomeworks = coursesservice.getcoursehomeworks(courseid)
# 		# coursevideos = coursesservice.getcoursevideos(courseid)
# 		# coursestarterpacks = coursesservice.getcoursestarterpacks(courseid)		
# 		# coursequizzes = coursesservice.getcoursequizzes(courseid)
# 		template_values = {}
# 		header_template_values = buildheadertemplatevalues(insession, uid)
# 		template_values.update(header_template_values)
# 		course_template_values = buildcoursetemplatevalues(insession, course, coursecontents)
# 		template_values.update(course_template_values)		
# 		logging.info('template_values='+str(template_values))
# 		template = JINJA_ENVIRONMENT.get_template('course.html')
# 		self.response.write(template.render(template_values))		

class CoursePage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'newuser' : False,
		}
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
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

class ClassroomPage(webapp2.RequestHandler):
	def get(self):
		basedir = os.path.dirname(__file__)		
		staticdir = os.path.join(basedir, 'static')
		staticfiles = os.listdir(staticdir)
		staticfiles = [staticfile for staticfile in staticfiles if not staticfile.startswith('.')]
		template_values = {}
		template_values['staticfiles'] = staticfiles
		template = JINJA_ENVIRONMENT.get_template('classroom.html')
		self.response.write(template.render(template_values))	

class ContactPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'newuser' : False,
		}
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('contact.html')
		self.response.write(template.render(template_values))

class ShowcasePage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'newuser' : False,
		}
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('showcase.html')
		self.response.write(template.render(template_values))		

class CurriculumPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		newuser = None
		cacheservice = MemcacheService()
		if sessionid:
			user = cacheservice.getsessionuser(sessionid)
			newuser = cacheservice.getfromsession(sessionid, "newuser")			
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			"newuser" : newuser,
		}
		if sessionid:
			cacheservice.clearfromsession(sessionid, "newuser")
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('curriculum.html')
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
		emailid = self.request.get('e')
		forgotservice = ForgotStudentIDService()
		returnvalue = forgotservice.sendemail(emailid)
		self.redirect('/forgot?e='+str(emailid)+'&r='+str(returnvalue))

class LoginPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
		}
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('login.html')		
		self.response.write(template.render(template_values))
	def post(self):
		studentid = extractkeyfromrequest(self.request, 'studentid')
		emailid = extractkeyfromrequest(self.request, 'email')
		if emailid:
			emailid = emailid.strip()
		if studentid:
			studentid = studentid.strip()
			studentid = int(studentid)
			userservice = TinkerAcademyUserService()
			user = userservice.finduserbystudentid(studentid)
			if user:
				sessionid = userservice.login(user)
				if sessionid:
					self.redirect('/course.html?s='+str(sessionid))
			else:
				self.redirect('/login.html')

class MyCoursesPage(webapp2.RequestHandler):
	def get(self):
		uid, insession = attemptlogin(self.request)
		coursesservice = CoursesService()
		userservice = UserService()
		emailid = userservice.getemailidforsession(uid)
		usercourses = coursesservice.listusercourses(emailid)
		template_values = {}
		header_template_values = buildheadertemplatevalues(insession, uid)
		template_values.update(header_template_values)
		course_template_values = buildmycoursestemplatevalues(insession, uid, usercourses)
		template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('mycourses.html?s='+str(sessionid))
		self.response.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'newuser' : False,
		}
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class PaymentPage(webapp2.RequestHandler):
	def get(self):
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {}
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('payment.html')
		self.response.write(template.render(template_values))

class ProfilePage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		source = None
		cacheservice = MemcacheService()
		quizresults = []
		hwresults = []
		if sessionid:
			user = cacheservice.getsessionuser(sessionid)
			source = translateclaztosource(user.claz)
			quizanswerarr = quizanswers(source)
			for quizint in range(1,9):
				if len(quizanswerarr) > quizint:
					quiz = quizanswerarr[quizint]
					quizlen = len(quiz)
					if "free" in quiz:
						quizlen = quizlen - 1 + quizanswerarr[quizint]["free"]
					quizresult = getattr(user, 'quiz' + str(quizint) + 'results')
					if quizresult is None:
						quizresult = 0
					quizresults.append({'total' : quizlen, 'correct': quizresult})
			hwanswerarr = hwanswers(source)
			for hwint in range(1,9):
				if len(hwanswerarr) > hwint:
					hw = hwanswerarr[hwint]
					hwlen = len(hw)
					if "free" in hw:
						hwlen = hwlen - 1 + hwanswerarr[hwint]["free"]
					hwresult = getattr(user, 'hw' + str(hwint) + 'results')
					if hwresult is None:
						hwresult = 0
					hwresults.append({'total' : hwlen, 'correct': hwresult})
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'quizresults' : quizresults,
			'hwresults' : hwresults
		}
		template = JINJA_ENVIRONMENT.get_template('profile.html')
		self.response.write(template.render(template_values))

class ProgrammingUsingJavaPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		cacheservice = MemcacheService()
		if sessionid:
			user = cacheservice.getsessionuser(sessionid)				
		template_values = {
			'sessionid' : sessionid,
			'user' : user
		}
		if sessionid:
			for i in range(1,101):
				template_values['quiz' + str(i) + 'submitted'] = cacheservice.getfromsession(sessionid, 'quiz' + str(i) + 'submitted');	
				template_values['quiz' + str(i) + 'results'] = cacheservice.getfromsession(sessionid, 'quiz' + str(i) + 'results');	
				template_values['quiz' + str(i) + 'len'] = cacheservice.getfromsession(sessionid, 'quiz' + str(i) + 'len');	
			for i in range(1,101):				
				cacheservice.clearfromsession(sessionid, 'quiz' + str(i) + 'submitted')
				cacheservice.clearfromsession(sessionid, 'quiz' + str(i) + 'results')
				cacheservice.clearfromsession(sessionid, 'quiz' + str(i) + 'len')
		template = JINJA_ENVIRONMENT.get_template('programmingusingjava.html')
		self.response.write(template.render(template_values))		
	def post(self):			
		userservice = TinkerAcademyUserService()
		sessionid = userservice.anonlogin()
		cacheservice = MemcacheService()
		self.redirect('/programmingusingjava.html?s='+str(sessionid))

class RegisterPage(webapp2.RequestHandler):
	def get(self):
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		isnewuser = False
		isfuture = False
		isrecservicesclaz = False
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
			isnewuser = cacheservice.getfromsession(sessionid, "newuser")	
			claz = cacheservice.getfromsession(sessionid, "claz")
			isfuture = claz == 'Future Sessions'
			isrecservicesclaz = claz == 'Sep 2015 - Nov 2015' or claz == 'Sep 2015 - Nov 2015 (AP)'
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {
			'sessionid' : sessionid,
			'user' : user,
			'isnewuser' : isnewuser,
			'isfuture' : isfuture,
			'isrecservicesclaz' : isrecservicesclaz
		}
		if sessionid:
			cacheservice.clearfromsession(sessionid, "newuser")
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('register.html')
		self.response.write(template.render(template_values))
	def post(self):
		emailid = extractkeyfromrequest(self.request, 'email')
		name = extractkeyfromrequest(self.request, 'name')
		claz = extractkeyfromrequest(self.request, 'class')
		favmod = extractkeyfromrequest(self.request, 'favmod')
		zipcode = extractkeyfromrequest(self.request, 'zipcode')
		if emailid:
			emailid = emailid.strip()
		validationservice = ValidationService()
		isvalidemail = validationservice.isvalidemail(emailid)
		if isvalidemail and name:
			userservice = TinkerAcademyUserService()
			sessionid = userservice.register(name, emailid, claz, favmod, zipcode)		
			cacheservice = MemcacheService()
			cacheservice.putinsession(sessionid, "newuser", True)	
			cacheservice.putinsession(sessionid, "claz", claz)
			self.redirect('/register.html?s='+str(sessionid))
		else:
			self.redirect('/register.html')

class ScholarshipPage(webapp2.RequestHandler):
	def get(self):
		# uid, insession = attemptlogin(self.request)
		# coursesservice = CoursesService()
		# courses = coursesservice.listupcomingcourses()
		template_values = {}
		# header_template_values = buildheadertemplatevalues(insession, uid)
		# template_values.update(header_template_values)
		# course_template_values = buildallcoursestemplatevalues(insession, courses)
		# template_values.update(course_template_values)
		template = JINJA_ENVIRONMENT.get_template('scholarship.html')
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
		emailid = self.request.get('e')
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
		emailid = self.request.get('e')
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

class SubmitHomeworkPage(webapp2.RequestHandler):
	def post(self):
		uid, insession = attemptlogin(self.request)
		if insession:
			pass
		self._done()
	def _done(self):
		uid, insession = attemptlogin(self.request)
		c = extractkeyfromrequest(self.request, 'c')
		cc = extractkeyfromrequest(self.request, 'cc')
		if c and cc and uid:
			self.redirect('/coursecontent?c='+str(c)+'&cc='+str(cc)+'&u='+uid)

class SaveQuizPage(webapp2.RequestHandler):
	def post(self):			
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		source = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
			if user:
				if self.request.params:
					quiz = str(extractkeyfromrequest(self.request, 'quiz'))
					quizint = int(quiz)
					source = str(extractkeyfromrequest(self.request, 'source'))
					if not source:
						source = translateclaztosource(user.claz)
					if source:
						answerarr = quizanswers(source)
						studentdict = self.request.params
						quizresults = evaluateanswer(studentdict, answerarr[quizint])
						quizlen = len(answerarr[quizint])
						if "free" in answerarr[quizint]:
							quizlen = quizlen - 1 + answerarr[quizint]["free"]
							quizresults = quizresults + answerarr[quizint]["free"]
						kvpairs = extractkeyvaluesfromrequest(self.request)
						quizstr = kvpairs
						setattr(user, 'quiz' + quiz, quizstr)
						setattr(user, 'quiz' + quiz + 'results', quizresults)
						user.put()
						cacheservice.setsessionuser(sessionid, user)
						cacheservice.putinsession(sessionid, 'quiz' + str(quiz) + 'submitted', True)	
						cacheservice.putinsession(sessionid, 'quiz' + str(quiz) + 'results', quizresults)	
						cacheservice.putinsession(sessionid, 'quiz' + str(quiz) + 'len', quizlen)	
		redirecthtml = "./index.html"
		if source == "ap":
			redirecthtml = "./apcomputerscience.html"
		elif source == "pj":
			redirecthtml = "./programmingusingjava.html"			
		if sessionid:
			redirecthtml = redirecthtml + "?s=" + str(sessionid)
		self.redirect(redirecthtml)


class SaveHomeworkPage(webapp2.RequestHandler):
	def post(self):			
		sessionid = extractkeyfromrequest(self.request, 's')
		if sessionid:
			sessionid = sessionid.strip()
		user = None
		source = None
		if sessionid:
			cacheservice = MemcacheService()
			user = cacheservice.getsessionuser(sessionid)
			if user:
				if self.request.params:
					hw = str(extractkeyfromrequest(self.request, 'hw'))
					hwint = int(hw)
					source = str(extractkeyfromrequest(self.request, 'source'))
					if not source:
						source = translateclaztosource(user.claz)
					if source:
						answerarr = hwanswers(source)
						studentdict = self.request.params
						hwresults = evaluateanswer(studentdict, answerarr[hwint])
						hwlen = len(answerarr[hwint])
						if "free" in answerarr[hwint]:
							hwlen = hwlen - 1 + answerarr[hwint]["free"]
							hwresults = hwresults + answerarr[hwint]["free"]
						kvpairs = extractkeyvaluesfromrequest(self.request)
						hwstr = kvpairs
						setattr(user, 'hw' + hw, hwstr)
						setattr(user, 'hw' + hw + 'results', hwresults)
						user.put()
						cacheservice.setsessionuser(sessionid, user)
						cacheservice.putinsession(sessionid, 'hw' + str(hw) + 'submitted', True)	
						cacheservice.putinsession(sessionid, 'hw' + str(hw) + 'results', hwresults)	
						cacheservice.putinsession(sessionid, 'hw' + str(hw) + 'len', hwlen)	
		redirecthtml = "./index.html"
		if source == "ap":
			redirecthtml = "./apcomputerscience.html"
		elif source == "pj":
			redirecthtml = "./programmingusingjava.html"			
		if sessionid:
			redirecthtml = redirecthtml + "?s=" + str(sessionid)
		self.redirect(redirecthtml)

# Old
class SubmitQuizPage(webapp2.RequestHandler):
	def post(self):
		uid, insession = attemptlogin(self.request)
		if insession:
			pass
		self._done()
	def _done(self):
		uid, insession = attemptlogin(self.request)
		c = extractkeyfromrequest(self.request, 'c')
		cc = extractkeyfromrequest(self.request, 'cc')
		if c and cc and uid:
			self.redirect('/coursecontent?c='+str(c)+'&cc='+str(cc)+'&u='+uid)
