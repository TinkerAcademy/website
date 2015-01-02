import logging
import os

from google.appengine.ext import db

class ChannelPartner(db.Model):
	channelpartnerid = db.StringProperty()
	channelpartnercity = db.StringProperty()
	channelpartnerstate = db.StringProperty()
	channelpartnername = db.StringProperty()
	channelpartnerwebsite = db.StringProperty()
	channelpartnerregsite = db.StringProperty()

class User(db.Model):
	emailid = db.StringProperty()
	emailid2 = db.StringProperty()
	username = db.StringProperty()
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

class CourseContent(db.Model):
	courseid = db.StringProperty()
	coursecontentid = db.StringProperty()
	coursecontentname = db.StringProperty()
	coursecontenturl = db.StringProperty()
	coursecontentdescription = db.TextProperty()

class CourseHandout(db.Model):
	courseid = db.StringProperty()
	coursecontentid = db.StringProperty()
	coursehandoutid = db.StringProperty()
	coursehandoutname = db.StringProperty()	
	coursehandoutdescription = db.TextProperty()
	coursehandoutdownloadurl = db.StringProperty()

class CourseHomework(db.Model):
	courseid = db.StringProperty()
	coursecontentid = db.StringProperty()
	coursehomeworkid = db.StringProperty()
	coursehomeworkname = db.StringProperty()
	coursehomeworkdescription = db.TextProperty()
	coursehomeworkdownloadurl = db.StringProperty()

class CourseStarterPack(db.Model):
	courseid = db.StringProperty()
	coursecontentid = db.StringProperty()
	coursestarterpackid = db.StringProperty()
	coursestarterpackname = db.StringProperty()	
	coursestarterpackdescription = db.TextProperty()
	coursestarterpackdownloadurl = db.StringProperty()

class CourseVideo(db.Model):
	courseid = db.StringProperty()
	coursecontentid = db.StringProperty()
	coursevideoid = db.StringProperty()
	coursevideoname = db.StringProperty()
	coursevideodescription = db.TextProperty()
	coursevideodownloadurl = db.StringProperty()

class CourseQuiz(db.Model):
	courseid = db.StringProperty()
	coursecontentid = db.StringProperty()
	coursequizid = db.StringProperty()
	coursequizname = db.StringProperty()
	coursequizdescription = db.TextProperty()
	coursequizdownloadurl = db.StringProperty()

class SignUp(db.Model):
	emailid = db.StringProperty()
	ipaddress = db.StringProperty()
	counter = db.IntegerProperty()
	ipupdated = db.BooleanProperty()

class OtherCities(db.Model):
	cityname = db.StringProperty()
	countryname = db.StringProperty()
	latitude = db.FloatProperty()
	longitude = db.FloatProperty()

class Email(db.Model):
	senderemailid = db.StringProperty()
	receiveremailid = db.StringProperty()
	typeid = db.StringProperty()
	emailupdated = db.BooleanProperty()
	subject = db.TextProperty()
	body = db.TextProperty()
	filename = db.StringProperty()

class Staff(db.Model):
	staffid = db.StringProperty()
	staffname = db.StringProperty()
	staffrole = db.StringProperty()
	staffdescription = db.StringProperty()
	staffemail = db.StringProperty()


