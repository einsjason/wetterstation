#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import time

##############################################################

#Keyboard ISR
def keyboar_isr(sig=None, frame=None):
	GPIO.cleanup()
	sys.exit(0)

#ISR
time_last = 0
min_time = float("inf")
avg_time = None

def isr(channel:int=None):
	global time_last, params, typ, min_time, avg_time, timeout

	v = GPIO.input(channel)
	if v == params[typ][2]:
		t = int((time.time_ns() - time_last) // 1e6)
		if t >= timeout:
			min_time = min(min_time, t)
			if avg_time == None:
				avg_time = t
			else: 
				avg_time += t
				avg_time /= 2
			print(channel, v, t, min_time, avg_time)
			time_last = time.time_ns()
		else:
			print(channel, v, t)

#Setze Keyboard ISR
signal.signal(signal.SIGINT, keyboar_isr)

#Parameter
pin = int(input("Pin: "))
typ = input("Typ (R ising, F alling): ")
timeout = int(input("Timeout: "))

params = {
	"R": (GPIO.PUD_DOWN, GPIO.RISING, True),
	"F": (GPIO.PUD_UP, GPIO.FALLING, False)
}

#GPIO
GPIO.setmode(GPIO.BCM)

if typ in params:
	GPIO.setup(pin, GPIO.IN, pull_up_down = params[typ][0])
	GPIO.add_event_detect(pin, params[typ][1], callback = isr)
else:
	raise ValueError("Unbekannter Typ")

while(True):
	pass