import os.path
import urllib.parse

def mimeType(extension:str) -> str:
	mime_types = {
		"html": "text/html",
		"js": "application/javascript",
		"css": "text/css",
		"png": "image/png",
		"jpg": "image/jpeg",
		"svg": "image/svg+xml",
		"ttf": "font/ttf",
		"ico": "image/vnd.microsoft.icon",
		"json": "application/json"
	}
	if extension in mime_types.keys():
		return mime_types[extension]
	else:
		return "application/octet_stream"
		
def getWebfile(webpath:str, basepath:str) -> tuple:
	if webpath == "/":
		webpath = "/index.html"
		
	path = f"{basepath}{webpath}"

	if os.path.isfile(path):
		extension = os.path.splitext(path)[1][1:]
		
		f = open(path, "rb")
		return (f.read(), mimeType(extension))
	else:
		return None
		
def getGETParams(webpath:str) -> tuple:
	start = webpath.find("?")
	if start >= 0:
		request_path = webpath[:start]
		get_parameters = urllib.parse.parse_qs(urllib.parse.urlparse(webpath).query)
		for param in get_parameters:
			get_parameters[param] = get_parameters[param][0]
	else:
		request_path = webpath
		get_parameters = {}
	
	return (request_path, get_parameters)