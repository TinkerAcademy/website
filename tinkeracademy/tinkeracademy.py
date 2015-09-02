import os
import urllib
import jinja2
import logging
import webapp2

from environment import JINJA_ENVIRONMENT

from pages import 	MainPage, \
					CurriculumPage, \
					LoginPage, \
					RegisterPage, \
					ContactPage, \
					AdminPage, \
					PaymentPage, \
					ScholarshipPage, \
					ShowcasePage
					# CoursePage, \
					# CourseContentsPage, \
					# ClassroomPage, \
					# ForgotPage, \
					# AllCoursesPage, \
					# MyCoursesPage, \
					# SignInPage, \
					# SignOutPage, \
					# AboutPage, \
					# SignUpPage, \
					# SignUpStatusPage, \
					# SubmitHomeworkPage, \
					# SubmitQuizPage

from tasks import 	EmailTask, \
					DatabaseUpdateTask, \
					TokenUpdateTask

application = webapp2.WSGIApplication([
										('/', MainPage),
										('/index.html', MainPage),
										('/curriculum.html', CurriculumPage),
										# ('/login.html', LoginPage),
										('/showcase.html', ShowcasePage),
										('/register.html', RegisterPage),
										('/contact.html', ContactPage),
										('/admin.html', AdminPage),
										('/payment.html', PaymentPage),
										('/scholarship.html', ScholarshipPage),
										('/task/email', EmailTask),
										# ('/coursecontent', CourseContentsPage),
										# ('/classroom', ClassroomPage),
										# ('/forgot', ForgotPage),
										# ('/about', AboutPage),
										# ('/allcourses', AllCoursesPage),
										# ('/mycourses', MyCoursesPage),
										# ('/signin', SignInPage),
										# ('/signout', SignOutPage),
										# ('/signup', SignUpPage),
										# ('/signupstatus', SignUpStatusPage),
										# ('/submithomework', SubmitHomeworkPage),
										# ('/submitquiz', SubmitQuizPage),
										# ('/task/databaseupdate', DatabaseUpdateTask),
										# ('/task/tokenupdate', TokenUpdateTask),
									], debug=True)



