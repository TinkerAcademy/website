import logging
import os

from google.appengine.ext import db

class User(db.Model):
	emailid = db.StringProperty()
	studentid = db.StringProperty()

class UserCourse(db.Model):
	studentid = db.IntegerProperty()
	courseid = db.StringProperty()
	startdate = db.DateProperty()
	enddate = db.DateProperty()
	status = db.IntegerProperty()

class UserHomework(db.Model):
	studentid = db.IntegerProperty()
	homeworkid = db.StringProperty()
	startdate = db.DateProperty()
	enddate = db.DateProperty()
	status = db.IntegerProperty()

class UserVideo(db.Model):
	studentid = db.IntegerProperty()
	videoid = db.StringProperty()
	startdate = db.DateProperty()
	enddate = db.DateProperty()
	status = db.IntegerProperty()

class UserStarterPack(db.Model):
	studentid = db.IntegerProperty()
	courseid = db.StringProperty()
	startdate = db.DateProperty()
	enddate = db.DateProperty()
	status = db.IntegerProperty()

class UserVideo(db.Model):
	studentid = db.IntegerProperty()
	videoid = db.StringProperty()
	startdate = db.DateProperty()
	enddate = db.DateProperty()
	status = db.IntegerProperty()

class UserQuiz(db.Model):
	studentid = db.IntegerProperty()
	quizid = db.StringProperty()
	startdate = db.DateProperty()
	enddate = db.DateProperty()
	status = db.IntegerProperty()

class Course(db.Model):
	courseid = db.StringProperty()
	coursetag = db.StringProperty()
	coursename = db.StringProperty()
	coursedescription = db.TextProperty()
	courseyear = db.IntegerProperty()
	coursestartdate = db.StringProperty()
	courseenddate = db.StringProperty()
	coursesession = db.StringProperty()
	coursepartner = db.StringProperty()
	courseminage = db.IntegerProperty()
	coursemaxage = db.IntegerProperty()
	coursenumclasses = db.IntegerProperty()
	courseclassdurationmins = db.IntegerProperty()
	courseisonline = db.BooleanProperty()

class Homework(db.Model):
	homeworkid = db.StringProperty()
	homeworkblob = db.BlobProperty()

class StarterPack(db.Model):
	starterpackid = db.StringProperty()	
	starterpackblob = db.BlobProperty()

class Video(db.Model):
	videoid = db.StringProperty()
	youtubeurl = db.StringProperty()

class Quiz(db.Model):
	quizid = db.StringProperty()
	quizblob = db.BlobProperty()

class SignUp(db.Model):
	emailid = db.StringProperty()
	zipcode = db.StringProperty()
	counter = db.IntegerProperty()

class Email(db.Model):
	senderemailid = db.StringProperty()
	receiveremailid = db.StringProperty()
	typeid = db.StringProperty()
	counter = db.IntegerProperty()
	subject = db.TextProperty()
	body = db.TextProperty()
	filename = db.StringProperty()
