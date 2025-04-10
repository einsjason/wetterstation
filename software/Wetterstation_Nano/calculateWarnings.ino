void calculateWarnings() {
	Serial.println("Warnungen werden berechnet");

	data["warnings"] = NULL; //delete
	uint8_t count = 0;

	// Frost/Hitze
	if (heat_index >= 36) {
		data["warnings"][count]["description"] = "Es tritt Extreme Hitze mit bis zu " + String(int8_t(temp)) + " °C auf.";
		data["warnings"][count]["headline"] = "WARNUNG vor EXTREMER HITZE";
		data["warnings"][count]["event"] = "EXTREME HITZE";
		data["warnings"][count]["level"] = 2;
		data["warnings"][count]["icon"] = "heat2";
		count++;
	} else if (heat_index >= 27) {
		data["warnings"][count]["description"] = "Es tritt Hitze mit bis zu " + String(int8_t(temp)) + " °C auf.";
		data["warnings"][count]["headline"] = "WARNUNG vor HITZE";
		data["warnings"][count]["event"] = "STARKE HITZE";
		data["warnings"][count]["level"] = 1;
		data["warnings"][count]["icon"] = "heat1";
		count++;
	}

	Serial.println("Warnungen berechnet");
}