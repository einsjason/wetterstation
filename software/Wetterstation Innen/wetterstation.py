#!/usr/bin/env python3

import signal
import sys
import smbus2
import time
import json
import pathlib

# Sensor-Librarys
from i2c.lib_bme280 import BME280
from i2c.lib_sgp30 import SGP30

from utils.utilities import terminalOutput
from getData import *
from checkData import *
from calculateData import *
from calculateWarnings import *
from exportData import *

SOFTWARE_INFO = {
	"version": "241123",
	"edition": "Innestation"
}

# #############################################################

# Keyboard ISR
def keyboar_isr(sig, frame):
	terminalOutput("Programm wird gestoppt")
	sys.exit(0)

# #############################################################

# Lese Config-Datei
config_file = open(f"{pathlib.Path(__file__).parent.resolve()}/config.json")
config = json.load(config_file)
config_file.close()

# Initialisiere I²C Bus
IICbus = smbus2.SMBus(config['i2c_bus'])
time.sleep(1)

print(terminalUtils.reset, end = "")
print(f"{terminalUtils.colors['yellow']}  \\  /      {terminalUtils.colors['blue']} __      __   _   _              _        _   _ ")
print(f"{terminalUtils.colors['yellow']}_ /‾‾{terminalUtils.colors['gray']}.-.    {terminalUtils.colors['blue']} \ \    / /__| |_| |_ ___ _ _ __| |_ __ _| |_(_)___ _ _ ")
print(f"{terminalUtils.colors['yellow']}  \\_{terminalUtils.colors['gray']}(   ).  {terminalUtils.colors['blue']}  \ \/\/ / -_)  _|  _/ -_) '_(_-<  _/ _` |  _| / _ \ ' \ ")
print(f"{terminalUtils.colors['yellow']}  /{terminalUtils.colors['gray']}(___(__) {terminalUtils.colors['blue']}   \_/\_/\___|\__|\__\___|_| /__/\__\__,_|\__|_\___/_||_| ")
print(f"{terminalUtils.colors['blue']}    / / /   {terminalUtils.colors['blue']} {SOFTWARE_INFO['edition']} - Version: {SOFTWARE_INFO['version']}")
print()
print(f"{terminalUtils.colors['gray2']}Drücken Sie >>Strg + C<<, um das Programm zu beenden.")
print(f"{terminalUtils.reset}---------------------------------------------------------------------")

# Variablen
sensors = {}
sensor_data = {}
data = {
	"data": {},
	"ref": {},
	"env_data": {
		"raw_data": {},
		"other_data": {},
		"calibration": {}
	},
	"sensors": {},
	"startup": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())
}
info = {
	"localisation": {},
	"name": config['stationinfo']['name']
}
warnings = []

# Initialisiere Sensoren
try: # BME 280
	sensors['bme280'] = BME280(IICbus, int(config['i2c']['bme280']['addr'], 16))
	data['sensors']['bme280'] = True
except:
	sensors['bme280'] = None
	data['sensors']['bme280'] = False

try: # SGP 30
	sensors['sgp30'] = SGP30(IICbus, int(config['i2c']['sgp30']['addr'], 16))
	data['sensors']['sgp30'] = True
except:
	sensors['sgp30'] = None
	data['sensors']['sgp30'] = False

# Setze Keyboard ISR
signal.signal(signal.SIGINT, keyboar_isr)
# Setze systemd stop ISR
signal.signal(signal.SIGTERM, keyboar_isr)

terminalOutput("Programm gestartet", False)

# Initialisiereung SGP 30
terminalOutput("CO2-Sensor wird initialisiert")
baseline = None
try:
	# Lese Environment-Datei
	env_file = open(config['output']['local'] + config['output']['filename']['environment'])
	env = json.load(env_file)
	env_file.close()
	if(isinstance(env["environment"]["calibration"]["co2_baseline"], int) and isinstance(env["environment"]["calibration"]["voc_baseline"], int)):
		baseline = (env["environment"]["calibration"]["co2_baseline"], env["environment"]["calibration"]["voc_baseline"])
except:
	pass

try:
	sensors['sgp30'].initialise(baseline)
	data['sensors']['sgp30'] = True
except:
	data['sensors']['sgp30'] = False
terminalOutput("CO2-Sensor initialisiert")

# Hauptprogramm
minute_last = -1

# Aktuelle Daten
getData(sensors, sensor_data, data, config)
checkData(sensor_data, data, config)
calculateData(data, config, sensors)
calculateWarnings(data, warnings)

while(True):
	minute = time.localtime().tm_min
	
	if(minute % 5 == 0 and minute != minute_last):
		minute_last = minute

		# Aktuelle Daten
		getData(sensors, sensor_data, data, config)
		checkData(sensor_data, data, config)
		calculateData(data, config, sensors)
		calculateWarnings(data, warnings)

		exportData(data, warnings, info, config, SOFTWARE_INFO)

	time.sleep(10)