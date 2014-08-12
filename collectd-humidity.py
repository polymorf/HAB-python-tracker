#!/usr/bin/python
import sys

import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 22

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
	print 'PUTVAL "Raspi/exec-humidity/temperature" interval=10.000 N:%0.1f' % (temperature)
	print 'PUTVAL "Raspi/exec-humidity/gauge-humidity" interval=10.000 N:%0.1f' % (humidity)
