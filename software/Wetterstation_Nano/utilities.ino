float dewPoint(float temp, float humidity) {
	float f = (17.271 * temp) / (237.7 + temp) + log(humidity / 100.0);
	return (237.7 * f) / (17.271 - f);
}

float windchill(float temp, float wind_speed) {
	return 13.12 + (0.6215 * temp) + (((0.3965 * temp) - 11.37) * pow(wind_speed, 0.16));
}

float heatIndex(float temp, float humidity) {
	return -8.784695 + 1.61139411 * temp + 2.338549 * humidity - 0.14611605 * temp * humidity - 0.012308094 * pow(temp, 2) - 0.016424828 * pow(humidity, 2) + 0.002211732 * pow(temp, 2) * humidity + 0.00072546 * temp * pow(humidity, 2) - 0.000003582 * pow(temp, 2) * pow(humidity, 2);
}

float absoluteHumidity(float temp, float humidity) {
	// Gaskonstanten
	float a;
	float b;
	if (temp >= 0) {
		a = 7.5;
		b = 237.3;
	} else {
		a = 7.6;
		b = 240.7;
	}

	return 1000 * (18.016 / 8314.3) * ((humidity * (6.1078 * exp(((a * temp) / (b + temp)) / log10(2.718281828459)))) / (temp + 273.15));
}

float gaussian(float x, float u, float t) {
	return exp(-((x - u) * (x - u)) / (2 * t * t));
}

void tempIndex(float temp, float temp_mean, float temp_coeff, int8_t& temp_index, String& temp_desc, int8_t& temp_value) {
	float temp_g = gaussian(temp, temp_mean, temp_coeff);
	if (temp_g < 0.8) {
		if (temp > temp_mean) {
			temp_value = 1;
		} else {
			temp_value = -1;
		}
	} else {
		temp_value = 0;
	}

	temp_index = max(ceil((1 - temp_g) * 5), 1);
	if (temp < temp_mean) {
		temp_index = -temp_index;
	}
	if (temp_index == 1 || temp_index == -1) {
		temp_desc = "Optimal";
	} else if (temp_value > 0) {
		temp_desc = "zu Warm";
	} else {
		temp_desc = "zu Kalt";
	}
}

void humidityIndex(float humidity, float humidity_mean, float humidity_coeff, int8_t& humidity_index, String& humidity_desc, int8_t& humidity_value) {
	float humidity_g = gaussian(humidity, humidity_mean, humidity_coeff);
	if (humidity_g < 0.8) {
		if (humidity > humidity_mean) {
			humidity_value = 1;
		} else {
			humidity_value = -1;
		}
	} else {
		humidity_value = 0;
	}

	humidity_index = max(ceil((1 - humidity_g) * 5), 1);
	if (humidity < humidity_mean) {
		humidity_index = -humidity_index;
	}
	if (humidity_index == 1 || humidity_index == -1) {
		humidity_desc = "Optimal";
	} else if (humidity_value > 0) {
		humidity_desc = "zu Feucht";
	} else {
		humidity_desc = "zu Trocken";
	}
}

float airDensity(float temp, float pressure) {
	return (pressure * 100) / (287.05 * (temp + 273.15));
}

String getIndexDescription(uint8_t index) {
	String desc[5] = { "Sehr Gut", "Gut", "Mäßig", "Schlecht", "Schlecht" };
	if (index >= 1 and index <= 5) {
		return desc[index - 1];
	} else {
		return "";
	}
}

String ipAddressToString(const IPAddress& ip) {
	return String(ip[0]) + String(".") + String(ip[1]) + String(".") + String(ip[2]) + String(".") + String(ip[3]);
}