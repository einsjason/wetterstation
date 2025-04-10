import json
import time
import urllib.request
import urllib.parse
import urllib.error

from utils.utilities import terminalOutput
from utils.timezone_linux import *

def exportData(data, warnings, info, config, SOFTWARE_INFO, type:str = "C"):
	def writeLocalFile(path, content):
		file = open(path, "w")
		file.write(content)
		file.close()

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

	terminalOutput("Daten werden exportiert")

	info['localisation']['timezone'] = getTimezoneContinentCity()
	tz = time.strftime("%z", time.localtime())
	tz = (-1 if tz[:1] == "-" else 1, int(tz[1:3]), int(tz[3:]))
	info['localisation']['timezone_offset'] = ((tz[1] * 3600) + (tz[2] * 60)) * tz[0]

	weatherdata = {
		"time": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(data['time'])),
		"data": data['data'],
		"ref": data['ref'],
		"warnings": warnings
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

	terminalOutput("Daten exportiert")
