void calculateData() {
	Serial.println("Daten werden berechnet");

	data["data"]["dew_point"] = dewPoint(temp, humidity);
	float wind_chill = windchill(temp, 0.0);
	data["data"]["wind_chill"] = wind_chill;
	if (temp >= 22) {
		heat_index = heatIndex(temp, humidity);
	} else {
		heat_index = temp;
	}
	data["data"]["heat_index"] = heat_index;
	float absolute_humidity = absoluteHumidity(temp, humidity);
	data["data"]["absolute_humidity"] = absolute_humidity;

	if (temp < 22) {
		data["data"]["felt_temp"] = wind_chill;
	} else {
		data["data"]["felt_temp"] = heat_index;
	}

	int8_t temp_index;
	int8_t temp_value;
	String temp_desc;
	int8_t humidity_index;
	int8_t humidity_value;
	String humidity_desc;
	tempIndex(temp, CALIBRATION_COMFORT_TEMPERATURE_MEAN, CALIBRATION_COMFORT_TEMPERATURE_COEFF, temp_index, temp_desc, temp_value);
	humidityIndex(humidity, CALIBRATION_COMFORT_HUMIDITY_MEAN, CALIBRATION_COMFORT_HUMIDITY_COEFF, humidity_index, humidity_desc, humidity_value);

	data["data"]["temp_index"] = temp_index;
	data["data"]["temp_index_description"] = temp_desc;
	data["data"]["temp_deviation"] = temp_value;
	data["data"]["humidity_index"] = humidity_index;
	data["data"]["humidity_index_description"] = humidity_desc;
	data["data"]["humidity_deviation"] = humidity_value;

	comfort_index = ceil(float(float(abs(temp_index) + abs(humidity_index)) / 2));
	String comfort_desc_[2] = { "", "" };
	uint8_t i = 0;
	comfort_desc = "";
	if (temp_value != 0) {
		comfort_desc_[i] = temp_desc;
		i++;
	}
	if (humidity_value != 0) {
		comfort_desc_[i] = humidity_desc;
		i++;
	}

	for(uint8_t j = 0; j < 2; j++) {
		if(comfort_desc_[j] != "") {
			if(j != 0 && i - 1 == j) {
				comfort_desc += " und " + comfort_desc_[j];
			} else if(j != 0) {
				comfort_desc += ", " + comfort_desc_[j];
			} else {
				comfort_desc += comfort_desc_[j];
			}
		}
	}

	if(comfort_desc != "") {
		comfort_desc = getIndexDescription(comfort_index) + " - " + comfort_desc;
	} else {
		comfort_desc = getIndexDescription(comfort_index);
	}
	data["data"]["comfort_index_description_short"] = getIndexDescription(comfort_index);
	data["data"]["comfort_index"] = comfort_index;
	data["data"]["comfort_index_description"] = comfort_desc;

	data["ref"]["temp_mean"] = CALIBRATION_COMFORT_TEMPERATURE_MEAN;
	data["ref"]["humidity_mean"] = CALIBRATION_COMFORT_HUMIDITY_MEAN;
	data["name"] = STATIONINFO_NAME;

	Serial.println("Daten berechnet");
}