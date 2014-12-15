import logging
import os
import sys
import uuid

from google.appengine.api import memcache

from models import User, \
				   UserCourse, \
				   SignUp, \
				   Course

class ForgotStudentIDService(object):
	def sendemail(self, emailid):
		#TODO: schedule email
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
	def listcourses(self):
		cacheservice = MemcacheService()
		courses = cacheservice.getcourses()
		if (not courses) or len(courses) == 0:
			courses = []
			query = Course.all()
			for q in query.run(limit=100):
				courses.append(query)
			cacheservice.setcourses(courses)
		return courses
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
	def signup(self, emailid):
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
			p.put()
			schedulerservice = SchedulerService()
			schedulerservice.schedulesignup(p)
			return p
		except Exception as e:
			logging.error("error signing up " + str(emailid))
			sys_err = sys.exc_info()
			logging.error(sys_err[1])
		return None

class SchedulerService(object):
	def schedulesignup(self, p):
		pass
