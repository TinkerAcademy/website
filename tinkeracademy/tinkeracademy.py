import os
import urllib
import jinja2
import logging
import webapp2

from environment import JINJA_ENVIRONMENT

from pages import 	MainPage, \
					ForgotPage, \
					AllCoursesPage, \
					MyCoursesPage, \
					SignInPage, \
					SignOutPage, \
					AboutPage, \
					SignUpPage, \
					SignUpStatusPage, \
					AdminPage

application = webapp2.WSGIApplication([
										('/', MainPage),
										('/forgot', ForgotPage),
										('/index.html', MainPage),
										('/about', AboutPage),
										('/allcourses', AllCoursesPage),
										('/mycourses', MyCoursesPage),
										('/signin', SignInPage),
										('/signout', SignOutPage),
										('/signup', SignUpPage),
										('/signupstatus', SignUpStatusPage),
										('/admin', AdminPage),
									], debug=True)



