import time
from utils.utilities import terminalOutput

def resetData(config, sensors):
	terminalOutput("Daten werden zurückgesetzt")

	time_now = int(time.time())

	try:
		sensors['eeprom'].update(config['eeprom_addr']['time'], 0)
		sensors['eeprom'].update(config['eeprom_addr']['reset'], time_now)
		sensors['eeprom'].clear(config['eeprom_addr']['t_min'])
		sensors['eeprom'].clear(config['eeprom_addr']['t_max'])
		sensors['eeprom'].clear(config['eeprom_addr']['rain'])
		sensors['eeprom'].clear(config['eeprom_addr']['pm1_24h_avg'])
		sensors['eeprom'].clear(config['eeprom_addr']['pm2_5_24h_avg'])
		sensors['eeprom'].clear(config['eeprom_addr']['pm10_24h_avg'])
		sensors['eeprom'].update(config['eeprom_addr']['pm1_24h_avg_count'], 0)
		sensors['eeprom'].update(config['eeprom_addr']['pm2_5_24h_avg_count'], 0)
		sensors['eeprom'].update(config['eeprom_addr']['pm10_24h_avg_count'], 0)
		sensors['eeprom'].update(config['eeprom_addr']['wind_s_max_1d'], 0.0)
		sensors['eeprom'].update(config['eeprom_addr']['wind_g_max_1d'], 0.0)
		sensors['eeprom'].clear(config['eeprom_addr']['wind_s_avg_1d'])
		sensors['eeprom'].update(config['eeprom_addr']['sunshine_1d'], 0)

		terminalOutput("Daten zurückgesetzt")
	except:
		terminalOutput("Fehler beim zurücksetzten der Daten")

def resetDataHour(config, sensors):
	terminalOutput("Stündliche Daten werden zurückgesetzt")

	time_now = int(time.time())

	try:
		sensors['eeprom'].update(config['eeprom_addr']['reset_hour'], time_now)
		sensors['eeprom'].update(config['eeprom_addr']['rain_1h'], 0.0)
		sensors['eeprom'].update(config['eeprom_addr']['rain_i_max_1h'], 0.0)
		sensors['eeprom'].update(config['eeprom_addr']['wind_s_max_1h'], 0.0)
		sensors['eeprom'].update(config['eeprom_addr']['wind_g_max_1h'], 0.0)
		sensors['eeprom'].update(config['eeprom_addr']['sunshine_1h'], 0)

		terminalOutput("Fehler beim zurücksetzten der Stündlichen Daten")
	except:
		terminalOutput("Fehler beim zurücksetzten der Stündlichen Daten")