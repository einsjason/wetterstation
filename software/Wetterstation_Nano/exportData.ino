bool exportData() {
	WiFiClient client;

	Serial.print("Netzwerkstatus: ");
	Serial.println(wifi_status);

	bool send_status = client.connect(OUTPUT_REMOTE_IP, OUTPUT_REMOTE_PORT);

	if (send_status) {
		digitalWrite(LED_BUILTIN, LOW);

		Serial.println("Daten werden exportiert");

		String post_data = "weatherdata.json=" + JSON.stringify(data);
		client.print("POST ");
		client.print(OUTPUT_REMOTE_PATH);
		client.println(" HTTP/1.1");
		client.println("Content-Type: application/x-www-form-urlencoded");
		client.print("Content-Length: ");
		client.println(post_data.length());
		client.print("User-Agent: WiFiNINA/");
		client.println(WiFi.firmwareVersion());
		client.println("Connection: close");
		client.print("Host: ");
		client.print(OUTPUT_REMOTE_IP);
		client.print(":");
		client.println(OUTPUT_REMOTE_PORT);
		client.println();
		client.println(post_data);

		client.stop();

		Serial.println("Daten exportiert");

		digitalWrite(LED_BUILTIN, HIGH);
		for (uint8_t i = 0; i < 2; i++) {
			delay(100);
			digitalWrite(LED_BUILTIN, LOW);
			delay(100);
			digitalWrite(LED_BUILTIN, HIGH);
		}
	} else {
		Serial.println("Daten konnten nicht exportiert werden");
	}

	return send_status;
}