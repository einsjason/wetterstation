import os
from utils.utilities import terminalOutput

def getData(sensors, sensor_data, data, config):
	terminalOutput("Sensordaten werden gelesen")

	#Luftsensor BME 280
	try:
		bme280_values = sensors['bme280'].read()
		sensor_data['temp'] = round(bme280_values[0] + config['calibration']['temp_housing_correction_offset'], 1)
		sensor_data['humidity'] = int(bme280_values[1])
		sensor_data['pressure'] = round(bme280_values[2], 1)
		data['sensors']['bme280'] = True
	except:
		sensor_data['temp'] = None
		sensor_data['humidity'] = None
		sensor_data['pressure'] = None
		data['sensors']['bme280'] = False

	# CO2-Sensor SGP30
	try:
		sgp30_values = sensors['sgp30'].read()
		sensor_data['co2'] = int(round(sgp30_values[0], 0))
		sensor_data['voc'] = int(round(sgp30_values[1], 0))
		data['sensors']['sgp30'] = True
	except:
		sensor_data['co2'] = None
		sensor_data['voc'] = None
		data['sensors']['sgp30'] = False

	try:
		baselines = sensors['sgp30'].getBaseline()
		data['env_data']['calibration'] = {
			"co2_baseline": baselines[0],
			"voc_baseline": baselines[1]
		}
	except:
		data['env_data']['calibration'] = {
			"co2_voc_baseline": None,
			"voc_baseline": None
		}

	#CPU Temperatur
	sensor_data['cpu_temp'] = int(round(float(os.popen("vcgencmd measure_temp").readline().replace("temp=","").replace("'C",""))))

	terminalOutput("Sensordaten gelesen")