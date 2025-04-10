import time
import math
import urllib.request
import gzip

def valueMap(value:float, in_min:float, in_max:float, out_min:float, out_max:float) -> float: # Arduino map Funktion
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def to_hex(val:int, min_length:int=2) -> str: # int to minimum min_length long hex string
	hex_str = hex(val)[2:]
	while(len(hex_str) < min_length):
		hex_str = "0" + hex_str
	return hex_str

def getResource(url:str, decode:bool=True, timeout:int=10, data:any=None, method:str="GET") -> any:
	request = urllib.request.Request(url, data=data, headers={
		"User-Agent": "urllib",
		"Accept-Encoding": "gzip"
	} ,method=method)
	data = urllib.request.urlopen(request, timeout=timeout)
	if data.info().get('Content-Encoding') == 'gzip':
		return gzip.decompress(data.read())
	if decode and data.headers.get_content_charset():
		return data.read().decode(data.headers.get_content_charset())
	else:
		return data.read()
	
def getMapInfo(zoom:int, lat_point:float, lon_point:float, lat_area:float=0.3, lon_area:float=1) -> dict:
	lat_min = lat_point - lat_area
	lat_max = lat_point + lat_area
	lon_min = lon_point - lon_area
	lon_max = lon_point + lon_area

	#def epsg4326ToEpsg3857(coordinates:float) -> tuple:
	#	x = (coordinates[1] * 20037508.34) / 180
	#	y = math.log(math.tan(((90 + coordinates[0]) * math.pi) / 360)) / (math.pi / 180)
	#	y = (y * 20037508.34) / 180
	#	return (x, y)

	def latLonToTile(lat_deg:float, lon_deg:float, zoom:int) -> tuple:
		lat_rad = math.radians(lat_deg)
		n = math.pow(2.0, zoom)
		xtile = (lon_deg + 180.0) / 360.0 * n
		ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
		return (int(xtile), int(ytile))

	def tileToLatLon(x:int, y:int, zoom:int) -> tuple:
		n = math.pow(2.0, zoom)
		lon = x / n * 360.0 - 180
		lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * y / n)))
		lat = math.degrees(lat_rad)
		return (lat, lon)

	southwest = latLonToTile(lat_min, lon_min, zoom)
	northeast = latLonToTile(lat_max, lon_max, zoom)
	bbox = tileToLatLon(southwest[0], southwest[1] + 1, zoom) + tileToLatLon(northeast[0] + 1, northeast[1], zoom)

	return {
		"zoom": zoom,
		"tile_start": (southwest[0], northeast[1]),
		"tile_end": (northeast[0], southwest[1]),
		"bbox": bbox,
		#"bbox_epsg3857": epsg4326ToEpsg3857([bbox[0], bbox[1]]) + epsg4326ToEpsg3857([bbox[2], bbox[3]]),
		"xtiles": abs(southwest[0] - northeast[0]) + 1,
		"ytiles": abs(northeast[1] - southwest[1]) + 1,
		"pointx": (lon_point - bbox[1]) / (bbox[3] - bbox[1]),
		"pointy": 1 - ((lat_point - bbox[0]) / (bbox[2] - bbox[0])),
		"tile_height": 20004.500 / (2 ** zoom) #halber Polumfang
}

def timezoneOffset() -> int:
	tz = time.strftime("%z", time.localtime())
	tz = (-1 if tz[:1] == "-" else 1, int(tz[1:3]), int(tz[3:]))
	return ((tz[1] * 3600) + (tz[2] * 60)) * tz[0]

def rainToColor(value:float) -> tuple:
	if value >= 150:
		return (255, 0, 255)
	elif value >= 75:
		return (199, 43, 199)
	elif value >= 30:
		return (144, 50, 144)
	elif value >= 15:
		return (13, 109, 199)
	elif value >= 10:
		return (23, 126, 220)
	elif value >= 5:
		return (34, 148, 243)
	elif value >= 2:
		return (51, 173, 255)
	elif value >= 0.4:
		return (83, 210, 255)
	elif value > 0:
		return (170, 255, 255)
	else:
		return (127, 127, 127)