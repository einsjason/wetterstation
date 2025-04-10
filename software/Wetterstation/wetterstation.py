#!/usr/bin/env python3

import signal
import sys
import pathlib
import smbus2
import time
import json
import RPi.GPIO as GPIO

# Sensor-Librarys
from i2c.lib_bme280 import BME280
from i2c.lib_lps35hw import LPS35HW
from i2c.lib_sht31d import SHT31D
from i2c.lib_ads1015 import ADS1015
from i2c.lib_mlx90614 import MLX90614
from i2c.lib_tlv493d import TLV493D
from i2c.lib_tsl2591 import TSL2591
from i2c.lib_pmsa003i import PMSA003I

from eeprom import EEPROM

from utils.utilities import terminalOutput
from getData import *
from checkData import *
from calculateData import *
from calculateWarnings import *
from exportData import *
from reset import *

SOFTWARE_INFO = {
	"version": "250101",
	"edition": "Aussenstation"
}

# #############################################################

# Keyboard ISR
def keyboar_isr(sig=None, frame=None):
	terminalOutput("Programm wird gestoppt")
	GPIO.cleanup()
	sys.exit(0)

# Anemometer ISR
def wind_isr(channel):
	global sensor_data, timer_anemometer, config

	if(GPIO.input(channel)):
		millis = time.time() * 1000.0
		t = millis - timer_anemometer

		if(t >= config['calibration']['interrupt_timeout_anemometer']):
			val_per_pulse = config['calibration']['val_per_pulse_anemometer'] # Radius: 0,068 m | Umfang: 0,42725660 m -> /2 (da 2 Impulse pro Umdrehung) -> 0,2136 m
				
			speed = (val_per_pulse / (t / 1000.0)) * 3.6 # km/h (*3,6 für m/s -> km/h)
			timer_anemometer = millis

			sensor_data['wind_speed_stream'] += speed
			sensor_data['wind_speed_stream_count'] += 1

# Anemometer
def wind_sr(): # Nach wind_dir_sr() ausführen
	global sensor_data, config

	if(sensor_data["wind_speed_stream_count"] > 0):
		sensor_data["wind_speed"] = round(sensor_data["wind_speed_stream"] / sensor_data["wind_speed_stream_count"], 1)
	else:
		sensor_data["wind_speed"] = 0.0

	if(sensor_data["wind_speed"] > sensor_data['wind_gust']): #max(sensor_data['wind_gust'], sensor_data["wind_speed"])
		sensor_data["wind_gust"] = sensor_data["wind_speed"]
		if(len(sensor_data['wind_dir_stream']) > 0):
			sensor_data["wind_gust_dir"] = sensor_data['wind_dir_stream'][-1]
		else:
			sensor_data["wind_gust_dir"] = None

	sensor_data['wind_speed_stream'] = 0
	sensor_data['wind_speed_stream_count'] = 0

# Windfahne
def wind_dir_sr():
	global sensor_data, sensors, config

	try:
		sensor_data['wind_dir_stream'].append(correctDir(magneticToDir(sensors['tlv493d'].read(), (config['calibration']['tlv493d_max_magnetic'], config['calibration']['tlv493d_max_magnetic']))))
		data['sensors']['tlv493d'] = True
	except:
		sensor_data['wind_dir'] = None
		data['sensors']['tlv493d'] = False

# Pluviometer ISR
def rain_isr(channel):
	global sensor_data, timer_pluviometer, config

	if(GPIO.input(channel)):
		millis = time.time() * 1000.0
		t = millis - timer_pluviometer

		if(t >= config['calibration']['interrupt_timeout_pluviometer']):
			val_per_pulse = config['calibration']['val_per_pulse_pluviometer'] # Wippe: 0,002873 l berechnet, 0,0015 l gemessen | Radius Trichter: 0,05 m | Fläche Trichter: 0,00785 m² -> 0,38 l/m² berechnet, 0.19 l/m² berechnet (1 mm = 1 l/m²)
			
			intensity = val_per_pulse / (t / 3.6e+6) # mm/h (/3,6*10^6 für ms -> h)
			timer_pluviometer = millis

			sensor_data['rain_intensity'] = max(intensity, 0.1)
			sensor_data['rain_total'] += val_per_pulse
			sensor_data['rain_total_1h'] += val_per_pulse
			sensor_data['rain_last_time'] = millis

# Tropfensensor ISR
def drop_isr(channel):
	global sensor_data
	
	if(not GPIO.input(channel)):
		sensor_data['rain_stream'] = True

##############################################################

timer_anemometer = 0
timer_pluviometer = 0

# Lese Config-Datei
config_file = open(f"{pathlib.Path(__file__).parent.resolve()}/config.json")
config = json.load(config_file)
config_file.close()

