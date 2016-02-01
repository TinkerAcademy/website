import os
import urllib
import jinja2
import logging
import webapp2

from environment import JINJA_ENVIRONMENT

from pages import 	MainPage, \
					AcePage, \
					CurriculumPage, \
					LoginPage, \
					RegisterPage, \
					SubscribePage, \
					AboutUsPage, \
					ContactPage, \
					AdminPage, \
					PaymentPage, \
					ScholarshipPage, \
					ShowcasePage, \
					APComputerSciencePage, \
					ProgrammingUsingJavaPage, \
					CoursePage, \
					AchievementsPage, \
					SaveQuizPage, \
					SaveHomeworkPage, \
					ProfilePage, \
					InstallationPage
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
										('/index-ace.html', AcePage),
										('/about.html', AboutUsPage),
										('/curriculum.html', CurriculumPage),
										('/login.html', LoginPage),
										('/course.html', CoursePage),
										('/apcomputerscience.html', APComputerSciencePage),										
										('/programmingusingjava.html', ProgrammingUsingJavaPage),										
										('/showcase.html', ShowcasePage),
										('/achievements.html', AchievementsPage),
										('/savequiz.html', SaveQuizPage),
										('/savehomework.html', SaveHomeworkPage),
										('/profile.html', ProfilePage),
										('/aboutus.html', AboutUsPage),
										('/register.html', RegisterPage),
										('/subscribe.html', SubscribePage),
										('/contact.html', ContactPage),
										('/installation.html', InstallationPage),
										('/admin.html', AdminPage),
										('/payment.html', PaymentPage),
										('/scholarship.html', ScholarshipPage),
										# ('/task/email', EmailTask),
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
										('/task/databaseupdate', DatabaseUpdateTask),
										# ('/task/tokenupdate', TokenUpdateTask),
									], debug=True)



