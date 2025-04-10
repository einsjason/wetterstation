import time
import math

from utils.utilities import *

def calculateData(data, config, sensors):		
	terminalOutput("Daten werden berechnet")

	time_now = int(time.time())

	data['time'] = time_now

	# Windchill
	if(isNumeric(data['data']['temp'])):
		data['data']['windchill'] = round(windchill(data['data']['temp'], 0), 1)
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

	# CO2-Index
	if(isNumeric(data['data']['co2'])):
		co2_index = co2Index(data['data']['co2'], "co2")
		data['data']['co2_index'] = co2_index[0]
		data['data']['co2_index_description'] = co2_index[1]
	else:
		data['data']['co2_index'] = None
		data['data']['co2_index_description'] = None

	# VOC-Index
	if(isNumeric(data['data']['voc'])):
		voc_index = co2Index(data['data']['voc'], "voc")
		data['data']['voc_index'] = voc_index[0]
		data['data']['voc_index_description'] = voc_index[1]
	else:
		data['data']['voc_index'] = None
		data['data']['voc_index_description'] = None

	data['ref']['temp_mean'] = config['calibration']['comfort_temperature_mean']
	data['ref']['humidity_mean'] = config['calibration']['comfort_humidity_mean']

	# Temperaturindex
	if(isNumeric(data['data']['temp'])):
		temp_index = tempIndex(data['data']['temp'], config['calibration']['comfort_temperature_mean'], config['calibration']['comfort_temperature_coeff'])

		data['data']['temp_index'] = temp_index[0]
		data['data']['temp_index_description'] = temp_index[1]
		data['data']['temp_index_deviation'] = temp_index[2]
	else:
		data['data']['temp_index'] = None
		data['data']['temp_index_description'] = None
		data['data']['temp_index_deviation'] = None

	# Luftfeuchtigkeitsindex
	if(isNumeric(data['data']['humidity'])):
		humidity_index = humidityIndex(data['data']['humidity'], config['calibration']['comfort_humidity_mean'], config['calibration']['comfort_humidity_coeff'])

		data['data']['humidity_index'] = humidity_index[0]
		data['data']['humidity_index_description'] = humidity_index[1]
		data['data']['humidity_index_deviation'] = humidity_index[2]
	else:
		data['data']['humidity_index'] = None
		data['data']['humidity_index_description'] = None
		data['data']['humidity_index_deviation'] = None

	# Comfort
	index = 0
	index_desc = []
	index_count = 0
	if(isNumeric(data['data']['temp_index'])):
		index += abs(data['data']['temp_index'])
		if(data['data']['temp_index_deviation'] != 0):
			index_desc.append(data['data']['temp_index_description'])
		index_count += 1
	if(isNumeric(data['data']['humidity_index'])):
		index += abs(data['data']['humidity_index'])
		if(data['data']['humidity_index_deviation'] != 0):
			index_desc.append(data['data']['humidity_index_description'])
		index_count += 1
	if(isNumeric(data['data']['co2_index'])):
		index += data['data']['co2_index']
		if(data['data']['co2_index'] >= 3):
			index_desc.append("zu hohe CO₂-Konzentration")
		index_count += 1
	if(index_count > 0):
		index = math.ceil(index / index_count)
		data['data']['comfort_index'] = index
		index_desc = ", ".join(index_desc)
		index_desc = rreplace(index_desc, ", ", " und ")
		if(index_desc != ""):
			data['data']['comfort_index_description'] = getIndexDescription(index) + " - " + index_desc
		else:
			data['data']['comfort_index_description'] = getIndexDescription(index)
		data['data']['comfort_index_description_short'] = getIndexDescription(index)
	else:
		data['data']['comfort_index'] = None
		data['data']['comfort_index_description'] = None
		data['data']['comfort_index_description_short'] = None

	terminalOutput("Daten berechnet")