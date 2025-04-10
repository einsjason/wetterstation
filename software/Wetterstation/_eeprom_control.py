import sys
import smbus2
import time
import json

from eeprom import EEPROM

action = None
if(len(sys.argv) > 1):
	action = sys.argv[1]
else:
	raise Exception("available options:\ngetall\ngetconfig\nget=<addrdec)>\nput=<addr(dec)>:<type>:<value>")

bus = smbus2.SMBus(1)
time.sleep(1)

memory = EEPROM(bus, 0x50)

if action == "getall":
	for i in range(memory.length):
		value = memory.get(i)
		print(i, value, type(value).__name__)

elif action == "getconfig":
	config_file = open("/home/pi/Scripts/config.json")
	config = json.load(config_file)
	config_file.close()

	for k in config['eeprom_addr']:
		i = config['eeprom_addr'][k]
		value = memory.get(i)
		print(i, f"\"{k}\"", value, type(value).__name__)

elif action[:4] == "get=":
	i = int(action[4:])
	value = memory.get(i)
	print(i, value, type(value).__name__)

elif action[:4] == "put=":
	a = action[4:]
	T = {
		"int": int,
		"float": float,
		"bool": bool,
		"NoneType": None
	}
	
	i = int(a[:a.index(":")])
	a = a[a.index(":") + 1:]
	t = a[:a.index(":")]
	v = a[a.index(":") + 1:]
	
	if T[t] == None:
		value = None
	else:
		value = T[t](v)

	print(i, value, type(value).__name__)
	memory.update(i, value)
	value = memory.get(i)
	print(i, value, type(value).__name__)

else:
	raise ValueError