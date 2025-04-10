void getData() {
	Serial.println("Sensordaten werden gelesen");

	temp = int16_t((bme280.readTemperature() + CALIBRATION_TEMP_HOUSING_CORRECTION_OFFSET) * 10) / 10.0;
	humidity = bme280.readHumidity();
	pressure = bme280.readPressure();

	env_data["sensor_status"]["bme280"] = sensor_status_bme280;

	data["data"]["temp"] = temp;
	data["data"]["humidity"] = humidity;
	env_data["environment"]["other_data"]["pressure"] = pressure;

	time = WiFi.getTime();
	data["time"] = time;
	env_data["time"] = time;

	env_data["info"]["version"] = VERSION;
	env_data["info"]["started"] = start_time;

	Serial.println("Sensordaten gelesen");
}