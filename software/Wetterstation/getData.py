import time
import os
import RPi.GPIO as GPIO
from utils.utilities import analogToTemp, getMostFrequent, terminalOutput
from utils.suninfo import Suninfo

def getData(sensors, sensor_data, data, config):
	terminalOutput("Sensordaten werden gelesen")

	# Luftsensor BME 280
	try:
		bme280_values = sensors['bme280'].read()
		sensor_data['temp'] = round(bme280_values[0], 1)
		sensor_data['bme_humidity'] = int(bme280_values[1])
		sensor_data['bme_pressure'] = round(bme280_values[2], 1)
		data['sensors']['bme280'] = True
	except:
		sensor_data['temp'] = None
		sensor_data['bme_humidity'] = None
		sensor_data['bme_pressure'] = None
		data['sensors']['bme280'] = False

	# Luftsensor LPS 35 HW
	try:
		lps_values = sensors['lps35hw'].read()
		sensor_data['lps_temp'] = round(lps_values[0], 1)
		sensor_data['pressure'] = round(lps_values[1], 1)
		data['sensors']['lps35hw'] = True
	except:
		sensor_data['lps_temp'] = None
		sensor_data['pressure'] = None
		data['sensors']['lps35hw'] = False

	# Luftsensor SHT 31-D
	try:
		sht31d_values = sensors['sht31d'].read()
		sensor_data['sht_temp'] = round(sht31d_values[0], 1)
		sensor_data['humidity'] = int(sht31d_values[1])
		data['sensors']['sht31d'] = True
	except:
		sensor_data['sht_temp'] = None
		sensor_data['humidity'] = None
		data['sensors']['sht31d'] = False

	# IR Temperatursensor MLX 90614
	try:
		mlx90614_values = sensors['mlx90614'].read()
		sensor_data['sky_temp'] = round(mlx90614_values[1], 1)
		sensor_data['mlx_temp'] = round(mlx90614_values[0], 1)
		data['sensors']['mlx90614'] = True
	except:
		sensor_data['sky_temp'] = None
		sensor_data['mlx_temp'] = None
		data['sensors']['mlx90614'] = False

	# Pluviometer
	if((time.time() * 1000.0) - sensor_data['rain_last_time'] >= config["calibration"]["pluviometer_reset_time"] and sensor_data['rain_intensity'] > 0.0): # Letzte Messung zu lange her?
		sensor_data['rain_intensity'] = 0.0

	# Tropfensensor
	sensor_data['rain'] = sensor_data['rain_stream']
	if(GPIO.input(config['gpio']['drop_sensor'])):
		sensor_data['rain_stream'] = False
	elif(sensor_data['rain_stream'] == False and GPIO.input(config['gpio']['drop_sensor']) == False):
		sensor_data['rain'] = True
		sensor_data['rain_stream'] = True

	# Windfahne
	sensor_data['wind_dir'] = getMostFrequent(sensor_data['wind_dir_stream'])
	sensor_data['wind_dir_stream'] = []

	# Lichtsensor TSL 2591
	try:
		sensor_data['brightness'] = int(round(sensors['tsl2591'].read() * config['calibration']['tsl2591_housing_correction_factor'], 0))
		data['sensors']['tsl2591'] = True
	except:
		sensor_data['brightness'] = None
		data['sensors']['tsl2591'] = False

	# Feinstaubsensor PMSA003I
	try:
		pmsa003i_values = sensors['pmsa003i'].read()
		sensor_data['pm1'] = int(round(pmsa003i_values[3], 0))
		sensor_data['pm2_5'] = int(round(pmsa003i_values[4], 0))
		sensor_data['pm10'] = int(round(pmsa003i_values[5], 0))
		data['sensors']['pmsa003i'] = True
	except:
		sensor_data['pm1'] = None
		sensor_data['pm2_5'] = None
		sensor_data['pm10'] = None
		data['sensors']['pmsa003i'] = False

	# Analog In
	try:
		# Gehäuse Temperatursensor
		sensor_data['housing_temp'] = int(round(analogToTemp(sensors['ads1015'].read(config['analog_gpio']['housing_temp']))))

		data['sensors']['ads1015'] = True
	except:
		# Gehäuse Temperatursensor
		sensor_data['housing_temp'] = None

		data['sensors']['ads1015'] = False

	# CPU-Temperatur
	sensor_data['cpu_temp'] = int(round(float(os.popen("vcgencmd measure_temp").readline().replace("temp=","").replace("'C",""))))

	# Sonnendaten
	now = time.localtime(time.time())
	data['astro'] = {
		"sunrise": Suninfo.getSunrise(config['stationinfo']['lat'], config['stationinfo']['lon'], now),
		"sunset": Suninfo.getSunset(config['stationinfo']['lat'], config['stationinfo']['lon'], now),
		"twilight_begin": Suninfo.getTwilightBegin(config['stationinfo']['lat'], config['stationinfo']['lon'], now),
		"twilight_end": Suninfo.getTwilightEnd(config['stationinfo']['lat'], config['stationinfo']['lon'], now)
	}

	terminalOutput("Sensordaten gelesen")