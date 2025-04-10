from utils.utilities import isInRange, terminalOutput, isBoolean

def checkData(sensor_data, data, config):
	terminalOutput("Sensordaten werden überprüft")

	# Luftsensor BME 280
	if(isInRange(sensor_data['temp'], -40, 85) and isInRange(sensor_data['bme_humidity'], 0, 100) and isInRange(sensor_data['bme_pressure'], 300, 1200)):
		data['data']['temp'] = sensor_data['temp']
		data['env_data']['other_data']['bme_pressure'] = sensor_data['bme_pressure']
		data['env_data']['other_data']['bme_humidity'] = sensor_data['bme_humidity']
	else:
		data['data']['temp'] = None
		data['env_data']['other_data']['bme_pressure'] = None
		data['env_data']['other_data']['bme_humidity'] = None
		data['sensors']['bme280'] = False

	# Luftsensor LPS 35 HW
	if(isInRange(sensor_data['pressure'], 260, 1260)): # and isInRange(sensor_data['lps_temp'], -40, 85)
		data['env_data']['other_data']['lps_temp'] = sensor_data['lps_temp']
		data['data']['pressure'] = sensor_data['pressure']
	else:
		data['env_data']['other_data']['lps_temp'] = None
		data['data']['pressure'] = None
		data['sensors']['lps35hw'] = False

	# Luftsensor SHT 31-D
	if(isInRange(sensor_data['sht_temp'], -40, 125) and isInRange(sensor_data['humidity'], 0, 100)):
		data['data']['humidity'] = sensor_data['humidity']
		data['env_data']['other_data']['sht_temp'] = sensor_data['sht_temp']
	else:
		data['data']['humidity'] = None
		data['env_data']['other_data']['sht_temp'] = None
		data['sensors']['sht31d'] = False

	# IR Temperatursensor MLX 90614
	if(isInRange(sensor_data['mlx_temp'], -40, 125) and isInRange(sensor_data['sky_temp'], -70, 380)):
		data['data']['sky_temp'] = sensor_data['sky_temp']
		data['env_data']['other_data']['mlx_temp'] = sensor_data['mlx_temp']
	else:
		data['data']['sky_temp'] = None
		data['env_data']['other_data']['mlx_temp'] = None
		data['sensors']['mlx90614'] = False

	# Anemometer
	if(isInRange(sensor_data['wind_speed'], 0, 100)):
		data['data']['wind_speed'] = round(sensor_data['wind_speed'], 1)
	else:
		data['data']['wind_speed'] = 100

	if(isInRange(sensor_data['wind_gust'], 0, 120)):
		data['data']['wind_gust'] = round(sensor_data['wind_gust'], 1)
	else:
		data['data']['wind_gust'] = 120
	sensor_data['wind_gust'] = 0

	# Windfahne
	if(isInRange(sensor_data['wind_dir'], 0, 359)):
		data['data']['wind_dir'] = round(sensor_data['wind_dir'], 0)
	else:
		data['data']['wind_dir'] = None
		data['sensors']['tlv493d'] = False

	if(isInRange(sensor_data['wind_gust_dir'], 0, 359)):
		data['env_data']['other_data']['wind_gust_dir'] = round(sensor_data['wind_gust_dir'], 0)
	else:
		data['env_data']['other_data']['wind_gust_dir'] = None

	# Tropfensensor
	data['data']['rain'] = sensor_data['rain']
	data['env_data']['raw_data']['rain'] = data['data']['rain']

	# Pluviometer
	if(isInRange(sensor_data['rain_intensity'], 0, 75)):
		data['data']['rain_intensity'] = round(sensor_data['rain_intensity'], 2)
	else:
		data['data']['rain_intensity'] = 75
	data['env_data']['raw_data']['rain_intensity'] = data['data']['rain_intensity']

	if(isInRange(sensor_data['rain_total'], 0)):	
		data['data']['rain_total'] = round(sensor_data['rain_total'], 2)
	else:
		data['data']['rain_total'] = None
	sensor_data['rain_total'] = 0.0

	if(isInRange(sensor_data['rain_total_1h'], 0)):
		data['data']['rain_total_1h'] = round(sensor_data['rain_total_1h'], 2)	
	else:
		data['data']['rain_total_1h'] = None
	sensor_data['rain_total_1h'] = 0.0

	# Lichtsensor TSL 2591
	if(isInRange(sensor_data['brightness'], 0, 88000 * config['calibration']['tsl2591_housing_correction_factor'])):
		data['data']['brightness'] = sensor_data['brightness']
	else:
		data['data']['brightness'] = None
		data['sensors']['tsl2591'] = False

	# Feinstaubsensor PMSA003I
	if(isInRange(sensor_data['pm1'], 0, 1000) and isInRange(sensor_data['pm2_5'], 0, 1000) and isInRange(sensor_data['pm10'], 0, 1000)):
		data['data']['pm1'] = sensor_data['pm1']
		data['data']['pm2_5'] = sensor_data['pm2_5']
		data['data']['pm10'] = sensor_data['pm10']
	else:
		data['data']['pm1'] = None
		data['data']['pm2_5'] = None
		data['data']['pm10'] = None
		data['sensors']['pmsa003i'] = False
	data['env_data']['raw_data']['pm1'] = data['data']['pm1']
	data['env_data']['raw_data']['pm2_5'] = data['data']['pm2_5']
	data['env_data']['raw_data']['pm10'] = data['data']['pm10']

	# Gehäusetemperatur
	if(isInRange(sensor_data['housing_temp'], -50, 150)):
		data['env_data']['housing_temp'] = sensor_data['housing_temp']
	else:
		data['env_data']['housing_temp'] = None

	# CPU-Temperatur
	data['env_data']['cpu_temp'] = sensor_data['cpu_temp']

	#####################################################################

	if(not data['sensors']['bme280'] and data['sensors']['sht31d']):
		data['data']['temp'] = data['env_data']['other_data']['sht_temp']

	#####################################################################

	terminalOutput("Sensordaten überprüft")