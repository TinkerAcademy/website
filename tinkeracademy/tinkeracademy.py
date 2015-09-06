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
					AboutUsPage, \
					ContactPage, \
					AdminPage, \
					PaymentPage, \
					ScholarshipPage, \
					ShowcasePage, \
					APComputerSciencePage
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
										('/about.html', AboutUsPage),
										('/curriculum.html', CurriculumPage),
										# ('/login.html', LoginPage),
										('/apcomputerscience.html', APComputerSciencePage),										
										('/showcase.html', ShowcasePage),
										('/aboutus.html', AboutUsPage),
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



