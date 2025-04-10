import json
import time
import urllib.request
import urllib.parse
import urllib.error

from utils.utilities import terminalOutput
from utils.timezone_linux import *

def exportData(data, warnings, info, config, SOFTWARE_INFO, type:str = "C"):
	def writeLocalFile(path:str, content:str) -> None:
		file = open(path, "w")
		file.write(content)
		file.close()

	def readLocalFile(path:str) -> str:
		file = open(path, "r")
		content = file.read()
		file.close()
		return content

	def sendToServer(url:str, content:dict) -> any:
		post_data = urllib.parse.urlencode(content, doseq=True)
		post_data = post_data.encode("ascii")

		request = urllib.request.Request(url, post_data)
		try:
			f = urllib.request.urlopen(request)
			return f.read(), True
		except urllib.error.HTTPError as err:
			return err.read(), err.code
		except:
			return "", 0
		
	##############################################################################

	terminalOutput("Daten werden exportiert (" + type + ")")

	info['localisation']['timezone'] = getTimezoneContinentCity()
	tz = time.strftime("%z", time.localtime())
	tz = (-1 if tz[:1] == "-" else 1, int(tz[1:3]), int(tz[3:]))
	info['localisation']['timezone_offset'] = ((tz[1] * 3600) + (tz[2] * 60)) * tz[0]

	if(type == "C"): #aktuell
		weatherdata = {
			"time": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['time'])),
			"last_reset": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['last_reset'])),
			"last_reset_1h": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['last_reset_1h'])),
			"data": data['data'],
			"ref": data['ref'],
			"warnings": warnings,
			"astro": {
				"sunrise": time.strftime("%Y-%m-%dT%H:%M:%S%z", data['astro']['sunrise']),
				"sunset": time.strftime("%Y-%m-%dT%H:%M:%S%z", data['astro']['sunset']),
				"twilight_begin": time.strftime("%Y-%m-%dT%H:%M:%S%z", data['astro']['twilight_begin']),
				"twilight_end": time.strftime("%Y-%m-%dT%H:%M:%S%z", data['astro']['twilight_end'])
			}
		} | info

		writeLocalFile(config['output']['local'] + "weatherdata.json", json.dumps(weatherdata))

		enviromentdata = {
			"time": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['time'])),
			"environment": data['env_data'],
			"info": {
				"version": SOFTWARE_INFO['version'],
				"started": data['startup']
			},
			"sensor_status": data['sensors']
		}

		writeLocalFile(config['output']['local'] + "environment.json", json.dumps(enviromentdata))

		sendToServer(config['output']['remote'], {
			"weatherdata.json": json.dumps(weatherdata)
		})

	elif(type == "H"): #stündlich
		try:
			weatherdata_hourly = json.loads(readLocalFile(config['output']['local'] + "weatherdata_hourly.json"))['data']
		except:
			weatherdata_hourly = []

		if(len(weatherdata_hourly) == 0 or time.strptime(weatherdata_hourly[0]['time'], "%Y-%m-%dT%H:%M:%S%z").tm_hour != time.localtime().tm_hour):
			weatherdata_h = {
				"time": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['time'])),
				"last_reset": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['last_reset'])),
				"last_reset_1h": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['last_reset_1h'])),
				"data": {
					"temp": data['data']['temp'],
					"humidity": data['data']['humidity'],
					"pressure": data['data']['pressure'],
					"sky_temp": data['data']['sky_temp'],
					"wind_speed_max_1h": data['data']['wind_speed_max_1h'],
					"wind_gust_max_1h": data['data']['wind_gust_max_1h'],
					"wind_dir": data['data']['wind_dir'],
					"rain": data['data']['rain'],
					"rain_total": data['data']['rain_total'],
					"rain_total_1h": data['data']['rain_total_1h'],
					"rain_intensity_max_1h": data['data']['rain_intensity_max_1h'],
					"brightness": data['data']['brightness'],
					"cloud": data['data']['cloud'],
					"irradiance": data['data']['irradiance'],
					"day_time": data['data']['day_time'],
					"felt_temp": data['data']['felt_temp'],
					"dew_point": data['data']['dew_point'],
					"absolute_humidity": data['data']['absolute_humidity'],
					"sealevel_pressure": data['data']['sealevel_pressure'],
					"wind_dir_str": data['data']['wind_dir_str'],
					"pm1": data['data']['pm1'],
					"pm2_5": data['data']['pm2_5'],
					"pm10": data['data']['pm10'],
					"aqi": data['data']['aqi'],
					"aqi_description": data['data']['aqi_description'],
					"sunshine_1h": data['data']['sunshine_1h'],
					"sunshine": data['data']['sunshine']
				}
			}

			while(len(weatherdata_hourly) > config['output']['num_hourly'] - 1):
				weatherdata_hourly.pop(len(weatherdata_hourly) - 1)

			weatherdata_hourly.insert(0, weatherdata_h)
			weatherdata_hourly_ = {
				"data": weatherdata_hourly,
				"ref": data['ref']
			} | info

			writeLocalFile(config['output']['local'] + "weatherdata_hourly.json", json.dumps(weatherdata_hourly_))

			sendToServer(config['output']['remote'], {
				"weatherdata_hourly.json": json.dumps(weatherdata_hourly_)
			})

	elif(type == "D"): #täglich
		try:
			weatherdata_daily = json.loads(readLocalFile(config['output']['local'] + "weatherdata_daily.json"))['data']
		except:
			weatherdata_daily = []

		if(len(weatherdata_daily) == 0 or time.strptime(weatherdata_daily[0]['time'], "%Y-%m-%dT%H:%M:%S%z").tm_mday != time.localtime().tm_mday):
			weatherdata_d = {
				"time": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['time'])),
				"last_reset": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['last_reset'])),
				"data": {
					"temp_min": data['data']['temp_min'],
					"temp_max": data['data']['temp_max'],
					"wind_speed_max_1d": data['data']['wind_speed_max_1d'],
					"wind_gust_max_1d": data['data']['wind_gust_max_1d'],
					"wind_speed_avg_1d": data['data']['wind_speed_avg_1d'],
					"rain_total": data['data']['rain_total'],
					"pm1_avg": data['data']['pm1_avg'],
					"pm2_5_avg": data['data']['pm2_5_avg'],
					"pm10_avg": data['data']['pm10_avg'],
					"aqi_avg": data['data']['aqi_avg'],
					"aqi_avg_description": data['data']['aqi_avg_description'],
					"sunshine_1d": data['data']['sunshine_1d']
				}
			}

			while(len(weatherdata_daily) > config['output']['num_daily'] - 1):
				weatherdata_daily.pop(len(weatherdata_daily) - 1)

			weatherdata_daily.insert(0, weatherdata_d)
			weatherdata_daily_ = {
				"data": weatherdata_daily,
				"ref": data['ref']
			} | info
			weatherdata_daily__ = weatherdata_d | {
				"ref": data['ref']
			} | info

			writeLocalFile(config['output']['local'] + "weatherdata_daily.json", json.dumps(weatherdata_daily_))

			writeLocalFile(config['output']['local'] + "daily/" + time.strftime("%Y-%m-%d", time.localtime(data['time'])) + ".json", json.dumps(weatherdata_daily__))

			sendToServer(config['output']['remote'], {
				"weatherdata_daily.json": json.dumps(weatherdata_daily_),
				"daily/" + time.strftime("%Y-%m-%d", time.localtime(data['time'])) + ".json": json.dumps(weatherdata_daily__)
			})

	terminalOutput("Daten exportiert (" + type + ")")
