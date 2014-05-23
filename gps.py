#!/usr/bin/python

import os
import sys
import serial
import time
import redis
import math

def gpsCoordinate(value,ref):
	value=value/100
	minutes=math.trunc(value)
	seconds=math.fmod(value, 1);
	pos = minutes + seconds * 5 / 3;
	if ref == 'S' or ref == 'W':
		return pos * -1
	return pos

def recvGPS(GPS,redis):
	allInfoReaded=0
	lineReaded=0

	# $GPGGA : Global Positioning System Fix Data
	# $GPGSA : GPS DOP and active satellites 
	# $GPGSV : GPS Satellites in view
	# $GPRMC : Recommended minimum specific GPS/Transit data
	# $GPVTG : Track made good and ground spee

	while allInfoReaded != 0x1F and lineReaded <= 10:
		line = GPS.readline()
		line = line.rstrip()
		gpsdata=line.split(',')
		if   gpsdata[0] == "$GPGGA":
			allInfoReaded |= 0x1
			# parse data
			utc_time=float(gpsdata[1])
			latitude=gpsCoordinate(float(gpsdata[2]),gpsdata[3])
			longitude=gpsCoordinate(float(gpsdata[4]),gpsdata[5])
			satellites=int(gpsdata[7])
			altitude=float(gpsdata[9])
			# send values to redis
			redis.set('gps.utc_time',utc_time)
			redis.set('gps.latitude',latitude)
			redis.set('gps.longitude',longitude)
			redis.set('gps.altitude',altitude)
			redis.set('gps.satellites.inview',satellites)
			# debug
			print "utc = "+str(utc_time)+" lat = "+str(latitude)+" long = "+str(longitude)+" alt = "+str(altitude)+" satellites = "+str(satellites)
		elif gpsdata[0] == "$GPGSA":
			allInfoReaded |= 0x2
			# parse data
			fix=gpsdata[2]
			usedsat=0
			for sat in range(3,14):
				if gpsdata[sat].isdigit():
					usedsat+=1
			# send values to redis
			redis.set('gps.fix',fix+"D")
			redis.set('gps.satellites.used',usedsat)
			# debug
			print "fix = "+fix+"D usedsat = "+str(usedsat)
		elif gpsdata[0] == "$GPGSV":
			allInfoReaded |= 0x4
		elif gpsdata[0] == "$GPRMC":
			allInfoReaded |= 0x8
			# parse data
			speed=float(gpsdata[7])
			course=float(gpsdata[8])
			# send values to redis
			redis.set('gps.speed',speed)
			redis.set('gps.course',course)
			# debug
			print "speed = "+str(speed)+" course = "+str(course)
		elif gpsdata[0] == "$GPVTG":
			allInfoReaded |= 0x10
		else:
			# debug
			print "Unknown GPS data "
		lineReaded += 1
	


if __name__ == '__main__':
	redis = redis.StrictRedis(host='localhost', port=6379, db=0)
	GPS = serial.Serial('/dev/ttyAMA0',9600, timeout=2, rtscts=1)
	try:
		while True:
			recvGPS(GPS,redis)
	except:
		print "Unexpected error:", sys.exc_info()
	finally:
		GPS.close()

