const warncell_id = 714612002;

async function getDataText(url) {
	const response = await fetch(url);
	const data = await response.text();

	return data;
}

async function getDataJson(url) {
	const response = await fetch(url);
	const data = await response.json();

	return data;
}

function switchMeasurements() {
	const div_measurements = document.getElementById('measurement');
	const button_measurements = document.getElementById('measurementButton');

	if (div_measurements.style.maxHeight == "0px") {
		div_measurements.style.maxHeight = "2000px";
		div_measurements.style.overflow = "auto";
		button_measurements.innerHTML = "<span class='icon_s'>&#xf106</span> Messwerte ausblenden";
	} else {
		div_measurements.style.maxHeight = "0px";
		div_measurements.style.overflow = "hidden";
		button_measurements.innerHTML = "<span class='icon_s'>&#xf107</span> Messwerte anzeigen";
	}
}

async function getWeather() {
	document.getElementById("load_current").style.display = "";

	try {
		const data = await getDataJson("https://rammer.org/api/weather/weatherdata.json");

		document.querySelector("#weather.content_container.bg_image").style.background = "url(https://rammer.org/_images/weather/backgrounds/weather/" + data.data.weather_icon_simple + ".jpg)";

		Array.from(document.querySelectorAll(".content_container.bg_image #measurement .container, .content_container.bg_image button")).forEach(e => {
			e.style.background = "var(--" + data.data.weather_icon_simple + ")";
		});

		document.getElementById("minutes_current").innerHTML = new Date(data.time).toLocaleTimeString("de-DE", {
			hour: "2-digit",
			minute: "2-digit"
		});

		document.getElementById("current_temp").innerHTML = parseFloat(data.data.temp).toFixed(0) + " °C";
		document.getElementById("current_felt_temp").innerHTML = parseFloat(data.data.felt_temp).toFixed(0) + " °C";
		document.getElementById("current_description").innerHTML = data.data.weather_description;
		document.getElementById("current_wind_dir_icon").style.transform = "rotate(" + (135 + data.data.wind_dir) + "deg)";
		document.getElementById("current_wind_description").innerHTML = data.data.wind_description;
		document.getElementById("current_measurements_temp").innerHTML = parseFloat(data.data.temp).toFixed(1) + " °C";
		document.getElementById("current_measurements_temp_min_max").innerHTML = parseFloat(data.data.temp_min).toFixed(1) + " °C / " + parseFloat(data.data.temp_max).toFixed(1) + " °C";
		document.getElementById("current_measurements_humidity").innerHTML = parseFloat(data.data.humidity).toFixed(0) + " %";
		document.getElementById("current_measurements_absolute_humidity").innerHTML = parseFloat(data.data.absolute_humidity).toFixed(1) + " g/m³";
		document.getElementById("current_measurements_dew_point").innerHTML = parseFloat(data.data.dew_point).toFixed(1) + " °C";
		document.getElementById("current_measurements_pressure").innerHTML = parseFloat(data.data.pressure).toFixed(0) + " hPa";
		document.getElementById("current_measurements_sealevel_pressure").innerHTML = parseFloat(data.data.sealevel_pressure).toFixed(0) + " hPa";
		document.getElementById("current_measurements_wind_speed").innerHTML = parseFloat(data.data.wind_speed).toFixed(1) + " km/h";
		document.getElementById("current_measurements_wind_gust").innerHTML = parseFloat(data.data.wind_gust).toFixed(1) + " km/h";
		document.getElementById("current_measurements_wind_dir").innerHTML = parseFloat(data.data.wind_dir).toFixed(0) + "°";
		document.getElementById("current_measurements_wind_dir_str").innerHTML = String(data.data.wind_dir_str);
		document.getElementById("current_measurements_rain").innerHTML = parseFloat(data.data.rain_total).toFixed(1) + " mm";
		document.getElementById("current_measurements_rain_1h").innerHTML = parseFloat(data.data.rain_total_1h).toFixed(1) + " mm";
		document.getElementById("current_measurements_rain_intensity").innerHTML = parseFloat(data.data.rain_intensity).toFixed(2) + " mm/h";
		document.getElementById("current_measurements_rain_intensity_max_1h").innerHTML = parseFloat(data.data.rain_intensity_max_1h).toFixed(2) + " mm/h";
		document.getElementById("current_measurements_cloud").innerHTML = parseFloat(data.data.cloud).toFixed(0) + " %";
		document.getElementById("current_measurements_irradiance").innerHTML = parseFloat(data.data.irradiance).toFixed(1) + " W/m²";
		document.getElementById("current_measurements_brightness").innerHTML = parseFloat(data.data.brightness).toFixed(0) + " lux";

		document.getElementById("astro_sunrise").innerHTML = new Date(data.astro.sunrise).toLocaleTimeString("de-DE", {
			hour: "2-digit",
			minute: "2-digit"
		});
		document.getElementById("astro_sunset").innerHTML = new Date(data.astro.sunset).toLocaleTimeString("de-DE", {
			hour: "2-digit",
			minute: "2-digit"
		});
		document.getElementById("astro_twilight_begin").innerHTML = new Date(data.astro.twilight_begin).toLocaleTimeString("de-DE", {
			hour: "2-digit",
			minute: "2-digit",
			weekday: "short"
		});
		document.getElementById("astro_twilight_end").innerHTML = new Date(data.astro.twilight_end).toLocaleTimeString("de-DE", {
			hour: "2-digit",
			minute: "2-digit",
			weekday: "short"
		});
	} catch (err) {
		console.error(err);
	}

	document.getElementById("load_current").style.display = "none";
}

async function getWeatherWarnings() {
	document.getElementById("weather_warnings_load").style.display = "";

	const dom = document.getElementById("warnings");
	dom.innerHTML = "";

	try {
		const data_dwd = await getDataJson("https://api.brightsky.dev/alerts?warn_cell_id=" + warncell_id);
		const bg_images = await getDataJson("https://rammer.org/api/weather/dwd_warnings.json");

		data_dwd.alerts.forEach(e => {
			let result = "<div class='bg_image container' style='width: calc(100% - 50px); background: var(--warnlevel" + bg_images[e.event_de].level + ");'>";
			result += "<table><tr>";
			result += "<td><span class='icon_r icon_fixwidth x-large'>&#xf05a</span></td>";
			result += "<td><b style='font-size: 110%;'>" + e.headline_de + "</b><br>" + e.description_de + "<br>" + new Date(e.onset).toLocaleTimeString("de-DE", {
				minute: '2-digit',
				hour: '2-digit',
				weekday: 'short'
			}) + " bis " + new Date(e.expires).toLocaleTimeString("de-DE", {
				minute: '2-digit',
				hour: '2-digit',
				weekday: 'short'
			}) + "</td>";
			result += "</tr></table>";

			dom.innerHTML += result;
		});
	} catch (err) {
		console.error(err);
	}

	try {
		const data = await getDataJson("https://rammer.org/api/weather/weatherwarnings.json");

		data.warnings.forEach(e => {
			let result = "<div class='bg_image container' style='width: calc(100% - 50px); background: var(--warnlevel" + e.level + ")'>";
			result += "<table><tr>";
			result += "<td><span class='icon_r icon_fixwidth x-large'>&#xf071</span></td>";
			result += "<td><b style='font-size: 110%;'>" + e.headline + "</b><br>" + e.description + "</td>";
			result += "</tr></table>";

			dom.innerHTML += result;
		});
	} catch (err) {
		console.error(err);
	}

	document.getElementById("weather_warnings_load").style.display = "none";
}