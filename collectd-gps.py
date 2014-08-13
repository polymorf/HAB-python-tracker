#!/usr/bin/python

import os
import time
import redis
import sys


redis = redis.StrictRedis(host='localhost', port=6379, db=0)
gps_latitude=redis.get('gps.latitude')
gps_longitude=redis.get('gps.longitude')
gps_altitude=redis.get('gps.altitude')
gps_speed=redis.get('gps.speed')
gps_course=redis.get('gps.course')
gps_sat=redis.get('gps.satellites.used')

print 'PUTVAL "Raspi/exec-gps/gauge-latitude" interval=10.000 N:'+gps_latitude
print 'PUTVAL "Raspi/exec-gps/gauge-longitude" interval=10.000 N:'+gps_longitude
print 'PUTVAL "Raspi/exec-gps/gauge-altitude" interval=10.000 N:'+gps_altitude
print 'PUTVAL "Raspi/exec-gps/gauge-speed" interval=10.000 N:'+gps_speed
print 'PUTVAL "Raspi/exec-gps/gauge-course" interval=10.000 N:'+gps_course
print 'PUTVAL "Raspi/exec-gps/gauge-sat" interval=10.000 N:'+gps_sat
