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

	terminalOutput("Warnungen werden berechnet")

	# Frost/Hitze Hitzeindex: https://www.pete.at/wetter/HitzeindexPete_doc.jpg
	if(isNumeric(data['data']['heat_index'])):
		if(data['data']['heat_index'] >= 36):
			warnings.append(createWarningMessage("Es tritt Extreme Hitze mit bis zu " + str(int(round(data['data']['temp'], 0))) + " °C auf.", "WARNUNG vor EXTREMER HITZE", "EXTREME HITZE", 2, "heat2"))
		elif(data['data']['heat_index'] >= 27):
			warnings.append(createWarningMessage("Es tritt Hitze mit bis zu " + str(int(round(data['data']['temp'], 0))) + " °C auf.", "WARNUNG vor HITZE", "STARKE HITZE", 1, "heat1"))

	# CO₂
	if(isNumeric(data['data']['co2_index'])):
		if(data['data']['co2_index'] >= 4):
			warnings.append(createWarningMessage("Es Besteht Gefahr durch eine sehr hohe CO₂-Konzentrationen bis zu " + str(data['data']['co2']) + " ppm.", "WARNUNG vor SCHLECHTER RAUMLUFT", "SCHLECHTE RAUMLUFT", 1, "co21"))

	# VOC
	if(isNumeric(data['data']['voc_index'])):
		if(data['data']['voc_index'] >= 4):
			warnings.append(createWarningMessage("Es Besteht Gefahr durch eine sehr hohe VOC-Konzentrationen bis zu " + str(data['data']['voc']) + " ppb.", "WARNUNG vor SCHLECHTER RAUMLUFT", "SCHLECHTE RAUMLUFT", 1, "co21"))

	terminalOutput("Warnungen berechnet")