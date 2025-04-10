import calendar
import math
import time

class Suninfo:

	@staticmethod
	def getSunrise(lat:float, lon:float, date:time.struct_time) -> time.struct_time:
		value = Suninfo.__calcSunTime(lat, lon, date, True)
		if value is None:
			return False
		else:
			return value

	@staticmethod
	def getSunset(lat:float, lon:float, date:time.struct_time) -> time.struct_time:
		value = Suninfo.__calcSunTime(lat, lon, date, False)
		if value is None:
			return False
		else:
			return value
		
	@staticmethod
	def getTwilightBegin(lat:float, lon:float, date:time.struct_time) -> time.struct_time:
		value = Suninfo.__calcSunTime(lat, lon, date, True, 96)
		if value is None:
			return False
		else:
			return value
		
	@staticmethod
	def getTwilightEnd(lat:float, lon:float, date:time.struct_time) -> time.struct_time:
		value = Suninfo.__calcSunTime(lat, lon, date, False, 96)
		if value is None:
			return False
		else:
			return value

	@staticmethod
	def __calcSunTime(lat:float, lon:float, date:time.struct_time, isRiseTime:bool=True, zenith:float=90.8) -> time.struct_time:
		day = int(time.strftime("%d", date))
		month = int(time.strftime("%m", date))
		year = int(time.strftime("%Y", date))

		TO_RAD = math.pi/180.0

		# 1. first calculate the day of the year
		N1 = math.floor(275 * month / 9)
		N2 = math.floor((month + 9) / 12)
		N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
		N = N1 - (N2 * N3) + day - 30

		# 2. convert the longitude to hour value and calculate an approximate time
		lngHour = lon / 15

		if isRiseTime: # sunrise
			t = N + ((6 - lngHour) / 24)
		else: # sunset
			t = N + ((18 - lngHour) / 24)

		# 3. calculate the Sun's mean anomaly
		M = (0.9856 * t) - 3.289

		# 4. calculate the Sun's true longitude
		L = M + (1.916 * math.sin(TO_RAD*M)) + (0.020 * math.sin(TO_RAD * 2 * M)) + 282.634
		L = Suninfo._forceRange(L, 360 ) # NOTE: L adjusted into the range [0,360)

		# 5a. calculate the Sun's right ascension
		RA = (1/TO_RAD) * math.atan(0.91764 * math.tan(TO_RAD*L))
		RA = Suninfo._forceRange(RA, 360 ) # NOTE: RA adjusted into the range [0,360)

		# 5b. right ascension value needs to be in the same quadrant as L
		Lquadrant  = (math.floor( L/90)) * 90
		RAquadrant = (math.floor(RA/90)) * 90
		RA = RA + (Lquadrant - RAquadrant)

		# 5c. right ascension value needs to be converted into hours
		RA = RA / 15

		# 6. calculate the Sun's declination
		sinDec = 0.39782 * math.sin(TO_RAD*L)
		cosDec = math.cos(math.asin(sinDec))

		# 7a. calculate the Sun's local hour angle
		cosH = (math.cos(TO_RAD*zenith) - (sinDec * math.sin(TO_RAD*lat))) / (cosDec * math.cos(TO_RAD*lat))

		if cosH > 1:
			return None     # The sun never rises on this location (on the specified date)
		if cosH < -1:
			return None     # The sun never sets on this location (on the specified date)

		# 7b. finish calculating H and convert into hours

		if isRiseTime:
			H = 360 - (1/TO_RAD) * math.acos(cosH)
		else: # setting
			H = (1/TO_RAD) * math.acos(cosH)

		H = H / 15

		#8. calculate local mean time of rising/setting
		T = H + RA - (0.06571 * t) - 6.622

		# 9. adjust back to UTC
		UT = T - lngHour
		UT = Suninfo._forceRange(UT, 24)   # UTC time in decimal format (e.g. 23.23)

		# 10. Return
		hr = Suninfo._forceRange(int(UT), 24)
		min = round((UT - int(UT))*60, 0)
		if min == 60:
			hr += 1
			min = 0

		# 10. check corner case https://github.com/SatAgro/suntime/issues/1
		if hr == 24:
			hr = 0
			day += 1
			
			if day > calendar.monthrange(year, month)[1]:
				day = 1
				month += 1

				if month > 12:
					month = 1
					year += 1

		sec = int((min - int(min)) * 60)
		min = int(min)

		tz_offset_minute = int(time.strftime("%z", time.localtime())[-2:])
		tz_offset_hours = int(time.strftime("%z", time.localtime())[:-2])

		return time.localtime(time.mktime(time.struct_time((year, month, day, hr + tz_offset_hours, min + tz_offset_minute, sec, 0, 0, -1))))

	@staticmethod
	def _forceRange(v, max):
		# force v to be >= 0 and < max
		if v < 0:
			return v + max
		elif v >= max:
			return v - max

		return v
	