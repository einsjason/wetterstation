#include <Arduino_JSON.h>
#include <Wire.h>
#include <math.h>
#include <SPI.h>
#include <WiFiNINA.h>

#include "BME280.h"

#include "config.h"

#define VERSION "250105"

//****************************************************************************************************

JSONVar data;
JSONVar env_data;

float temp;
uint8_t humidity;
uint16_t pressure;
float heat_index;
uint8_t comfort_index;
String comfort_desc;

uint32_t time = 0;
uint32_t start_time = 0;

IPAddress ip;
uint8_t wifi_status;
WiFiServer server(WIFI_SERVER_PORT);

BME280 bme280 = BME280(I2C_BME280);
bool sensor_status_bme280 = false;

uint32_t minute = 0;
uint32_t minute_last = -1;

//****************************************************************************************************

void setup() {
	pinMode(LED_BUILTIN, OUTPUT);

	Serial.begin(9600);
	delay(2000);
	Serial.print("Wetterstation - Nano - Version ");
	Serial.println(VERSION);

	Wire.begin();
	Wire.setClock(400000L);

	WiFi.setHostname(WIFI_HOST);

	sensor_status_bme280 = bme280.begin();

	if (WiFi.status() == WL_NO_MODULE) {
		Serial.println("Kommunikation mit Netzwerkmodul fehlgeschlagen");
		while (true) {
			digitalWrite(LED_BUILTIN, HIGH);
			delay(100);
			digitalWrite(LED_BUILTIN, LOW);
			delay(1900);
		}
	}

	ip = connectToWifi();
	server.begin();

	delay(5000);  // Warte, um Uhrzeit abzurufen
	time = WiFi.getTime();
	start_time = time;

	Serial.println("Start abgeschlossen");

	getData();
	calculateData();
	calculateWarnings();
	exportData();
}

void loop() {
	if (!checkWifi()) {
		ip = connectToWifi();
	}
	wifiClient();

	minute = WiFi.getTime() / 60;
	if(minute % 5 == 0 && minute != minute_last) {
		minute_last = minute;
		getData();
		calculateData();
		calculateWarnings();
		exportData();
	}

	delay(100);
}