# Initialisiere I²C Bus
IICbus =  smbus2.SMBus(config['i2c_bus'])
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
sensor_data = {
	"wind_speed_stream": 0,
	"wind_speed_stream_count": 0,
	"wind_speed": 0,
	"wind_gust": 0,
	"wind_dir_stream": [],
	"wind_dir": 0,
	"wind_gust_dir": 0,
	"rain_intensity": 0.0,
	"rain_total": 0.0,
	"rain_total_1h": 0.0,
	"rain_last_time": 0,
	"rain_stream": False
}
data = {
	"data": {
		"temp_min": None,
		"temp_max": None
	},
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
	"localisation": {
		"lat": config['stationinfo']['lat'],
		"lon": config['stationinfo']['lon'],
		"alt": config['stationinfo']['alt'],
		"warncell_id": config['stationinfo']['warncell_id']
	},
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

try: # LPS 35 HW
	sensors['lps35hw'] = LPS35HW(IICbus, int(config['i2c']['lps35hw']['addr'], 16))
	data['sensors']['lps35hw'] = True
except:
	sensors['lps35hw'] = None
	data['sensors']['lps35hw'] = False

try: # SHT 31-D
	sensors['sht31d'] = SHT31D(IICbus, int(config['i2c']['sht31d']['addr'], 16))
	data['sensors']['sht31d'] = True
except:
	sensors['sht31d'] = None
	data['sensors']['sht31d'] = False

try: # MLX 90614
	sensors['mlx90614'] = MLX90614(IICbus, int(config['i2c']['mlx90614']['addr'], 16))
	data['sensors']['mlx90614'] = True
except:
	sensors['mlx90614'] = None
	data['sensors']['mlx90614'] = False

try: # TSL 2591
	sensors['tsl2591'] = TSL2591(IICbus, int(config['i2c']['tsl2591']['addr'], 16))
	data['sensors']['tsl2591'] = True
except:
	sensors['tsl2591'] = None
	data['sensors']['tsl2591'] = False

try: # TLV 493D
	isI2cDevicePresent(IICbus, int(config['i2c']['tlv493d']['addr'], 16), True)
	sensors['tlv493d'] = TLV493D(IICbus, int(config['i2c']['tlv493d']['addr'], 16))
	data['sensors']['tlv493d'] = True
except:
	try: # fallback Addresse
		sensors['tlv493d'] = TLV493D(IICbus, int(config['i2c']['tlv493d']['fallback_addr'], 16))
		data['sensors']['tlv493d'] = True
	except:
		sensors['tlv493d'] = None
		data['sensors']['tlv493d'] = False

try: # PMSA003I
	sensors['pmsa003i'] = PMSA003I(IICbus, int(config['i2c']['pmsa003i']['addr'], 16))
	data['sensors']['pmsa003i'] = True
except:
	sensors['pmsa003i'] = None
	data['sensors']['pmsa003i'] = False

#try: # AS3935
#	sensors['as3935'] = None #AS3935(IICbus, int(config['i2c']['as3935']['addr'], 16))
#	data['sensors']['as3935'] = False #True
#except:
#	sensors['as3935'] = None
#	data['sensors']['as3935'] = False

try: # ADS 1015
	sensors['ads1015'] = ADS1015(IICbus, int(config['i2c']['ads1015']['addr'], 16))
	data['sensors']['ads1015'] = True
except:
	sensors['ads1015'] = None
	data['sensors']['ads1015'] = False

try: # 24LC32
	sensors['eeprom'] = EEPROM(IICbus, int(config['i2c']['24lc32']['addr'], 16))
	data['sensors']['24lc32'] = True
except:
	sensors['eeprom'] = None
	data['sensors']['24lc32'] = False

# Setze Keyboard ISR
signal.signal(signal.SIGINT, keyboar_isr)
# Setze systemd stop ISR
signal.signal(signal.SIGTERM, keyboar_isr)

# GPIO
GPIO.setmode(GPIO.BCM)

# Lüfter
GPIO.setup(config['gpio']['fan'], GPIO.OUT)
GPIO.output(config['gpio']['fan'], False)

# Lüfter Luftsensor
GPIO.setup(config['gpio']['fan_air_sensor'], GPIO.OUT)
GPIO.output(config['gpio']['fan_air_sensor'], False)

# GPIO Anemomter ISR
GPIO.setup(config['gpio']['anemometer'], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(config['gpio']['anemometer'], GPIO.RISING, callback = wind_isr)

# GPIO Pluviometer ISR
GPIO.setup(config['gpio']['pluviometer'], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(config['gpio']['pluviometer'], GPIO.RISING, callback = rain_isr)

# GPIO Drop Sensor ISR
GPIO.setup(config['gpio']['drop_sensor'], GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(config['gpio']['drop_sensor'], GPIO.FALLING, callback = drop_isr)

terminalOutput("Programm gestartet", False)

# Hauptprogramm
minute_last = -1
hour_last = time.localtime().tm_hour
day_last = time.localtime().tm_mday

sht_heater_last = -1

# aktuelle Daten
getData(sensors, sensor_data, data, config)
checkData(sensor_data, data, config)
calculateData(data, config, sensors)
calculateWarnings(data, warnings)

while(True):
	wind_dir_sr()
	wind_sr()

	minute = time.localtime().tm_min

	if((minute + config['calibration']['sht31d_heater']['cooldown']) % 5 == 0 and minute != sht_heater_last):
		sht_heater_last = minute

		try:
			sensors['sht31d'].setHeater(False)
		except IOError:
			pass
	
	if(minute % 5 == 0 and minute != minute_last):
		minute_last = minute

		hour = time.localtime().tm_hour
		if(hour != hour_last):
			hour_last = hour

			# stündliche Daten
			exportData(data, warnings, info, config, SOFTWARE_INFO, "H")
			resetDataHour(config, sensors)

		day = time.localtime().tm_mday
		if(day != day_last):
			day_last = day
			
			# tägliche Daten
			exportData(data, warnings, info, config, SOFTWARE_INFO, "D")
			resetData(config, sensors)
		
		# aktuelle Daten
		getData(sensors, sensor_data, data, config)
		checkData(sensor_data, data, config)
		calculateData(data, config, sensors)
		calculateWarnings(data, warnings)

		exportData(data, warnings, info, config, SOFTWARE_INFO, "C")

	time.sleep(10)