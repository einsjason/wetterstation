from utils.utilities import isNumeric, terminalOutput

def calculateWarnings(data, warnings):
	warnings.clear()

	def createWarningMessage(description, headline, event, level, icon):
		return {
			"description": description,
			"headline": headline,
			"event": event,
			"level": level,
			"icon": icon
		}

	# #############################################################################

	terminalOutput("Wetterwarnungen werden berechnet")

	# Frost/Hitze Hitzeindex: https://www.pete.at/wetter/HitzeindexPete_doc.jpg
	if(isNumeric(data['data']['temp'])):
		if(data['data']['temp'] <= -10):
			warnings.append(createWarningMessage("Es tritt Strenger Frost mit bis zu " + str(int(round(data['data']['temp'], 0))) + " °C auf.", "WARNUNG vor STRENGEM FROST", "STRENGER FROST", 1, "frost1"))
		elif(data['data']['temp'] <= 0):
			warnings.append(createWarningMessage("Es tritt Frost mit bis zu " + str(int(round(data['data']['temp'], 0))) + " °C auf.", "WARNUNG vor FROST", "FROST", 0, "frost0"))

	if(isNumeric(data['data']['heat_index'])):
		if(data['data']['heat_index'] >= 36):
			warnings.append(createWarningMessage("Es tritt eine Extreme Hitze mit bis zu " + str(int(round(data['data']['temp'], 0))) + " °C auf.", "WARNUNG vor EXTREMER HITZE", "EXTREME HITZE", 2, "heat2"))
		elif(data['data']['heat_index'] >= 27):
			warnings.append(createWarningMessage("Es tritt Hitze mit bis zu " + str(int(round(data['data']['temp'], 0))) + " °C auf.", "WARNUNG vor HITZE", "STARKE HITZE", 1, "heat1"))

	# Wind
	if(isNumeric(data['data']['wind_gust'])):
		if(data['data']['wind_gust'] >= 80):
			warnings.append(createWarningMessage("Es treten Schwere Sturmböen mit Windgeschwindigkeiten bis zu " + str(int(round(data['data']['wind_gust'], 0))) + " km/h auf.", "WARNUNG vor SCHWEREN STURMBÖEN", "SCHWERE STURMBÖEN", 3, "wind3"))
		elif(data['data']['wind_gust'] >= 60):
			warnings.append(createWarningMessage("Es treten Sturmböen mit Windgeschwindigkeiten bis zu " + str(int(round(data['data']['wind_gust'], 0))) + " km/h auf.", "WARNUNG vor STURMBÖEN", "STURMBÖEN", 2, "wind2"))
		elif(data['data']['wind_gust'] >= 40):
			warnings.append(createWarningMessage("Es treten Windböen mit Windgeschwindigkeiten bis zu " + str(int(round(data['data']['wind_gust'], 0))) + " km/h auf.", "WARNUNG vor WINDBÖEN", "WINDBÖEN", 1, "wind1"))

	# Starkregen
	if(isNumeric(data['data']['rain_intensity'])):
		if(data['data']['rain'] and data['data']['rain_intensity'] >= 25):
			warnings.append(createWarningMessage("Es tritt Starkregen mit bis zu " + str(int(round(data['data']['rain_intensity'], 0))) + " mm/h auf.", "WARNUNG vor STARKREGEN", "STARKREGEN", 1, "rain1"))

	# Nebel
	if(isNumeric(data['data']['humidity']) and isNumeric(data['data']['sky_temp']) and isNumeric(data['data']['temp'])):
		if(data['data']['humidity'] >= 95 and data['data']['sky_temp'] >= data['data']['temp'] - 0.1): # Nebel
			warnings.append(createWarningMessage("Die Sicht kann durch Nebel teilweise eingeschränkt sein.", "WARNUNG vor NEBEL", "NEBEL", 0, "fog0"))

	# Glatteis
	if(isNumeric(data['data']['humidity']) and isNumeric(data['data']['temp']) and data['data']['rain'] != None):
		if(data['data']['temp'] <= 0 and (data['data']['humidity'] >= 90 or data['data']['rain'])):
			warnings.append(createWarningMessage("Es besteht die Gefahr der Glatteisbildung.", "WARNUNG vor GLÄTTE", "GLÄTTE", 1, "ice1"))
			
	# Feinstaub
	if(isNumeric(data['data']['aqi'])):
		if(data['data']['aqi'] >= 5):
			warnings.append(createWarningMessage("Es Besteht Gefahr durch eine sehr hohe Feinstaubbelastung mit Feinstaubkonzentrationen bis zu " + str(data['data']['pm2_5']) + " µg/m³ (PM₂,₅) und " + str(data['data']['pm10']) + " µg/m³ (PM₁₀).", "WARNUNG vor FEINSTAUB", "FEINSTAUB", 1, "smog1"))

	terminalOutput("Wetterwarnungen berechnet")