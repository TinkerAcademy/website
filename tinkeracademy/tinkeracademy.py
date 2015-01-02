import os
import urllib
import jinja2
import logging
import webapp2

from environment import JINJA_ENVIRONMENT

from pages import 	MainPage, \
					CoursePage, \
					CourseContentsPage, \
					ForgotPage, \
					AllCoursesPage, \
					MyCoursesPage, \
					SignInPage, \
					SignOutPage, \
					AboutPage, \
					SignUpPage, \
					SignUpStatusPage, \
					SubmitHomeworkPage, \
					SubmitQuizPage

from tasks import 	EmailTask, \
					DatabaseUpdateTask, \
					TokenUpdateTask

application = webapp2.WSGIApplication([
										('/', MainPage),
										('/course', CoursePage),
										('/coursecontent', CourseContentsPage),
										('/forgot', ForgotPage),
										('/index.html', MainPage),
										('/about', AboutPage),
										('/allcourses', AllCoursesPage),
										('/mycourses', MyCoursesPage),
										('/signin', SignInPage),
										('/signout', SignOutPage),
										('/signup', SignUpPage),
										('/signupstatus', SignUpStatusPage),
										('/submithomework', SubmitHomeworkPage),
										('/submitquiz', SubmitQuizPage),
										('/task/email', EmailTask),
										('/task/databaseupdate', DatabaseUpdateTask),
										('/task/tokenupdate', TokenUpdateTask),
									], debug=True)



