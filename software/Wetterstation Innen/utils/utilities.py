import math
import time
from utils.terminalUtils import *

def terminalOutput(data:str, override_last_line:bool=True):
	output = time.strftime("[%H:%M:%S]", time.localtime()) + " - " + data
	if(override_last_line):
		print(terminalUtils.prevline + terminalUtils.clearline + output)
	else:
		print(output)

def isI2cDevicePresent(bus, address:int, raise_error:bool=False) -> bool:
	try:
		bus.read_byte_data(address, 0)
		return True
	except OSError:
		if raise_error:
			raise OSError
		return False

def isInRange(value:float, value_min:float=None, value_max:float=None) -> bool:
	if(isNumeric(value)):
		if(isNumeric(value_min) and value < value_min):
			return False
		if(isNumeric(value_max) and value > value_max):
			return False
		return True
	else:
		return False

def isNumeric(value:any) -> bool:
	return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool) and value != None

def isBoolean(value:any) -> bool:
	return isinstance(value, bool) and value != None

def isString(value:any) -> bool:
	return isinstance(value, str) and value != None

def valueMap(v:float, in_min:float, in_max:float, out_min:float, out_max:float) -> float:
    return (v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def valueAvg(value1:float, value2:float) -> float:
	return (value1 + value2) / 2

def rreplace(string:str, old:str, new:str) -> str:
	return (string[::-1].replace(old[::-1], new[::-1], 1))[::-1]
	
def dewPoint(temp:float, humidity:float) -> float:
	f = (17.271 * temp) / (237.7 + temp) + math.log(humidity / 100.0)
	return (237.7 * f) / (17.271 - f)

def windchill(temp:float, wind_speed:float) -> float:
	return 13.12 + (0.6215 * temp) + (((0.3965 * temp) - 11.37) * (wind_speed ** 0.16))

def heatIndex(temp:float, humidity:float) -> float:
	return  -8.784695 + 1.61139411 * temp + 2.338549 * humidity - 0.14611605 * temp * humidity - 0.012308094 * (temp ** 2) - 0.016424828 * (humidity ** 2) + 0.002211732 * (temp ** 2) * humidity + 0.00072546 * temp * (humidity ** 2) - 0.000003582 * (temp ** 2) * (humidity ** 2)

def absoluteHumidity(temp:float, humidity:float) -> float:
	# Gaskonstanten
	if(temp >= 0):
		a = 7.5
		b = 237.3
	else:
		a = 7.6
		b = 240.7

	e_s = 6.1078 * math.exp(((a * temp) / (b + temp)) / math.log10(math.e)) #Sättingungsdampfdruck
	return 1000 * (18.016 / 8314.3) * ((humidity * e_s) / (temp + 273.15))

def relativeHumidity(temp: float, absolute_humidity: float) -> float:
	# Gaskonstanten
	if temp >= 0:
		a = 7.5
		b = 237.3
	else:
		a = 7.6
		b = 240.7

	e_s = 6.1078 * math.exp(((a * temp) / (b + temp)) / math.log10(math.e)) #Sättingungsdampfdruck
	return (absolute_humidity * (temp + 273.15)) / (1000 * (18.016 / 8314.3) * e_s)

def gaussian(x:float, u:float, t:float) -> float:
	return math.exp(-((x - u) * (x - u)) / (2 * t * t))

def tempIndex(temp:float, temp_mean:float, temp_coeff:float) -> tuple:
	temp_g = gaussian(temp, temp_mean, temp_coeff)
	if (temp_g < 0.8):
		if (temp > temp_mean):
			temp_value = 1
		else:
			temp_value = -1
	else:
		temp_value = 0

	temp_index = max(math.ceil((1 - temp_g) * 5), 1)
	if(temp < temp_mean):
		temp_index = -temp_index
	if(temp_index == 1 or temp_index == -1):
		temp_desc = "Optimal"
	else:
		temp_desc = "zu " + ("Warm" if temp_value > 0 else "Kalt")
	return (temp_index, temp_desc, temp_value)

def humidityIndex(humidity:float, humidity_mean:float, humidity_coeff:float) -> tuple:
	humidity_g = gaussian(humidity, humidity_mean, humidity_coeff)
	if (humidity_g < 0.8):
		if (humidity > humidity_mean):
			humidity_value = 1
		else:
			humidity_value = -1
	else:
		humidity_value = 0

	humidity_index = max(math.ceil((1 - humidity_g) * 5), 1)
	if(humidity < humidity_mean):
		humidity_index = -humidity_index
	if(humidity_index == 1):
		humidity_desc = "Optimal"
	else:
		humidity_desc = "zu " + ("Feucht" if humidity_value > 0 else "Trocken")
	return (humidity_index, humidity_desc, humidity_value)

def airDensity(temp:float, pressure:float) -> float:
	return (pressure * 100) / (287.05 * (temp + 273.15))

def co2Index(value:float, param:str="co2") -> tuple: # https://de.elv.com/media/image/d6/a0/00/luftqualitaet_tabelle.jpg, https://cdn.soselectronic.com/novinky/obr/obr2055_p1732.jpg
	limits = {
		"co2": [600, 1000, 1500, 1800],
		"voc": [65, 220, 660, 2200]
	}
	desc = ["Sehr Gut", "Gut", "Mäßig", "Schlecht", "Schlecht"]
	
	if param in limits:
		i = 1
		for l in limits[param]:
			if value <= l:
				return (i, desc[i - 1])
			i += 1
		return (i, desc[i - 1])
	else:
		return None
	
def getIndexDescription(index:int) -> str:
	desc = ["Sehr Gut", "Gut", "Mäßig", "Schlecht", "Schlecht"]
	if(index >= 1 and index <= 5):
		return desc[index - 1]
	else:
		raise ValueError