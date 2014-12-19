import sys
import logging
import pygeoip

geoip = None

def loadgeoip():
	global geoip	
	if geoip is None:
		geoip = pygeoip.GeoIP('GeoLiteCity.dat', flags=pygeoip.const.MEMORY_CACHE)
	logging.info('geoip ' + str(geoip))
	return geoip

# ZIPCODE_FILE = 'free-zipcode-database-Primary.csv'

# VALID_ZIPCODE_LIST = {}

# def validate_zipcode(zipcode):
	# read_zipcode_database()
	# if zipcode in VALID_ZIPCODE_LIST:
	# 	return True
	# return False

# def read_zipcode_database():
	# if len(VALID_ZIPCODE_LIST) > 0:
	# 	return
	# csvfile = open(ZIPCODE_FILE, 'rb')
	# try:
	# 	csvreader = csv.reader(csvfile)
	# 	header=True
	# 	for row in csvreader:
	# 		if header:
	# 			header = False
	# 			continue
	# 		zipcode = row[0]
	# 		city = row[2]
	# 		state = row[3]
	# 		VALID_ZIPCODE_LIST[zipcode] = { 'zipcode': zipcode, 'city': city, 'state': state }
	# except:
	# 	logging.error("error parsing csv file " + str(ZIPCODE_FILE))
	# 	sys_err = sys.exc_info()
	# 	logging.error(sys_err[1])		
	# finally:
	# 	if csvfile:
	# 		csvfile.close()