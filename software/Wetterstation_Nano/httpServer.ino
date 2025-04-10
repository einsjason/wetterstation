void wifiClient() {
	WiFiClient client = server.available();

	if (client) {
		uint8_t response = 0;
		String currentLine = "";

		digitalWrite(LED_BUILTIN, LOW);

		while (client.connected()) {
			if (client.available()) {
				char c = client.read();
				if (c == '\n') {
					if (currentLine.length() == 0) {
						String response_string = "";
						if (response == 1) {
							int16_t rssi = WiFi.RSSI();
							String link_quality = "";
							if(rssi > -50) {
								link_quality = "very good";
							} else if(rssi > -60) {
								link_quality = "good";
							} else if(rssi > -70) {
								link_quality = "fair";
							} else if(rssi > -80) {
								link_quality = "poor";
							} else {
								link_quality = "very poor";
							}
							response_string = "<title>Wetterstation NANO</title><h1>Wetterstation NANO</h1>Version: " + String(VERSION) + "<h2>Overview</h2><table><tr><td>Temperature:</td><td>" + String(temp) + " °C</td></tr><tr><td>Comfort:</td><td>" + comfort_desc + "</td></tr><tr><td>Humidity:</td><td>" + String(humidity) + " %</td></tr></table><h2>Data</h2><a href='data/'>data/</a><h2>Network</h2><table><tr><td>wlan0:</td><td>" + ipAddressToString(ip) + "<br>" + WIFI_SSID + "<br>Quality: " + link_quality + "</td></tr></table>";
							client.println("HTTP/1.1 200 OK");
							client.println("Content-Type: text/html; charset=UTF-8");
						} else if (response == 2) {
							response_string = "<h1>Index of /data</h1><ul><li><a href='../'>../</a></li><li><a href='weatherdata.json'>weatherdata.json</a></li><li><a href='environment.json'>environment.json</a></li></ul>";
							client.println("HTTP/1.1 200 OK");
							client.println("Access-Control-Allow-Origin: *");
							client.println("Content-Type: text/html; charset=UTF-8");
						} else if (response == 3) {
							response_string = JSON.stringify(data);
							client.println("HTTP/1.1 200 OK");
							client.println("Content-Type: application/json");
							client.println("Access-Control-Allow-Origin: *");
						} else if (response == 4) {
							response_string = JSON.stringify(env_data);
							client.println("HTTP/1.1 200 OK");
							client.println("Content-Type: application/json");
							client.println("Access-Control-Allow-Origin: *");
						} else {
							response_string = "<h1>Not Found</h1>";
							client.println("HTTP/1.1 404 Not Found");
							client.println("Content-Type: text/html; charset=UTF-8");
						}

						client.print("Server: WiFiNINA/");
						client.println(WiFi.firmwareVersion());
						client.print("Content-Length: ");
						client.println(response_string.length());
						client.println();
						client.println(response_string);
						break;
					} else {
						currentLine = "";
					}
				} else if (c != '\r') {
					currentLine += c;
				}

				if (currentLine.endsWith("GET / ")) {
					response = 1;
				} else if (currentLine.endsWith("GET /data/ ")) {
					response = 2;
				} else if (currentLine.endsWith("GET /data/weatherdata.json ")) {
					response = 3;
				} else if (currentLine.endsWith("GET /data/environment.json ")) {
					response = 4;
				}
			}
		}

		client.stop();

		digitalWrite(LED_BUILTIN, HIGH);
	}
}