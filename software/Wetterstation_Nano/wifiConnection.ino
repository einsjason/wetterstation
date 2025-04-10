IPAddress connectToWifi() {
	uint32_t timer = 0;
	
	digitalWrite(LED_BUILTIN, LOW);

	Serial.print("Netzwerkverbindung mit ");
	Serial.print(WIFI_SSID);
	Serial.println(" wird hergestellt");

	wifi_status = WL_IDLE_STATUS;
	while (wifi_status != WL_CONNECTED) {
		timer = millis();

		wifi_status = WiFi.begin(WIFI_SSID, WIFI_PASS);

		while(millis() - timer <= 5000) {
			digitalWrite(LED_BUILTIN, HIGH);
			delay(500);
			digitalWrite(LED_BUILTIN, LOW);
			delay(500);
		}
	}
	digitalWrite(LED_BUILTIN, HIGH);

	IPAddress ip = WiFi.localIP();
	Serial.print("Netzwerverbindung hergestellt - IP: ");
	Serial.println(ipAddressToString(ip));

	return ip;
}

bool checkWifi() {
	wifi_status = WiFi.status();
	bool status = wifi_status != WL_CONNECTION_LOST && wifi_status != WL_DISCONNECTED;
	if(!status) {
		Serial.println("Netzwerkverbindung unterbrochen");
	}
	return status;
}