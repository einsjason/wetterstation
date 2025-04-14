#!/usr/bin/env python3

import signal
import pathlib
import json

from utils.utilities import *
from utils.terminal_utils import *
from utils.timezone_linux import *

from server import *

SOFTWARE_INFO = {
	"version": "250410-BUGFIX"
}

# #############################################################

# Keyboard ISR
def keyboar_isr(sig=None, frame=None):
	Terminal.message("Programm wird gestoppt")
	webserver.stop()
	exit()

###############################################################################

# Lese Config-Datei
config_file = open(f"{pathlib.Path(__file__).parent.resolve()}/config.json")
config = json.load(config_file)
config_file.close()

config["cache"] = {}

print(Terminal.reset, end = "")
print(f"{Terminal.colors['yellow']}  \\  /      {Terminal.colors['blue']} __      __   _   _              _ _         _ ")
print(f"{Terminal.colors['yellow']}_ /‾‾{Terminal.colors['gray']}.-.    {Terminal.colors['blue']} \ \    / /__| |_| |_ ___ _ _ __| (_)____ __| |__ _ _  _ ")
print(f"{Terminal.colors['yellow']}  \\_{Terminal.colors['gray']}(   ).  {Terminal.colors['blue']}  \ \/\/ / -_)  _|  _/ -_) '_/ _` | (_-< '_ \ / _` | || | ")
print(f"{Terminal.colors['yellow']}  /{Terminal.colors['gray']}(___(__) {Terminal.colors['blue']}   \_/\_/\___|\__|\__\___|_| \__,_|_/__/ .__/_\__,_|\_, | ")
print(f"{Terminal.colors['blue']}    / / /   {Terminal.colors['blue']} Version: {SOFTWARE_INFO['version']}"+(" " * (28 - len(SOFTWARE_INFO['version'])))+f" |_|          |__/")
print()
print(f"{Terminal.colors['gray']}Drücken Sie >>Strg + C<<, um das Programm zu beenden.")
link = Terminal.link(f"http://localhost:{config['http']['port']}", "Interface öffnen")
print(f"{Terminal.colors['gray']}{link}")
print(f"{Terminal.reset}---------------------------------------------------------------------")
print()

signal.signal(signal.SIGINT, keyboar_isr)
signal.signal(signal.SIGTERM, keyboar_isr)

tz = getTimezoneContinentCity()
if "/" not in tz and " " in tz:
	tz = config['stationinfo']['fallback_tz']
config["cache"]['timezone'] = tz

config["cache"]["map_info"] = getMapInfo(config["map_zoom"], config["stationinfo"]["lat"], config["stationinfo"]["lon"])

webserver = WebServer(config["http"]["port"], config["http"]["only_localhost"], "/interface", config)

Terminal.message("Programm gestartet")

webserver.start()
