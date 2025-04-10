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
	
def analogToTemp(analog_value:int, max_analog_value:int=1659, voltage:float=3.3) -> float:
	return (analog_value * ((voltage * 1000) / max_analog_value) - 500) / 10

def tempDiffToCloudiness(ground_temp:float, sky_temp:float, lower_border:int=5, upper_border:int=20) -> float:
	temp_diff = ground_temp - sky_temp
	if (temp_diff >= upper_border):
		return 0.0
	elif (temp_diff <= lower_border):
		return 1.0
	else:
		return round(valueMap(temp_diff, upper_border, lower_border, 0.0, 1.0), 1)
	
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

def sealevelPressure(temp:float, pressure:float, alt:int) -> float:
	return pressure * (((temp + 273.15) / ((temp + 273.15) + (0.0065 * alt))) ** -5.255) # Temperaturen in Kelvin!

def brightnessToIrradiance(brightness:float) -> float:
	return brightness * 0.0079 # https://essay.utwente.nl/82693/1/86293_Burgt_BA_EEMCS.pdf Seite 66

def uvIndex(irradiance:float) -> int:
	desc = ["Niedrig", "Niedrig", "Niedrig", "Mäßig", "Mäßig", "Mäßig", "Hoch", "Hoch", "Sehr Hoch", "Sehr Hoch", "Sehr Hoch", "Extrem Hoch", "extrem Hoch"]
	i = min(irradiance // 100, 12)
	return (i, desc[i])

def kmhToBft(kmh: float) -> tuple:
	if (kmh == 0):
		return 0, "Windstill"
	elif (kmh < 1.85):
		return 0, "schwacher Wind"
	elif (kmh < 7.41):
		return 1, "schwacher Wind"
	elif (kmh < 12.96):
		return 2, "schwacher Wind"
	elif (kmh < 20.37):
		return 3, "schwacher Wind"
	elif (kmh < 29.63):
		return 4, "mäßiger Wind"
	elif (kmh < 40.74):
		return 5, "mäßiger Wind"
	elif (kmh < 51.86):
		return 6, "starker Wind"
	elif (kmh < 62.97):
		return 7, "starker Wind"
	elif (kmh < 75.93):
		return 8, "stürmischer Wind"
	elif (kmh < 88.9):
		return 9, "Sturm"
	elif (kmh < 103.71):
		return 10, "starker Sturm"
	elif (kmh < 118.53):
		return 11, "orkanartiger Sturm"
	else:
		return 12, "Orkan"

def dirToStr(dir: int) -> tuple:
	dir = dir - (dir // 360) * 360

	if (dir < 11.25):
		return "N", "Nord"
	elif (dir < 33.75):
		return "NNW", "Nordnordost"
	elif (dir < 56.25):
		return "NO", "Nordost"
	elif (dir < 78.75):
		return "ONO", "Ostnordost"
	elif (dir < 101.25):
		return "O", "Ost"
	elif (dir < 123.75):
		return "OSO", "Ostsüdost"
	elif (dir < 146.25):
		return "SO", "Südost"
	elif (dir < 168.75):
		return "SSO", "Südsüdost"
	elif (dir < 191.25):
		return "S", "Süd"
	elif (dir < 213.75):
		return "SSW", "Südsüdwest"
	elif (dir < 236.25):
		return "SW", "Südwest"
	elif (dir < 258.75):
		return "WSW", "Westsüdwest"
	elif (dir < 281.25):
		return "W", "West"
	elif (dir < 303.75):
		return "WNW", "Westnordwest"
	elif (dir < 326.25):
		return "NW", "Nordwest"
	elif (dir < 378.75):
		return "NNW", "Nordnordwest"
	else:
		return "N", "Nord"
	
def correctDir(dir:int, steps:int = 8) -> int:
	dir = dir - (dir // 360) * 360
	resolution = int(round(360 / steps, 0))
	dir += resolution / 2
	dir = (dir // resolution) * resolution
	dir = dir - (dir // 360) * 360
	return dir

def sinCosToDeg(cosX:float, sinY:float) -> float:
	rad = 0.0
	if(cosX >= 0 and sinY >= 0): # 0 - 90
		rad = valueAvg(math.acos(cosX), math.asin(sinY))
	elif(cosX < 0 and sinY >= 0): # 90 - 180
		rad = valueAvg(math.acos(cosX), math.pi - math.asin(sinY))
	elif(cosX < 0 and sinY < 0): # 180 - 270
		rad = 1.5 * math.pi - valueAvg(math.acos(cosX), math.asin(sinY))
	elif(cosX >= 0 and sinY < 0): # 270 - 360
		rad = 2 * math.pi - valueAvg(math.acos(cosX), - math.asin(sinY))
	
	return 360 - math.degrees(rad)
	
def magneticToDir(magnetic:tuple, max_magnetic:tuple) -> int:
	x = magnetic[0] / max_magnetic[0]
	y = magnetic[1] / max_magnetic[1]

	if(x >= 0):
		x = min(1.0, x)
	else:
		x = max(-1.0, x)

	if(y >= 0):
		y = min(1.0, y)
	else:
		y = max(-1.0, y)

	return sinCosToDeg(x, y)

def getMostFrequent(list:list) -> any:
	if(len(list) > 0):
		counter = 0
		element = list[0]
		
		for i in list:
			curr_frequency = list.count(i)
			if(curr_frequency > counter):
				counter = curr_frequency
				element = i
	
		return element
	else:
		return None
	
def airDensity(temp:float, pressure:float) -> float:
	return (pressure * 100) / (287.05 * (temp + 273.15))

def aqiIndex(value:float, param:str="pm10") -> tuple: # https://ecmwf-projects.github.io/copernicus-training-cams/_images/eaqi_index_level.png
	limits = {
		"o3": [50, 100, 130, 240, 380],
		"no2": [40, 90, 120, 230, 340],
		"so2": [100, 200, 350, 500, 750],
		"pm10": [20, 40, 50, 100, 150],
		"pm2_5": [10, 20, 25, 50, 75]
	}
	desc = ["Sehr Gut", "Gut", "Mäßig", "Schlecht", "Sehr Schlecht", "Extrem Schlecht"]
	
	if param in limits:
		i = 1
		for l in limits[param]:
			if value <= l:
				return (i, desc[i - 1])
			i += 1
		return (i, desc[i - 1])
	else:
		return None
	
def pmHumidityCorrection(pm:float, growth_factor:float) -> float:
	return pm / growth_factor

def pmHumidityGrowthFactor(humidity:float, a:float=1, b:float=0.25, hum_max:float=90) -> float:
	if(hum_max >= 100 and hum_max < 0):
		raise ValueError("hum max must be >= 0 and < 100")
	hum = min(humidity / 100, hum_max / 100) # bei hum == 1 => Division durch 0
	return a + ((b * (hum ** 2)) / (1 - hum))

def rainIntensityLevel(rain_intensity:float) -> tuple:
	if(rain_intensity == 0):
		return (0, "kein Regen")
	elif(rain_intensity <= 2.5):
		return (1, "leichter Regen")
	elif(rain_intensity <= 10):
		return (2, "mäßiger Regen")
	elif(rain_intensity <= 50):
		return (3, "starker Regen")
	else:
		return (4, "sehr straker Regen")
	
def sunshineThreshold(lat:float, lon:float, utc_time:time.struct_time, threshold_factor:float=0.75) -> float: #http://www.plevenon-meteo.info/technique/theorie/enso/ensoleillement.html
	DEG_TO_RAD = math.pi / 180
	RAD_TO_DEG = 180 / math.pi

	solar_time = (utc_time.tm_hour * 60 + utc_time.tm_min + lon * 4) / 60
	eta = (solar_time - 12) * 15

	declination = 23.45 * math.sin(360 * (284 + utc_time.tm_yday) / 365 * DEG_TO_RAD)
	elevation = math.asin(math.sin(lat * DEG_TO_RAD) * math.sin(declination * DEG_TO_RAD) + math.cos(lat * DEG_TO_RAD) * math.cos(declination * DEG_TO_RAD) * math.cos(eta * DEG_TO_RAD)) * RAD_TO_DEG

	r_out = 1367 * (1 + 0.034 * math.cos((360 * utc_time.tm_yday / 365) * DEG_TO_RAD))

	m = math.sqrt(1229 + (614 * math.sin(elevation * DEG_TO_RAD)) ** 2) - 614 * math.sin(elevation * DEG_TO_RAD)# * (pressure / sealevel_pressure)

	r_direct = r_out * 0.6 ** m * math.sin(elevation * DEG_TO_RAD)
	r_diffus = r_out * (0.271 - 0.294 * 0.6 ** m) * math.sin(elevation * DEG_TO_RAD)
	r = max(0, r_diffus + r_direct)

	if elevation > 3:
		threshold = threshold_factor * r
	else:
		threshold = 0

	return r, threshold

def sunshine(radiation:float, treshold:float) -> bool:
	return treshold > 0 and radiation > treshold