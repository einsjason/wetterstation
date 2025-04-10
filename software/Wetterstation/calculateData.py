import time
import RPi.GPIO as GPIO

from utils.utilities import *

def calculateData(data, config, sensors):		
	terminalOutput("Daten werden berechnet")

	time_now = int(time.time())
	planned_last_reset = (time_now // 86400) * 86400

	data['time'] = time_now

	# Lese Daten aus EEPROM
	try:
		time_last = int(sensors['eeprom'].get(config['eeprom_addr']['time']))
		reset_last = sensors['eeprom'].get(config['eeprom_addr']['reset'])
		reset_1h_last = sensors['eeprom'].get(config['eeprom_addr']['reset_hour'])

		temp_min = sensors['eeprom'].get(config['eeprom_addr']['t_min'])
		temp_max = sensors['eeprom'].get(config['eeprom_addr']['t_max'])

		rain = sensors['eeprom'].get(config['eeprom_addr']['rain'])
		rain_1h = sensors['eeprom'].get(config['eeprom_addr']['rain_1h'])
		rain_intensity_max_1h = sensors['eeprom'].get(config['eeprom_addr']['rain_i_max_1h'])

		wind_speed_max_1h = sensors['eeprom'].get(config['eeprom_addr']['wind_s_max_1h'])
		wind_gust_max_1h = sensors['eeprom'].get(config['eeprom_addr']['wind_g_max_1h'])
		wind_speed_max_1d = sensors['eeprom'].get(config['eeprom_addr']['wind_s_max_1d'])
		wind_gust_max_1d = sensors['eeprom'].get(config['eeprom_addr']['wind_g_max_1d'])
		wind_speed_avg_1d = sensors['eeprom'].get(config['eeprom_addr']['wind_s_avg_1d'])

		pressure_last = sensors['eeprom'].get(config['eeprom_addr']['pressure_0h'])
		pressure_last_1h = sensors['eeprom'].get(config['eeprom_addr']['pressure_1h'])
		pressure_last_2h = sensors['eeprom'].get(config['eeprom_addr']['pressure_2h'])
		pressure_last_3h = sensors['eeprom'].get(config['eeprom_addr']['pressure_3h'])

		pm1_24h_avg = sensors['eeprom'].get(config['eeprom_addr']['pm1_24h_avg'])
		pm2_5_24h_avg = sensors['eeprom'].get(config['eeprom_addr']['pm2_5_24h_avg'])
		pm10_24h_avg = sensors['eeprom'].get(config['eeprom_addr']['pm10_24h_avg'])
		pm1_24h_avg_count = sensors['eeprom'].get(config['eeprom_addr']['pm1_24h_avg_count'])
		if(pm1_24h_avg_count == None):
			pm1_24h_avg_count = 0
		pm2_5_24h_avg_count = sensors['eeprom'].get(config['eeprom_addr']['pm2_5_24h_avg_count'])
		if(pm2_5_24h_avg_count == None):
			pm2_5_24h_avg_count = 0
		pm10_24h_avg_count = sensors['eeprom'].get(config['eeprom_addr']['pm10_24h_avg_count'])
		if(pm10_24h_avg_count == None):
			pm10_24h_avg_count = 0

		sunshine_1h = sensors['eeprom'].get(config['eeprom_addr']['sunshine_1h'])
		sunshine_1d = sensors['eeprom'].get(config['eeprom_addr']['sunshine_1d'])
		sunshine_interval_start = sensors['eeprom'].get(config['eeprom_addr']['sunshine_interval_start'])

		sensors['eeprom'].update(config['eeprom_addr']['time'], time_now)
		
		if(isNumeric(reset_last)):
			data['last_reset'] = reset_last
		else:
			data['last_reset'] = time_now
			sensors['eeprom'].update(config['eeprom_addr']['reset'], time_now)

		if(isNumeric(reset_1h_last)):
			data['last_reset_1h'] = reset_1h_last
		else:
			data['last_reset_1h'] = time_now
			sensors['eeprom'].update(config['eeprom_addr']['reset_hour'], time_now)

		data['sensors']['24lc32'] = True
	except:
		time_last = 0
		reset_last = 0
		reset_1h_last = 0

		temp_min = None
		temp_max = None

		rain = None
		rain_1h = None
		rain_intensity_max_1h = None

		wind_speed_max_1h = None
		wind_gust_max_1h = None
		wind_speed_max_1d = None
		wind_gust_max_1d = None
		wind_speed_avg_1d = None

		pressure_last = None
		pressure_last_1h = None
		pressure_last_2h = None
		pressure_last_3h = None

		pm1_24h_avg = None
		pm2_5_24h_avg = None
		pm10_24h_avg = None
		pm1_24h_avg_count = 0
		pm2_5_24h_avg_count = 0
		pm10_24h_avg_count = 0

		sunshine_1h = None
		sunshine_1d = None
		sunshine_interval_start = None
		
		data['last_reset'] = time_now
		data['last_reset_1h'] = time_now

		data['sensors']['24lc32'] = False

	# Tageszeit
	data['data']['day_time'] = data['time'] >= time.mktime(data['astro']['sunrise']) and data['time'] <= time.mktime(data['astro']['sunset'])
	data['env_data']['other_data']['day_time2'] = data['time'] >= time.mktime(data['astro']['sunrise']) + 900 and data['time'] <= time.mktime(data['astro']['sunset']) - 900 # 15 min nach Sonnenaufgang bis 15 min vor Sonnenuntergang

	# Temperatur
	if(isNumeric(data['data']['temp'])):
		if(isNumeric(temp_min)):
			data['data']['temp_min'] = min(round(temp_min, 1), data['data']['temp'])
		else:
			data['data']['temp_min'] = data['data']['temp']

		try:
			sensors['eeprom'].update(config['eeprom_addr']['t_min'], data['data']['temp_min'])
		except:
			pass

		if(isNumeric(temp_max)):
			data['data']['temp_max'] = max(round(temp_max, 1), data['data']['temp'])
		else:
			data['data']['temp_max'] = data['data']['temp']
			
		try:
			sensors['eeprom'].update(config['eeprom_addr']['t_max'], data['data']['temp_max'])
		except:
			pass
	else:
		data['data']['temp_min'] = None
		data['data']['temp_max'] = None

	# Luftdruck
	if(time.localtime().tm_min % 60 == 0):
		if(isNumeric(pressure_last_2h)): # Schiebe 2 auf 3
			pressure_last_3h = pressure_last_2h
			try:
				sensors['eeprom'].update(config['eeprom_addr']['pressure_3h'], pressure_last_3h)
			except:
				pass
		else:
			pressure_last_3h = None
			try:
				sensors['eeprom'].clear(config['eeprom_addr']['pressure_3h'])
			except:
				pass

		if(isNumeric(pressure_last_1h)): # Schiebe 1 auf 2
			pressure_last_2h = pressure_last_1h
			try:
				sensors['eeprom'].update(config['eeprom_addr']['pressure_2h'], pressure_last_2h)
			except:
				pass
		else:
			pressure_last_2h = None
			try:
				sensors['eeprom'].clear(config['eeprom_addr']['pressure_2h'])
			except:
				pass

		if(isNumeric(pressure_last)): # Schiebe 0 auf 1
			pressure_last_1h = pressure_last
			try:
				sensors['eeprom'].update(config['eeprom_addr']['pressure_1h'], pressure_last_1h)
			except:
				pass
		else:
			pressure_last_1h = None
			try:
				sensors['eeprom'].clear(config['eeprom_addr']['pressure_1h'])
			except:
				pass

		if(isNumeric(data['data']['pressure'])): #Schiebe aktuell auf 0
			pressure_last = data['data']['pressure']
			try:
				sensors['eeprom'].update(config['eeprom_addr']['pressure_0h'], pressure_last)
			except:
				pass
		else:
			pressure_last = None
			try:
				sensors['eeprom'].clear(config['eeprom_addr']['pressure_0h'])
			except:
				pass
	else:
		pass
			
	if(isNumeric(pressure_last) and isNumeric(pressure_last_1h)):
		data['data']['pressure_trend_1h'] = round(pressure_last - pressure_last_1h, 1)
	else:
		data['data']['pressure_trend_1h'] = None

	if(isNumeric(pressure_last) and isNumeric(pressure_last_3h)):
		data['data']['pressure_trend_3h'] = round(pressure_last - pressure_last_3h, 1)
	else:
		data['data']['pressure_trend_3h'] = None

	# Solarstahlung und Sonnenschein
	max_irradiance, treshold = sunshineThreshold(config['stationinfo']['lat'], config['stationinfo']['lon'], time.gmtime(), config['calibration']['sunshine_threshold_factor'])
	data['ref']['irradiance_treshold_factor'] = config['calibration']['sunshine_threshold_factor']
	data['env_data']['raw_data']['irradiance_treshold'] = treshold
	data['env_data']['raw_data']['max_irradiance'] = max_irradiance

	if(isNumeric(data['data']['brightness'])):
		data['data']['irradiance'] = int(round(brightnessToIrradiance(data['data']['brightness']), -1))
		uvi = uvIndex(data['data']['irradiance'])
		data['data']['uv_index'] = uvi[0]
		data['data']['uv_index_description'] = uvi[1]

		if(data['data']['day_time']):
			data['data']['sunshine'] = sunshine(data['data']['irradiance'], treshold)
		else:
			data['data']['sunshine'] = False
	else:
		data['data']['irradiance'] = None
		data['data']['uv_index'] = None
		data['data']['uv_index_description'] = None
		data['data']['sunshine'] = None

	# Bewölkung
	if(isNumeric(data['data']['temp']) and isNumeric(data['data']['sky_temp'])):
		data['data']['cloud'] = int(round(tempDiffToCloudiness(data['data']['temp'], data['data']['sky_temp']), 1) * 100)
		if data['env_data']['other_data']['day_time2'] and isBoolean(data['data']['sunshine']) and not data['data']['sunshine']:  # Korrektur bei fehlendem Sonnenschein ab 15 min nach Sonnenaufgang bis 15 min vor Sonnenuntergang
			data['data']['cloud'] = max(data['data']['cloud'], 40)
		elif data['env_data']['other_data']['day_time2'] and isBoolean(data['data']['sunshine']) and data['data']['sunshine']: # Korrektur bei Sonnenschein
			data['data']['cloud'] = min(data['data']['cloud'], 60)
	else:
		data['data']['cloud'] = None

	# Niederschlag
	if(isBoolean(data['data']['rain']) and isNumeric(data['data']['cloud'])):
		if(data['data']['rain'] and data['data']['cloud'] == 0):
			data['data']['rain'] = False

	if(isBoolean(data['data']['rain']) and isNumeric(data['data']['rain_intensity'])):
		if(data['data']['rain'] and data['data']['rain_intensity'] == 0.0):
			data['data']['rain_intensity'] = 0.1

	# Niederschlagsintensität
	if(isNumeric(data['data']['rain_intensity']) and isNumeric(rain_intensity_max_1h)):
		data['data']['rain_intensity_max_1h'] = max(round(rain_intensity_max_1h, 1), data['data']['rain_intensity'])
		try:
			sensors['eeprom'].update(config['eeprom_addr']['rain_i_max_1h'], data['data']['rain_intensity_max_1h'])
		except:
			pass
	else:
		data['data']['rain_intensity_max_1h'] = None
		try:
			sensors['eeprom'].update(config['eeprom_addr']['rain_i_max_1h'], 0.0)
		except:
			pass

	# Niederschlagsmenge
	if(isNumeric(data['data']['rain_total']) and isNumeric(rain)):
		data['data']['rain_total'] += round(rain, 2)
		try:
			sensors['eeprom'].update(config['eeprom_addr']['rain'], data['data']['rain_total'])
		except:
			pass
	else:
		try:
			sensors['eeprom'].update(config['eeprom_addr']['rain'], 0.0)
		except:
			pass

	if(isNumeric(data['data']['rain_total_1h']) and isNumeric(rain_1h) and time_last >= planned_last_reset):
		data['data']['rain_total_1h'] += round(rain_1h, 2)
		try:
			sensors['eeprom'].update(config['eeprom_addr']['rain_1h'], data['data']['rain_total_1h'])
		except:
			pass
	else:
		try:
			sensors['eeprom'].update(config['eeprom_addr']['rain_1h'], 0.0)
		except:
			pass

	#Sonnenscheindauer
	if(isNumeric(sunshine_interval_start)): #Messintervall Länge
		interval_length = min(round((time_now - sunshine_interval_start) / 60), 5)
	else:
		interval_length = 5

	try:
		sensors['eeprom'].update(config['eeprom_addr']['sunshine_interval_start'], time_now)
	except:
		pass

	if(isBoolean(data['data']['sunshine']) and isNumeric(sunshine_1h)): #Stundenwert
		data['data']['sunshine_1h'] = sunshine_1h + (data['data']['sunshine'] * interval_length)
		try:
			sensors['eeprom'].update(config['eeprom_addr']['sunshine_1h'], data['data']['sunshine_1h'])
		except:
			pass
	else:
		data['data']['sunshine_1h'] = None
		try:
			sensors['eeprom'].update(config['eeprom_addr']['sunshine_1h'], 0)
		except:
			pass

	if(isBoolean(data['data']['sunshine']) and isNumeric(sunshine_1d)): #Tageswert
		data['data']['sunshine_1d'] = sunshine_1d + (data['data']['sunshine'] * interval_length) # mal Anzahl Minuten Execute-Intervall
		try:
			sensors['eeprom'].update(config['eeprom_addr']['sunshine_1d'], data['data']['sunshine_1d'])
		except:
			pass
	else:
		data['data']['sunshine_1d'] = None
		try:
			sensors['eeprom'].update(config['eeprom_addr']['sunshine_1d'], 0)
		except:
			pass

	# Windchill
	if(isNumeric(data['data']['temp']) and isNumeric(data['data']['wind_gust'])):
		data['data']['windchill'] = round(windchill(data['data']['temp'], data['data']['wind_gust']), 1)
	else:
		data['data']['windchill'] = None

	# Hitzeindex
	if(isNumeric(data['data']['temp']) and isNumeric(data['data']['humidity'])):
		if(data['data']['temp'] >= 22):
			data['data']['heat_index'] = round(heatIndex(data['data']['temp'], data['data']['humidity']), 1)
		else:
			data['data']['heat_index'] = False
	else:
		data['data']['heat_index'] = None

	# Gefühlte Temperatur
	if(isNumeric(data['data']['windchill']) and data['data']['temp'] < 22):
		data['data']['felt_temp'] = data['data']['windchill']
	elif(isNumeric(data['data']['heat_index']) and data['data']['temp'] >= 22):
		data['data']['felt_temp'] = data['data']['heat_index']
	else:
		data['data']['felt_temp'] = None

	# Taupunkt
	if(isNumeric(data['data']['temp']) and isNumeric(data['data']['humidity'])):
		data['data']['dew_point'] = round(dewPoint(data['data']['temp'], data['data']['humidity']), 1)
	else:
		data['data']['dew_point'] = None

	# Absolute Luftfeuchte
	if(isNumeric(data['data']['temp']) and isNumeric(data['data']['humidity'])):
		data['data']['absolute_humidity'] = round(absoluteHumidity(data['data']['temp'], data['data']['humidity']), 1)
	else:
		data['data']['absolute_humidity'] = None
		
	# Meereshöhendruck
	if(isNumeric(data['data']['pressure']) and isNumeric(data['data']['temp'])):
		data['data']['sealevel_pressure'] = round(sealevelPressure(data['data']['temp'], data['data']['pressure'], config['stationinfo']['alt']), 1)
	else:
		data['data']['sealevel_pressure'] = None

	# Windgeschwindigkeiten
	if(isNumeric(data['data']['wind_speed'])):
		data['data']['wind_speed_bft'] = kmhToBft(data['data']['wind_speed'])[0]
	else:
		data['data']['wind_speed_bft']= None
		
	if(isNumeric(data['data']['wind_speed']) and isNumeric(wind_speed_max_1h)): #max-Werte 1h
		data['data']['wind_speed_max_1h'] = max(round(wind_speed_max_1h, 1), data['data']['wind_speed'])
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_s_max_1h'], data['data']['wind_speed_max_1h'])
		except:
			pass
	else:
		data['data']['wind_speed_max_1h'] = None
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_s_max_1h'], 0.0)
		except:
			pass

	if(isNumeric(data['data']['wind_speed']) and isNumeric(wind_speed_max_1d)): #max-Werte 1d
		data['data']['wind_speed_max_1d'] = max(round(wind_speed_max_1d, 1), data['data']['wind_speed'])
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_s_max_1d'], data['data']['wind_speed_max_1d'])
		except:
			pass
	else:
		data['data']['wind_speed_max_1d'] = None
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_s_max_1d'], 0.0)
		except:
			pass

	if(isNumeric(data['data']['wind_speed'])): #avg-Werte 1d
		if(isNumeric(wind_speed_avg_1d)):
			data['data']['wind_speed_avg_1d'] = round((wind_speed_avg_1d + data['data']['wind_speed']) / 2, 1)
		else:
			data['data']['wind_speed_avg_1d'] = data['data']['wind_speed']
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_s_avg_1d'], data['data']['wind_speed_avg_1d'])
		except:
			pass
	else:
		data['data']['wind_speed_avg_1d'] = None

	# Windböengeschwindigkeiten
	if(isNumeric(data['data']['wind_gust'])):
		data['data']['wind_gust_bft'] = kmhToBft(data['data']['wind_gust'])[0]
	else:
		data['data']['wind_gust_bft'] = None

	if(isNumeric(data['data']['wind_gust']) and isNumeric(wind_gust_max_1h)): #max-Werte 1h
		data['data']['wind_gust_max_1h'] = max(round(wind_gust_max_1h, 1), data['data']['wind_gust'])
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_g_max_1h'], data['data']['wind_gust_max_1h'])
		except:
			pass
	else:
		data['data']['wind_gust_max_1h'] = None
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_g_max_1h'], 0.0)
		except:
			pass

	if(isNumeric(data['data']['wind_gust']) and isNumeric(wind_gust_max_1d)): #max-Werte 1d
		data['data']['wind_gust_max_1d'] = max(round(wind_gust_max_1d, 1), data['data']['wind_gust'])
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_g_max_1d'], data['data']['wind_gust_max_1d'])
		except:
			pass
	else:
		data['data']['wind_gust_max_1d'] = None
		try:
			sensors['eeprom'].update(config['eeprom_addr']['wind_g_max_1d'], 0.0)
		except:
			pass

	# Windrichtung
	if(isNumeric(data['data']['wind_dir'])):
		data['data']['wind_dir_str'] = dirToStr(data['data']['wind_dir'])[0]
	else:
		data['data']['wind_dir_str'] = None

	# Windböenrichtung
	if(isNumeric(data['env_data']['other_data']['wind_gust_dir'])):
		data['env_data']['other_data']['wind_gust_dir_str'] = dirToStr(data['env_data']['other_data']['wind_gust_dir'])[0]
	else:
		data['env_data']['other_data']['wind_gust_dir_str'] = None

	# Windbeschreibung
	if(isNumeric(data['data']['wind_dir']) and isNumeric(data['data']['wind_gust'])):
		if(data['data']['wind_gust_bft'] > 0): #wenn wind_gust numeric ist, ist wind_gust_bft auch numeric
			data['data']['wind_description'] = kmhToBft(data['data']['wind_gust'])[1] + " aus " + dirToStr(data['data']['wind_dir'])[1]
		else:
			data['data']['wind_description'] = kmhToBft(data['data']['wind_gust'])[1]
	elif(isNumeric(data['data']['wind_dir'])):
		data['data']['wind_description'] = dirToStr(data['data']['wind_dir'])[1]
	elif(isNumeric(data['data']['wind_gust'])):
		data['data']['wind_description'] = kmhToBft(data['data']['wind_gust'])[1]
	else:
		data['data']['wind_description'] = None

	# Feinstaub
	if(isNumeric(data['data']['humidity'])):
		pm_growth_factor = pmHumidityGrowthFactor(data['data']['humidity'])
	else:
		pm_growth_factor = None
	data['env_data']['raw_data']['pm_growth_factor'] = pm_growth_factor

	if(isNumeric(data['data']['pm1'])):
		if(isNumeric(pm_growth_factor)): # Feuchtekorrektur PM1
			data['data']['pm1'] = int(round(pmHumidityCorrection(data['data']['pm1'], pm_growth_factor) ,0))

		if(isNumeric(pm1_24h_avg)): # Feinstaubmittelwert PM1
			pm1_24h_avg += data['data']['pm1']
		else:
			pm1_24h_avg = data['data']['pm1']
		pm1_24h_avg_count += 1
		data['data']['pm1_avg'] = int(round(pm1_24h_avg  / pm1_24h_avg_count, 0))

		try:
			sensors['eeprom'].update(config['eeprom_addr']['pm1_24h_avg'], pm1_24h_avg)
			sensors['eeprom'].update(config['eeprom_addr']['pm1_24h_avg_count'], pm1_24h_avg_count)
		except:
			pass
	else:
		data['data']['pm1_avg'] = None

	if(isNumeric(data['data']['pm2_5'])):
		if(isNumeric(pm_growth_factor)): # Feuchtekorrektur PM2,5
			data['data']['pm2_5'] = int(round(pmHumidityCorrection(data['data']['pm2_5'], pm_growth_factor) ,0))

		if(isNumeric(pm2_5_24h_avg)): # Feinstaubmittelwert PM2,5
			pm2_5_24h_avg += data['data']['pm2_5']
		else:
			pm2_5_24h_avg = data['data']['pm2_5']
		pm2_5_24h_avg_count += 1
		data['data']['pm2_5_avg'] = int(round(pm2_5_24h_avg  / pm2_5_24h_avg_count, 0))

		try:
			sensors['eeprom'].update(config['eeprom_addr']['pm2_5_24h_avg'], pm2_5_24h_avg)
			sensors['eeprom'].update(config['eeprom_addr']['pm2_5_24h_avg_count'], pm2_5_24h_avg_count)
		except:
			pass
	else:
		data['data']['pm2_5_avg'] = None

	if(isNumeric(data['data']['pm10'])):
		if(isNumeric(pm_growth_factor)): # Feuchtekorrektur PM10
			data['data']['pm10'] = int(round(pmHumidityCorrection(data['data']['pm10'], pm_growth_factor) ,0))

		if(isNumeric(pm10_24h_avg)): # Feinstaubmittelwert PM10
			pm10_24h_avg += data['data']['pm10']
		else:
			pm10_24h_avg = data['data']['pm10']
		pm10_24h_avg_count += 1
		data['data']['pm10_avg'] = int(round(pm10_24h_avg  / pm10_24h_avg_count, 0))

		try:
			sensors['eeprom'].update(config['eeprom_addr']['pm10_24h_avg'], pm10_24h_avg)
			sensors['eeprom'].update(config['eeprom_addr']['pm10_24h_avg_count'], pm10_24h_avg_count)
		except:
			pass
	else:
		data['data']['pm10_avg'] = None

	if(isNumeric(data['data']['pm2_5']) and isNumeric(data['data']['pm10'])): # Feinstaubindex
		aqi2_5 = aqiIndex(data['data']['pm2_5'], "pm2_5")
		aqi10 = aqiIndex(data['data']['pm10'], "pm10")
		if(aqi10[0] >= aqi2_5[0]):
			data['data']['aqi'] = aqi10[0]
			data['data']['aqi_description'] = aqi10[1]
		else:
			data['data']['aqi'] = aqi2_5[0]
			data['data']['aqi_description'] = aqi2_5[1]
	else:
		data['data']['aqi'] = None
		data['data']['aqi_description'] = None

	if(isNumeric(data['data']['pm2_5_avg']) and isNumeric(data['data']['pm10_avg'])): # Feinstaubindex Mittelwert
		aqi2_5 = aqiIndex(data['data']['pm2_5_avg'], "pm2_5")
		aqi10 = aqiIndex(data['data']['pm10_avg'], "pm10")
		if(aqi10[0] >= aqi2_5[0]):
			data['data']['aqi_avg'] = aqi10[0]
			data['data']['aqi_avg_description'] = aqi10[1]
		else:
			data['data']['aqi_avg'] = aqi2_5[0]
			data['data']['aqi_avg_description'] = aqi2_5[1]
	else:
		data['data']['aqi_avg'] = None
		data['data']['aqi_avg_description'] = None

	# Icon und Wetterbeschreibung
	if(isNumeric(data['data']['rain_intensity']) and isNumeric(data['data']['cloud']) and isNumeric(data['data']['temp']) and isBoolean(data['data']['day_time'])):
		if data['data']['cloud'] <= 20: # Bewölkung
			data['data']['weather_icon_simple'] = "clear"
			data['data']['weather_icon'] = "clear"
			if data['data']['day_time']:
				data['data']['weather_description'] = "Sonnig"
			else:
				data['data']['weather_description'] = "Klar"
		elif data['data']['cloud'] >= 80:
			data['data']['weather_icon_simple'] = "cloudy"
			data['data']['weather_icon'] = "cloudy"
			data['data']['weather_description'] = "Bedeckt"
		else:
			data['data']['weather_icon_simple'] = "partly-cloudy"
			data['data']['weather_icon'] = "partly-cloudy"
			data['data']['weather_description'] = "Bewölkt"
		
		if(data['data']['rain']): # Niederschlag
			if(data['data']['weather_icon'] == "clear"):
				data['data']['weather_icon'] = "partly-cloudy"

			data['data']['weather_description'] = rainIntensityLevel(data['data']['rain_intensity'])[1]

			if(data['data']['temp'] < 0):
				data['data']['weather_icon_simple'] = "snow"
				data['data']['weather_icon'] += "-snow"
				data['data']['weather_description'] += "/Schneefall"
				data['data']['condition'] = "snow" if not 'condition' in data['data'] or data['data']['condition'] != "thunderstorm" else "thunderstorm"
			else:
				data['data']['weather_icon_simple'] = "rain"
				data['data']['weather_icon'] += "-rain"
				data['data']['condition'] = "rain" if not 'condition' in data['data'] or data['data']['condition'] != "thunderstorm" else "thunderstorm"
		else: # trocken
			if(data['data']['humidity'] >= 95 and data['data']['sky_temp'] >= data['data']['temp'] - 0.1): # Nebel
				data['data']['weather_icon_simple'] = "fog"
				data['data']['weather_icon'] = "fog"
				data['data']['weather_description'] = "Nebel"
				data['data']['condition'] = "fog" if not 'condition' in data['data'] or data['data']['condition'] != "thunderstorm" else "thunderstorm"
			else:
				data['data']['condition'] = "dry" if not 'condition' in data['data'] or data['data']['condition'] != "thunderstorm" else "thunderstorm"

		if(data['data']['day_time']):
			data['data']['weather_icon_simple'] += "-day"
			data['data']['weather_icon'] += "-day"
		else:
			data['data']['weather_icon_simple'] += "-night"
			data['data']['weather_icon'] += "-night"
	else:
		data['data']['weather_icon_simple'] = None
		data['data']['weather_icon'] = None
		data['data']['weather_description'] = None
		data['data']['condition'] = None

	# Lüfter
	fan = False
	if(isNumeric(data['env_data']['housing_temp']) and data['env_data']['housing_temp'] >= config['fan']['housing_temp']):
		fan = True
	data['env_data']['fan'] = fan
	GPIO.output(config['gpio']['fan'], fan)

	# Lüfter Luftsensor
	fan_air_sensor = False
	if(isBoolean(data['data']['sunshine']) and data['data']['sunshine']):
		fan_air_sensor = True
	data['env_data']['fan_air_sensor'] = fan_air_sensor
	GPIO.output(config['gpio']['fan_air_sensor'], fan_air_sensor)

	# SHT31-D Heater
	heater = False
	if(isNumeric(data['data']['humidity']) and data['data']['humidity'] >= config['calibration']['sht31d_heater']['value'] and time.localtime().tm_min % 5 == 0):
		heater = True
	data['env_data']['sht_heater'] = heater
	try:
		sensors['sht31d'].setHeater(heater)
	except IOError:
		pass

	terminalOutput("Daten berechnet")