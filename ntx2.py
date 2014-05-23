#!/usr/bin/python

import os
import time
import redis
import sys
import RPi.GPIO as GPIO

payload_name="DAVCLA"
bits = 7
stopbits = 2
baud = 50
baud_delay=(1000000/baud)
data_pin=12



def sendBit(bit):
	GPIO.output(data_pin, bit)
	time.sleep(baud_delay/1000000.0)

def sendByte(byte):
	byte=ord(byte)
	sendBit(False) #start bit
	for i in range(0,bits):
		if byte & 1:
			sendBit(True)
		else:
			sendBit(False)
		byte=byte>>1
	for i in range(0,stopbits):
		sendBit(True) # stop bit

def sendNTX2(data):
	for byte in data:
		sendByte(byte)

def getFrame(redis,count):
	gps_time=redis.get('gps.utc_time')
	gps_latitude=redis.get('gps.latitude')
	gps_longitude=redis.get('gps.longitude')
	gps_altitude=redis.get('gps.altitude')
	gps_speed=redis.get('gps.speed')
	gps_course=redis.get('gps.course')
	gps_sat=redis.get('gps.satellites.used')
	data="$$%s,%d,%s:%s:%s,%7.5lf,%7.5lf,%05.5u,%d,%d,%d,%3.1f,%3.1f,%3.1f" % (
		payload_name,
		count,
		str(gps_time)[0:2],str(gps_time)[2:4],str(gps_time)[4:6],
		float(gps_latitude),
		float(gps_longitude),
		float(gps_altitude),
		int((float(gps_speed) * 13) / 7),
		int(float(gps_course)),
		int(gps_sat),
		0,
		0,
		0
	)
	return data

def computeCRC(data):
	CRC = 0xffff
	xPolynomial = 0x1021
	for i in range(2,len(data)):
		CRC ^= (ord(data[i]) << 8)
		for j in range(0,8):
			if CRC & 0x8000:
				CRC = (CRC << 1) ^ 0x1021
			else:
				CRC <<= 1
	data+="*"
	data+="%X" % ((CRC >> 12) & 15)
	data+="%X" % ((CRC >> 8) & 15)
	data+="%X" % ((CRC >> 4) & 15)
	data+="%X" % (CRC & 15)
	data+="\n"
	return data

if __name__ == '__main__':
	count=0
	try:
		# Setup GPIO
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(data_pin, GPIO.OUT)
		# Connect to redis
		redis = redis.StrictRedis(host='localhost', port=6379, db=0)
		# Main loop
		while True:
			data = getFrame(redis,count)
			data = computeCRC(data)
			print data
			sendNTX2(data)
			count+=1
	finally:  
		GPIO.cleanup()
