import os
import urllib
import jinja2
import logging
import webapp2

from environment import JINJA_ENVIRONMENT

from pages import 	MainPage, \
					CoursePage, \
					ForgotPage, \
					AllCoursesPage, \
					MyCoursesPage, \
					SignInPage, \
					SignOutPage, \
					AboutPage, \
					SignUpPage, \
					SignUpStatusPage

from tasks import 	EmailTask, \
					DatabaseUpdateTask

application = webapp2.WSGIApplication([
										('/', MainPage),
										('/course', CoursePage),
										('/forgot', ForgotPage),
										('/index.html', MainPage),
										('/about', AboutPage),
										('/allcourses', AllCoursesPage),
										('/mycourses', MyCoursesPage),
										('/signin', SignInPage),
										('/signout', SignOutPage),
										('/signup', SignUpPage),
										('/signupstatus', SignUpStatusPage),
										('/task/email', EmailTask),
										('/task/databaseupdate', DatabaseUpdateTask),
									], debug=True)



