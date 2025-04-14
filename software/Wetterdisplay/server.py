import time
import json
import io
import PIL.Image
import http.server

from utils.utilities import *
from utils.suninfo import *

from utils.web_utils import *
from utils.terminal_utils import *

path = ""
config = {}

class WebServer():
	def __init__(self, port:int, only_localhost:bool, path_:str, config_:dict):
		global path, config
		self.__host = "127.0.0.1" if only_localhost else "0.0.0.0"
		self.__port = port
		path = f"{os.path.dirname(os.path.realpath(__file__))}{path_}"
		config = config_

		self.server = http.server.HTTPServer((self.host, self.port), RequestHandler) # Server in neuem Thread starten

	@property
	def port(self) -> int:
		return self.__port
	
	@property
	def host(self) -> str:
		return self.__host

	def start(self):
		Terminal.message("Server an Port " + str(self.port) + " gestartet")
		self.server.serve_forever()

	def stop(self):
		# set the two flags needed to shutdown the HTTP server manually
		self.server._BaseServer__is_shut_down.set()
		self.server.__shutdown_request = True

		Terminal.message('Server wird gestoppt')
		self.server.shutdown()
		self.server.server_close()

# ##################################################################################################

class RequestHandler(http.server.BaseHTTPRequestHandler):
	
	def do_GET(self):
		global path, cache

		request_path, get_parameters = getGETParams(self.path)

		if request_path[:4] == "/api":
			if request_path == "/api/update_spotlight": # Hintergrundbild aktualisieren
				COLOR_SAMPLING_RATE = 50
				try:
					data = json.loads(getResource(config["data_sources"]["bing_url"]))
					spotlight_info = data['images'][0]['copyright']
					spotlight_info = spotlight_info[:spotlight_info.index("(") - 1] # save image description for next http requests
					image = getResource(config["data_sources"]["bing_base_url"] + data['images'][0]['url'], False)
					
					# convert to image object
					image_ = PIL.Image.open(io.BytesIO(image))
					image_.save(f"{path}/spotlight/image.jpg")
					image_ = image_.convert("RGB")
					
					avg = [0, 0, 0] # average color
					# take every nth pixel as defined in SPOTLIGHT_COLOR_SAMPLING_RATE and calculate the average color
					image_pixels = image_.load()
					for y in range(image_.size[1] // COLOR_SAMPLING_RATE):
						for x in range(image_.size[0] // COLOR_SAMPLING_RATE):
							r, g, b = image_pixels[x, y]
							avg[0] = int((avg[0] + r) / 2)
							avg[1] = int((avg[1] + g) / 2)
							avg[2] = int((avg[2] + b) / 2)

					spotlight_color = "#" + to_hex(avg[0]) + to_hex(avg[1]) + to_hex(avg[2])

					file = open(f"{path}/spotlight/info.json", "w")
					file.write(json.dumps({
						"description": spotlight_info,
						"color": spotlight_color,
						"update_time": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())
					}))
					file.close()

					self.__response(code=201, data="201 - Created")
				except Exception as err:
					self.__response(code=503, data="503 - Service Unavaiable")

			elif request_path == "/api/radar_info":
				self.__response(mime="application/json", data=json.dumps({
					"point": {
						"left": int(round(config["cache"]["map_info"]["pointx"] * config["cache"]["map_info"]["xtiles"] * 256)),
						"top": int(round(config["cache"]["map_info"]["pointy"] * config["cache"]["map_info"]["ytiles"] * 256))
					},
					"size": {
						"width": config["cache"]["map_info"]["xtiles"] * 256,
						"height": config["cache"]["map_info"]["ytiles"] * 256
					} 
				}))

			elif request_path == "/api/radar" or request_path == "/api/radar/time": # Radarbild
				if "n" in get_parameters:
					n = int(get_parameters["n"])
				else:
					n = 0

				try:
					t = (time.time() // 300) * 300
					tstring = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(t))
					tstring = f"{tstring[:-2]}:{tstring[-2:]}"
					data = getResource(config["data_sources"]["weatherradar_url"]
						+ "?tz=" + config["cache"]["timezone"]
						+ "&lat=" + str(config["stationinfo"]["lat"])
						+ "&lon=" + str(config["stationinfo"]["lon"])
						+ "&distance=" + str(config["radar_distance"] * 1000)
						+ "&format=plain"
						+ "&date=" + tstring)
					data = json.loads(data)['radar']

					if n >= 0 and n < len(data):
						data = data[n]
					else:
						self.__response(code=400, data="400 - Bad Request")
						return

					if request_path[-5:] == "/time":
						self.__response(mime="application/json", data=json.dumps({
							"time": data["timestamp"]
						}))
					else:
						sizex = len(data["precipitation_5"])
						sizey = len(data["precipitation_5"][0])

						image = PIL.Image.new("RGBA", (sizex, sizey), (0, 0, 0, 0))
						for x in range(sizex):
							for y in range(sizey):
								if data["precipitation_5"][x][y] > 0:
									col = rainToColor((data["precipitation_5"][x][y] / 100) * 12)
									image.putpixel((y, x), (col[0], col[1], col[2], 255))

						fac = 250 / config["cache"]["map_info"]["tile_height"]
						resized_image = image.resize((round(sizex * fac), round(sizey * fac)), resample=PIL.Image.Resampling.NEAREST)

						image_bytes = io.BytesIO()
						resized_image.save(image_bytes, format="PNG")
						image_bytes = image_bytes.getvalue()

						self.__response(mime="image/png", data=image_bytes)
				except:
					self.__response(code=503, data="503 - Service Unavaiable")

			elif request_path == "/api/radar_forecast": # Radarvorhersage
				try:
					t = (time.time() // 300) * 300
					tstring = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(t))
					tstring = f"{tstring[:-2]}:{tstring[-2:]}"
					data = getResource(config["data_sources"]["weatherradar_url"]
						+ "?tz=" + config["cache"]["timezone"]
						+ "&lat=" + str(config["stationinfo"]["lat"])
						+ "&lon=" + str(config["stationinfo"]["lon"])
						+ "&distance=1"
						+ "&format=plain"
						+ "&date=" + tstring)
					data = json.loads(data)['radar']
					data_res = []
					for d in data:
						data_res.append({
							"value": (d["precipitation_5"][0][0] / 100) * 12,
							"time": d["timestamp"]
						})
					self.__response(mime="application/json", data=json.dumps(data_res))
				except:
					self.__response(code=503, data="503 - Service Unavaiable")

			elif request_path == "/api/map": # OSM Karte
				TRANSPARENT_TRESHOLD = 200
				BRIGHTNESS = 2
				#try:
				map = PIL.Image.new("RGBA", (config["cache"]["map_info"]["xtiles"] * 256, config["cache"]["map_info"]["ytiles"] * 256))

				for iy in range(config["cache"]["map_info"]["tile_start"][1], config["cache"]["map_info"]["tile_end"][1] + 1):
					for ix in range(config["cache"]["map_info"]["tile_start"][0], config["cache"]["map_info"]["tile_end"][0] + 1):
						image = getResource(config["data_sources"]["osm_url"]
							+ str(config["map_zoom"])
							+ "/" + str(ix)
							+ "/" + str(iy)
							+ ".png", False)

						# convert to Image object
						image = PIL.Image.open(io.BytesIO(image))
						image = image.convert("LA")

						image_pixels = image.load()
						for y in range(image.size[1]):
							for x in range(image.size[0]):
								l, a = image_pixels[x, y]
								l = 255 - l
								l = min(l * BRIGHTNESS, 255)
									
								if l < TRANSPARENT_TRESHOLD - 30:
									a = 0
								elif l > TRANSPARENT_TRESHOLD + 30:
									a = 255
								else:
									a = int(valueMap(l, TRANSPARENT_TRESHOLD - 30, TRANSPARENT_TRESHOLD + 30, 0, 255))
								l = 255
								image_pixels[x, y] = (l, a)

						map.paste(image, ((ix - config["cache"]["map_info"]["tile_start"][0]) * 256, (iy - config["cache"]["map_info"]["tile_start"][1]) * 256))

				# convert back to bytes
				image_bytes = io.BytesIO()
				map.save(image_bytes, format="PNG")
				image_bytes = image_bytes.getvalue()

				self.__response(mime="image/png", data=image_bytes)
				#except:
				#	self.__response(code=503, data="503 - Service Unavaiable")

			elif request_path[:10] == "/api/data_":
				if request_path[10:] in config["data_sources"]["weather_url"]:
					try:
						self.__response(mime="application/json", data=getResource(config["data_sources"]["weather_url"][request_path[10:]]))
					except Exception as er:
						self.__response(code=503, data="503 - Service Unavaiable")
				else:
					self.__response(code=404, data="404 - Not Found")

			elif request_path == "/api/weatherwarnings":
				try:
					data = getResource(config["data_sources"]["weatherwarnings_url"]
						+ "?tz=" + config["cache"]["timezone"]
						+ "&lat=" + str(config["stationinfo"]["lat"])
						+ "&lon=" + str(config["stationinfo"]["lon"]))
					data = json.loads(data)['alerts']
					self.__response(mime="application/json", data=json.dumps(data))
				except:
					self.__response(code=503, data="503 - Service Unavaiable")

			elif request_path == "/api/weatherforecast":
				try:
					res = []
					num_d = 4

					t = ((((time.time() + time.localtime().tm_gmtoff) // 86400) * 86400) + 43200) - time.localtime().tm_gmtoff # Setze auf Mittag, um falsche Berechnungen bei Zeitumstellungen zu verhindern
					for i in range(num_d):
						data = getResource(config["data_sources"]["weatherforecast_url"]
							+ "?tz=" + config["cache"]["timezone"]
							+ "&lat=" + str(config["stationinfo"]["lat"])
							+ "&lon=" + str(config["stationinfo"]["lon"])
							+ "&date=" + time.strftime("%Y-%m-%d", time.localtime(t + (i * 86400))))
						data = json.loads(data)['weather']
						data.pop()
						res.append(data)

					self.__response(mime="application/json", data=json.dumps(res))
				except:
					self.__response(code=503, data="503 - Service Unavaiable")

			elif request_path == "/api/suninfo":
				res = []
				num_d = 4
				
				t = ((((time.time() + time.localtime().tm_gmtoff) // 86400) * 86400) + 43200) - time.localtime().tm_gmtoff # Setze auf Mittag, um falsche Berechnungen bei Zeitumstellungen zu verhindern
				for i in range(num_d):
					t_ = time.localtime(t + (i * 86400))
					res.append({
						"sunrise": time.strftime("%Y-%m-%dT%H:%M:%S%z", Suninfo.getSunrise(config["stationinfo"]["lat"], config["stationinfo"]["lon"], t_)),
						"sunset": time.strftime("%Y-%m-%dT%H:%M:%S%z", Suninfo.getSunset(config["stationinfo"]["lat"], config["stationinfo"]["lon"], t_))
					})
				self.__response(mime="application/json", data=json.dumps(res))

			else: # API Fallback
				self.__response(code=404, data="404 - Not Found")

		else:
			webfile = getWebfile(request_path, path)

			if webfile:
				self.__response(mime=webfile[1], data=webfile[0], cache=False if request_path[:10] == "/spotlight" else True)
			else:
				self.__response(code=404, data="404 - Not Found")
	
	# ##################################################
	
	def __response(self, code:int=200, mime:str="text/plain", data:str="200 - Ok", cache:bool=False):
		try:
			self.send_response(code)
			self.send_header("Content-Type", mime)
			if cache:
				self.send_header("Cache-Control", "public, max-age=604800")
			else:
				self.send_header("Cache-Control", "no-store")
			self.end_headers()
			if(isinstance(data, str)):
				self.wfile.write(bytes(data, "utf-8"))
			else:
				self.wfile.write(data)
		except ConnectionAbortedError as err:
			pass

	# ##################################################

	def log_message(self, format:str, *args):
		pass