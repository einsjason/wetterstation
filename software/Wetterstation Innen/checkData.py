from utils.utilities import isInRange, terminalOutput

def checkData(sensor_data, data, config):
	terminalOutput("Sensordaten werden überprüft")

	if(isInRange(sensor_data['temp'], -40, 85) and isInRange(sensor_data['humidity'], 0, 100) and isInRange(sensor_data['pressure'], 300, 1200)):
		data['data']['temp'] = sensor_data['temp']
		data['data']['humidity'] = sensor_data['humidity']
		data['env_data']['other_data']['pressure'] = sensor_data['pressure']
	else:
		data['data']['temp'] = None
		data['data']['humidity'] = None
		data['env_data']['other_data']['pressure'] = None
		data['sensors']['bme280'] = False

	if(isInRange(sensor_data['co2'], 400, 60000) and isInRange(sensor_data['voc'], 0, 60000)):
		data['data']['co2'] = round(sensor_data['co2'], -1)
		data['data']['voc'] = round(sensor_data['voc'], -1)
	else:
		data['data']['co2'] = None
		data['data']['voc'] = None

	#CPU Temperatur
	data['env_data']['cpu_temp'] = sensor_data['cpu_temp']

	#####################################################################

	terminalOutput("Sensordaten überprüft")