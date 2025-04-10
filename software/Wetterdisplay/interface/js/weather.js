async function getCurrent() { //Aktuelle Daten
	let data_out;
	let data_in = [];

	//Außendaten
	setLoadStatus(document.getElementById("outside_load_data"), "load");
	console.info("load current outside");
	try {
		data_out = JSON.parse(await fetchData("/api/data_outside"));

		document.getElementById("outside_time").innerHTML = "";
		const t = new Date(formatUnixTime(data_out.time));
		if (new Date().getTime() - t.getTime() > 600000) {
			document.getElementById("outside_time").innerHTML += "<maskimg style='mask-image: url(icons/warning.svg); -webkit-mask-image: url(icons/warning.svg); vertical-align: -0.15em;'></maskimg>";
		}
		document.getElementById("outside_time").innerHTML += t.toLocaleTimeString("de-de", {
			hour: "2-digit",
			minute: "2-digit"
		});

		/*document.getElementById("outside_warn_temp").innerHTML = "";
		document.getElementById("outside_warn_wind").innerHTML = "";
		document.getElementById("outside_warn_rain").innerHTML = "";
		data_out.warnings.forEach(w => {
			if (w.event.includes("HITZE") || w.event.includes("STRENGER FROST")) {
				document.getElementById("outside_warn_temp").innerHTML = "";
			} else if (w.event.includes("FROST")) {
				document.getElementById("outside_warn_temp").innerHTML = "";
			} else if (w.event.includes("WINDBÖEN") || w.event.includes("STURMBÖEN")) {
				document.getElementById("outside_warn_wind").innerHTML = "";
			} else if (w.event.includes("STARKREGEN")) {
				document.getElementById("outside_warn_rain").innerHTML = "";
			}
		});:*/

		if (data_out.data.day_time) {
			document.documentElement.classList.add("light");
			document.documentElement.classList.remove("dark");
		} else {
			document.documentElement.classList.add("dark");
			document.documentElement.classList.remove("light");
		}

		document.getElementById("outside_name").innerHTML = data_out.name;

		document.getElementById("outside_temp").innerHTML = formatNumber(data_out.data.temp, 1) + " <span class='unit'>°C</span>";
		document.getElementById("outside_condition").innerHTML = data_out.data.weather_description;
		document.getElementById("outside_icon").src = "weather_icons/" + data_out.data.weather_icon + ".svg";
		document.getElementById("outside_humidity").innerHTML = formatNumber(data_out.data.humidity, 0) + " <span class='unit'>%</span>";
		document.getElementById("outside_pressure").innerHTML = formatNumber(data_out.data.pressure, 0) + " <span class='unit'>mbar</span>";
		document.getElementById("outside_dew_point").innerHTML = formatNumber(data_out.data.dew_point, 1) + " <span class='unit'>°C</span>";
		document.getElementById("outside_felt_temp").innerHTML = formatNumber(data_out.data.felt_temp, 1) + " <span class='unit'>°C</span>";
		document.getElementById("outside_wind_speed").innerHTML = formatNumber(data_out.data.wind_gust, 1) + " <span class='unit'>km/h</span>";
		document.getElementById("outside_wind_dir").innerHTML = String(data_out.data.wind_dir_str);
		document.getElementById("outside_wind_dir_icon").style.transform = "rotate(" + data_out.data.wind_dir + "deg)";
		document.getElementById("outside_rain").innerHTML = formatNumber(data_out.data.rain_total, 1) + " <span class='unit'>mm</span>";
		document.getElementById("outside_rain_intensity").innerHTML = formatNumber(data_out.data.rain_intensity, 1) + " <span class='unit'>mm/h</span>";
		document.getElementById("outside_airquality").innerHTML = formatNumber(data_out.data.pm2_5, 0) + " <span class='unit'>µg/m³</span>";
		document.getElementById("outside_airquality_index").style.color = "var(--aqi_" + data_out.data.aqi + ")";
		document.getElementById("outside_uv").innerHTML = data_out.data.uv_index;
		document.getElementById("outside_uv_index").style.color = "var(--uvi_" + data_out.data.uv_index + ")";
		document.getElementById("outside_cloud").innerHTML = data_out.data.cloud + " <span class='unit'>%</span>";
		document.getElementById("outside_sunshine").innerHTML = Math.floor(data_out.data.sunshine_1d / 60) + " <span class='unit'>h</span> " + (data_out.data.sunshine_1d - Math.floor(data_out.data.sunshine_1d / 60) * 60) + " <span class='unit'>min</span>";
		document.getElementById("outside_rain_icon").style.maskImage = "url(icons/rain_" + rainIcon(data_out.data.rain_intensity) + ".svg)";
		document.getElementById("outside_rain_icon").style.webkitMaskImage = "url(icons/rain_" + rainIcon(data_out.data.rain_intensity) + ".svg)";

		document.getElementById("outside").style.background = "url(weather_backgrounds/" + data_out.data.weather_icon_simple + ".jpg)";

		document.getElementById("astro_sunrise").innerHTML = new Date(formatUnixTime(data_out.astro.sunrise)).toLocaleTimeString("de-de", {
			hour: "2-digit",
			minute: "2-digit"
		});
		document.getElementById("astro_sunset").innerHTML = new Date(formatUnixTime(data_out.astro.sunset)).toLocaleTimeString("de-de", {
			hour: "2-digit",
			minute: "2-digit"
		});

		document.getElementById("clock_data_outside_temp").innerHTML = formatNumber(data_out.data.temp, 1) + " <span class='unit'>°C</span>";
		document.getElementById("clock_data_outside_icon").src = "weather_icons/" + data_out.data.weather_icon + ".svg";

		setLoadStatus(document.getElementById("outside_load_data"));
	} catch (err) {
		console.warn(err);

		setLoadStatus(document.getElementById("outside_load_data"), "error");

		document.getElementById("outside_time").innerHTML = "";

		document.documentElement.classList.remove("light");
		document.documentElement.classList.remove("dark");

		document.getElementById("outside_name").innerHTML = "Außen";

		document.getElementById("outside_temp").innerHTML = "-";
		document.getElementById("outside_condition").innerHTML = "-";
		document.getElementById("outside_icon").src = "weather_icons/null.svg";
		document.getElementById("outside_humidity").innerHTML = "-";
		document.getElementById("outside_pressure").innerHTML = "-";
		document.getElementById("outside_dew_point").innerHTML = "-";
		document.getElementById("outside_felt_temp").innerHTML = "-";
		document.getElementById("outside_wind_speed").innerHTML = "-";
		document.getElementById("outside_wind_dir").innerHTML = "-";
		document.getElementById("outside_wind_dir_icon").style.transform = "";
		document.getElementById("outside_rain").innerHTML = "-";
		document.getElementById("outside_rain_intensity").innerHTML = "-";
		document.getElementById("outside_airquality").innerHTML = "-";
		document.getElementById("outside_airquality_index").style.color = "";
		document.getElementById("outside_uv").innerHTML = "-";
		document.getElementById("outside_uv_index").style.color = "";
		document.getElementById("outside_cloud").innerHTML = "-";
		document.getElementById("outside_sunshine").innerHTML = "-";
		document.getElementById("outside_rain_icon").style.maskImage = "url(icons/rain_0.svg)";
		document.getElementById("outside_rain_icon").style.webkitMaskImage = "url(icons/rain_0.svg)";

		document.getElementById("outside").style.background = "";

		document.getElementById("astro_sunrise").innerHTML = "-";
		document.getElementById("astro_sunset").innerHTML = "-";

		document.getElementById("clock_data_outside_temp").innerHTML = "-";
		document.getElementById("clock_data_outside_icon").src = "weather_icons/null.svg";
	}

	//Innendaten
	const inside_stations = 2;

	for (let i = 1; i <= inside_stations; i++) {
		setLoadStatus(document.getElementById("inside" + i + "_load_data"), "load");
		console.info("load current inside" + i + "");
		try {
			data_in[i] = JSON.parse(await fetchData("/api/data_inside" + (i > 1 ? i : "")));

			document.getElementById("inside" + i + "_time").innerHTML = "";
			const t = new Date(formatUnixTime(data_in[i].time));
			if (new Date().getTime() - t.getTime() > 600000) {
				document.getElementById("inside" + i + "_time").innerHTML += "<maskimg style='mask-image: url(icons/warning.svg); -webkit-mask-image: url(icons/warning.svg); vertical-align: -0.15em;'></maskimg>";
			}
			document.getElementById("inside" + i + "_time").innerHTML += t.toLocaleTimeString("de-de", {
				hour: "2-digit",
				minute: "2-digit"
			});

			document.getElementById("inside" + i + "_name").innerHTML = data_in[i].name;

			document.getElementById("inside" + i + "_temp").innerHTML = formatNumber(data_in[i].data.temp, 1) + " <span class='unit'>°C</span>";
			document.getElementById("inside" + i + "_icon").style.background = "var(--index_" + data_in[i].data.comfort_index + ")";
			document.getElementById("inside" + i + "_condition").innerHTML = data_in[i].data.comfort_index_description_short;
			document.getElementById("inside" + i + "_humidity").innerHTML = formatNumber(data_in[i].data.humidity, 0) + " <span class='unit'>%</span>";
			document.getElementById("inside" + i + "_dew_point").innerHTML = formatNumber(data_in[i].data.dew_point, 1) + " <span class='unit'>°C</span>";
			document.getElementById("inside" + i + "_co2").innerHTML = (data_in[i].data.co2 ? formatNumber(data_in[i].data.co2, 0) + " <span class='unit'>ppm</span>" : "-");
			document.getElementById("inside" + i + "_temp_index").style.color = "var(--index_" + data_in[i].data.temp_index + ")";
			document.getElementById("inside" + i + "_humidity_index").style.color = "var(--index_" + data_in[i].data.humidity_index + ")";
			document.getElementById("inside" + i + "_co2_index").style.color = (data_in[i].data.co2_index ? "var(--index_" + data_in[i].data.co2_index + ")" : "");

			if(i == 1) {
				document.getElementById("clock_data_inside" + i + "_name").innerHTML = data_in[i].name;
				document.getElementById("clock_data_inside" + i + "_temp").innerHTML = formatNumber(data_in[i].data.temp, 1) + " <span class='unit'>°C</span>";
				document.getElementById("clock_data_inside" + i + "_index").style.color = "var(--index_" + data_in[i].data.comfort_index + ")";
			}

			setLoadStatus(document.getElementById("inside" + i + "_load_data"));
		} catch (err) {
			console.warn(err);

			setLoadStatus(document.getElementById("inside" + i + "_load_data"), "error");

			document.getElementById("inside" + i + "_time").innerHTML = "";

			document.getElementById("inside" + i + "_name").innerHTML = "Innen " + i;

			document.getElementById("inside" + i + "_temp").innerHTML = "-";
			document.getElementById("inside" + i + "_icon").style.background = "";
			document.getElementById("inside" + i + "_condition").innerHTML = "-";
			document.getElementById("inside" + i + "_humidity").innerHTML = "-";
			document.getElementById("inside" + i + "_dew_point").innerHTML = "-";
			document.getElementById("inside" + i + "_co2").innerHTML = "-";
			document.getElementById("inside" + i + "_temp_index").style.color = "";
			document.getElementById("inside" + i + "_humidity_index").style.color = "";
			document.getElementById("inside" + i + "_co2_index").style.color = "";

			if(i == 1) {
				document.getElementById("clock_data_inside" + i + "_name").innerHTML = "Innen " + i;
				document.getElementById("clock_data_inside" + i + "_temp").innerHTML = "-";
				document.getElementById("clock_data_inside" + i + "_index").style.color = "";
			}
		}

		//Luftfeuchteänderung
		try {
			if (data_out.data.absolute_humidity == null || data_out.data.absolute_humidity == null) {
				throw new Error('Value is NaN');
			}
			const abs_hum_diff = data_out.data.absolute_humidity - data_in[i].data.absolute_humidity;
			let ic = ""
			if (abs_hum_diff >= 1) {
				ic = "humidity_plus";
			} else if (abs_hum_diff <= -1) {
				ic = "humidity_minus";
			} else {
				ic = "humidity_nochange";
			}

			document.getElementById("inside" + i + "_humidity_change").style.maskImage = "url(icons/" + ic + ".svg)";
			document.getElementById("inside" + i + "_humidity_change").style.webkitMaskImage = "url(icons/" + ic + ".svg)";
		} catch (err) {
			console.warn(err);

			document.getElementById("inside" + i + "_humidity_change").style.maskImage = "";
			document.getElementById("inside" + i + "_humidity_change").style.webkitMaskImage = "";
		}
	}
}

async function getWarnings() { //Warnungen
	setLoadStatus(document.getElementById("warnings_load_data"), "load");

	const WARNLEVEL = {
		minor: 1,
		moderate: 2,
		severe: 3,
		extreme: 4
	};

	console.info("load warnings");
	try {
		data_warn = JSON.parse(await fetchData("/api/weatherwarnings"));

		document.getElementById("warnings_container").style.display = "";

		if (data_warn.length > 0) {
			let warn_level = 0;
			let begin = Infinity;
			let end = 0;
			let event = "";
			let num_warnings = 0;

			let warn_level_advance = 0;
			let begin_advance = Infinity;
			let end_advance = 0;
			let event_advance = "";
			let num_warnings_advance = 0;

			data_warn.forEach(e => {
				const is_advance = e.event_de.startsWith("VORABINFORMATION");
				let l = WARNLEVEL[e.severity];
				if (l < 0 || l > 4) {
					l = 1;
				}
				if (is_advance) {
					num_warnings_advance++;
					warn_level_advance = Math.max(warn_level, l);
					begin_advance = Math.min(begin, new Date(e.onset).getTime());
					end_advance = Math.max(end, new Date(e.expires).getTime());
					event_advance += (event != "" ? ", " : "") + e.event_de;
				} else {
					num_warnings++;
					warn_level = Math.max(warn_level, l);
					begin = Math.min(begin, new Date(e.onset).getTime());
					end = Math.max(end, new Date(e.expires).getTime());
					event += (event != "" ? ", " : "") + e.event_de;
				}
			});

			document.getElementById("warnings_icon").style.display = "";
			if (num_warnings > 0) {
				document.getElementById("warnings").innerHTML = "<b>" + event + "</b> - " + new Date(begin).toLocaleTimeString("de-de", {
					weekday: "short",
					hour: "2-digit",
					minute: "2-digit"
				}) + " bis " + new Date(end).toLocaleTimeString("de-de", {
					weekday: "short",
					hour: "2-digit",
					minute: "2-digit"
				});
				document.getElementById("warnings_icon").style.maskImage = "url(icons/warning.svg)";
				document.getElementById("warnings_icon").style.webkitMaskImage = "url(icons/warning.svg)";
				document.getElementById("warnings_container").style.background = "var(--warnlevel" + warn_level + ")";
			} else if (num_warnings_advance > 0) {
				document.getElementById("warnings").innerHTML = "<b>" + event_advance + "</b> - " + new Date(begin_advance).toLocaleTimeString("de-de", {
					weekday: "short",
					hour: "2-digit",
					minute: "2-digit"
				}) + " bis " + new Date(end_advance).toLocaleTimeString("de-de", {
					weekday: "short",
					hour: "2-digit",
					minute: "2-digit"
				});
				document.getElementById("warnings_icon").style.maskImage = "url(icons/info.svg)";
				document.getElementById("warnings_icon").style.webkitMaskImage = "url(icons/info.svg)";
				document.getElementById("warnings_container").style.background = "var(--warnlevel" + warn_level_advance + ")";
			}
		} else {
			document.getElementById("warnings").innerHTML = "<i>Aktuell keine Wetterwarnungen.</i>";
			document.getElementById("warnings_icon").style.display = "none";

			document.getElementById("warnings_container").style.background = "";
		}

		setLoadStatus(document.getElementById("warnings_load_data"));
	} catch (err) {
		console.warn(err);

		setLoadStatus(document.getElementById("warnings_load_data"), "error");
		document.getElementById("warnings_container").style.display = "none";
	}
}

async function getForecast() { //Vorhersage
	//setLoadStatus(document.getElementById("forecast_load_data"), "load");
	setLoadStatus(document.getElementById("forecast_detailed_load_data"), "load");
	setLoadStatus(document.getElementById("forecast_today_load_data"), "load");

	console.info("load foreacast");
	try {
		const today_offset = new Date().getHours();
		let data = JSON.parse(await fetchData("/api/weatherforecast"));
		let suninfo = JSON.parse(await fetchData("/api/suninfo"));
		
		data.forEach((e, i) => {
			let icon_arr = [];
			let rain = 0;
			let t_min = Infinity;
			let t_max = -Infinity;

			let icon_arr_detailed = [
				[],
				[],
				[],
				[]
			];
			let rain_detailed = [0, 0, 0, 0];
			let t_min_detailed = [Infinity, Infinity, Infinity, Infinity];
			let t_max_detailed = [-Infinity, -Infinity, -Infinity, -Infinity];

			e.forEach((h, hi) => {
				icon_arr.push(h.icon);
				rain += h.precipitation;
				t_min = Math.min(h.temperature, t_min);
				t_max = Math.max(h.temperature, t_max);

				const detailed_offset = parseInt(hi / 6);
				icon_arr_detailed[detailed_offset].push(h.icon);
				rain_detailed[detailed_offset] += h.precipitation;
				t_min_detailed[detailed_offset] = Math.min(h.temperature, t_min_detailed[detailed_offset]);
				t_max_detailed[detailed_offset] = Math.max(h.temperature, t_max_detailed[detailed_offset]);

				let offset = (i * 24 + hi) - today_offset;
				if (offset >= 0 && offset < 24) { //nur nächste 24 Stunden
					const t = new Date(h.timestamp);
					let dt = (t.getTime() >= new Date(suninfo[i].sunrise).getTime() && t.getTime() < new Date(suninfo[i].sunset).getTime() ? "day" : "night");

					document.getElementById("forecast_today_" + offset + "_time").innerHTML = t.getHours() + " <span class='unit'>Uhr</span>";
					document.getElementById("forecast_today_" + offset + "_icon").src = "weather_icons/" + getIcon2(h.icon, h.precipitation, dt) + ".svg";
					document.getElementById("forecast_today_" + offset + "_temp").innerHTML = formatNumber(h.temperature, 0) + " <span class='unit'>°C</span>";
					document.getElementById("forecast_today_" + offset + "_rain").innerHTML = formatNumber(h.precipitation, 1) + " <span class='unit'>mm</span>";
					document.getElementById("forecast_today_" + offset + "_winddir").innerHTML = winddir(h.wind_direction);
					document.getElementById("forecast_today_" + offset + "_wind").innerHTML = formatNumber(h.wind_speed, 0) + " <span class='unit'>km/h</span>";
				}
			});

			let icon = getIcon(icon_arr, rain);

			if (i == 0) {
				//document.getElementById("forecast_" + i + "_day").innerHTML = "Heute";
				document.getElementById("forecast_detailed_" + i + "_day").innerHTML = "Heute, " + new Date(e[0].timestamp).toLocaleString('de-DE', {
					day: "numeric",
					month: "numeric"
				});;
			} else {
				/*document.getElementById("forecast_" + i + "_day").innerHTML = new Date(e[0].timestamp).toLocaleString('de-DE', {
					weekday: 'long'
				});*/
				document.getElementById("forecast_detailed_" + i + "_day").innerHTML = new Date(e[0].timestamp).toLocaleString('de-DE', {
					weekday: 'long',
					day: "numeric",
					month: "numeric"
				});
			}

			/*document.getElementById("forecast_" + i + "_temp").innerHTML = formatNumber(t_min, 0) + " / " + formatNumber(t_max, 0) + " <span class='unit'>°C</span>";
			document.getElementById("forecast_" + i + "_icon").src = "weather_icons/" + icon + ".svg";*/
			document.getElementById("forecast_detailed_" + i + "_container").style.background = "url(weather_backgrounds2/" + icon + ".jpg)";
			document.getElementById("forecast_detailed_" + i + "_temp").innerHTML = formatNumber(t_min, 0) + " / " + formatNumber(t_max, 0) + " <span class='unit'>°C</span>";

			for (let j = 0; j < 4; j++) {
				let icon_detailed;
				if (j == 1 || j == 2) {
					icon_detailed = getIcon(icon_arr_detailed[j], rain_detailed[j]);
				} else {
					icon_detailed = getIcon(icon_arr_detailed[j], rain_detailed[j], "night");
				}

				document.getElementById("forecast_detailed_" + i + "_" + j + "_temp").innerHTML = formatNumber(t_min_detailed[j], 0) + " / " + formatNumber(t_max_detailed[j], 0) + " <span class='unit'>°C</span>";
				document.getElementById("forecast_detailed_" + i + "_" + j + "_rain").innerHTML = formatNumber(rain_detailed[j], 1) + " <span class='unit'>mm</span>";
				document.getElementById("forecast_detailed_" + i + "_" + j + "_icon").src = "weather_icons/" + icon_detailed + ".svg";
			}
		});

		//setLoadStatus(document.getElementById("forecast_load_data"));
		setLoadStatus(document.getElementById("forecast_detailed_load_data"));
		setLoadStatus(document.getElementById("forecast_today_load_data"));
	} catch (err) {
		console.warn(err);

		//setLoadStatus(document.getElementById("forecast_load_data"), "error");
		setLoadStatus(document.getElementById("forecast_detailed_load_data"), "error");
		setLoadStatus(document.getElementById("forecast_today_load_data"), "error");

		for (let i = 0; i < 4; i++) {
			/*document.getElementById("forecast_" + i + "_day").innerHTML = "-";
			document.getElementById("forecast_" + i + "_icon").scr = "weather_icons/null.svg";
			document.getElementById("forecast_" + i + "_temp").innerHTML = "-";*/
			document.getElementById("forecast_detailed_" + i + "_container").style.background = "";

			for (let j = 0; j < 4; j++) {
				document.getElementById("forecast_detailed_" + i + "_" + j + "_temp").innerHTML = "-";
				document.getElementById("forecast_detailed_" + i + "_" + j + "_rain").innerHTML = "-";
				document.getElementById("forecast_detailed_" + i + "_" + j + "_icon").src = "weather_icons/null.svg";
			}
		}

		for (let i = 0; i < 24; i++) {
			document.getElementById("forecast_today_" + i + "_time").innerHTML = "-";
			document.getElementById("forecast_today_" + i + "_icon").src = "weather_icons/null.svg";
			document.getElementById("forecast_today_" + i + "_temp").innerHTML = "-";
			document.getElementById("forecast_today_" + i + "_rain").innerHTML = "-";
			document.getElementById("forecast_today_" + i + "_winddir").innerHTML = "-";
			document.getElementById("forecast_today_" + i + "_wind").innerHTML = "-";
		}
	}
}

async function getRadar() { //Radar
	async function loadPrecipitationForecast() {
		setLoadStatus(document.getElementById("precipitation_forecast_load_data"), "load");

		const timestamp = Array.from(document.querySelectorAll(".precipitation_timestamps td"));
		const drop = Array.from(document.querySelectorAll(".precipitation_icons td maskimg"));

		try {
			let data = await fetchData("/api/radar_forecast");
			data = JSON.parse(data);
			data.forEach((e, i) => {
				if(i % 2 == 0) {
					let ind = parseInt(i / 2);
					let val = (i < data.length - 1 ? e.value : ((e.value / 12) + (data[i + 1].value / 12)) * 6); //Addiere 5 min Werte zu 10 min Werte
					drop[ind].style.background = "var(--rain" + precipitationLevel(val) + ")";
					drop[ind].style.maskImage = "url(icons/rain2_" + rainIcon(val) + ".svg)";
					drop[ind].style.webkitMaskImage = "url(icons/rain2_" + rainIcon(val) + ".svg)";
					if (i % 3 == 0) {
						timestamp[ind].innerHTML = leadingZero(new Date(e.time).getHours()) + ":" + leadingZero(new Date(e.time).getMinutes());
					} else {
						timestamp[ind].innerHTML = "";
					}
				}
			});
			setLoadStatus(document.getElementById("precipitation_forecast_load_data"));
		} catch (err) {
			console.warn(err);
			setLoadStatus(document.getElementById("precipitation_forecast_load_data"), "error");
			drop.forEach(e => {
				e.style.background = "var(--rain-1)";
				e.style.maskImage = "url(icons/rain2_0.svg)";
				e.style.webkitMaskImage = "url(icons/rain2_0.svg)";
			});
		}
	}

	if (!document.getElementById("map_layer_radar")) { //init
		const dom = document.getElementById("map_container");
		const display_size = [document.getElementById("map").clientWidth, document.getElementById("map").clientHeight];

		const data = JSON.parse(await fetchData("/api/radar_info"));

		dom.style.width = data.size.width + "px";
		dom.style.height = data.size.height + "px";

		dom.innerHTML += "<img id='map_layer_radar' class='map_overlayer' style='position: absolute; top: " + data.point.top + "px; left: " + data.point.left + "px; transform: translate(-50%, -50%);'>";
		dom.innerHTML += "<img id='map_baselayer' class='map_baselayer' src='/api/map'>";
		dom.innerHTML += "<maskimg id='map_marker' style='position: absolute; top: " + data.point.top + "px; left: " + data.point.left + "px;'></maskimg>";

		dom.style.marginLeft = ((display_size[0] / 2) - data.point.left) + "px";
		dom.style.marginTop = ((display_size[1] / 2) - data.point.top) + "px";
	}

	// update
	console.info("load radar");
	document.getElementById("map_layer_radar").src = "/api/radar?t=" + Date.now();

	await loadPrecipitationForecast();
}

async function updateWeather(set_autoupdate = true) {
	await getCurrent();
	await getWarnings();
	await getForecast();
	await getRadar();

	if (set_autoupdate) {
		const now = Date.now();
		const next_update = (parseInt(now / DATA_UPDATE_INTERVAL) * DATA_UPDATE_INTERVAL) + DATA_UPDATE_INTERVAL + DATA_UPDATE_DELAY;
		const time_to_next_update = next_update - now;

		console.info("next weather update:", time_to_next_update);

		setTimeout(updateWeather, time_to_next_update);
	}
}

/******************************************************************* */

function getIcon(values, rain = 0, daytime = "day", rain_limit = 0.4) { //summary
	let icon = "";
	if (values.includes("thunderstorm")) {
		icon = "thunderstorm";
	} else if (values.includes("hail")) {
		icon = "hail";
	} else if (values.includes("snow")) {
		icon = "snow";
	} else if (values.includes("sleet")) {
		icon = "sleet";
	} else if (values.includes("rain") || rain >= rain_limit) {
		icon = "rain";
	} else {
		let count = {};

		values.forEach(e => {
			let value = e.replace("-night", "-day");
			if (count.hasOwnProperty(value)) {
				count[value] += 1;
			} else {
				count[value] = 1;
			}
		});

		let max_value = [null, 0];

		Object.keys(count).forEach(e => {
			if (count[e] >= max_value[1]) {
				max_value = [e, count[e]];
			}
		});

		icon = max_value[0].replace("-day", "");
	}

	return icon + "-" + daytime;
}

function getIcon2(value, rain = 0, daytime = "day", rain_limit = 0.2) {
	let icon = "";
	if (value.includes("thunderstorm") || value.includes("hail") || value.includes("sleet") || value.includes("rain")) {
		icon = value;
	} else if (rain >= rain_limit) {
		icon = "rain";
	} else {
		value = value.replace("-night", "");
		value = value.replace("-day", "");
		icon = value;
	}

	return icon + "-" + daytime;
}

/*function getIconChar(name) {
	const ICON = {
		"clear-day": "f00d",
		"clear-night": "f02e",
		"partly-cloudy-day": "f002",
		"partly-cloudy-night": "f086",
		"cloudy-day": "f041",
		"cloudy-night": "f041",
		"cloudy": "f041",
		"rain-day": "f019",
		"rain-night": "f019",
		"rain": "f019",
		"sleet-day": "f0b5",
		"sleet-night": "f0b5",
		"sleet": "f0b5",
		"snow-day": "f01b",
		"snow-night": "f01b",
		"snow": "f01b",
		"hail-day": "f015",
		"hail-night": "f015",
		"hail": "f015",
		"fog-day": "f014",
		"fog-night": "f014",
		"fog": "f014",
		"thunderstorm-day": "f01e",
		"thunderstorm-night": "f01e",
		"thunderstorm": "f01e",
		"wind-day": "f011",
		"wind-night": "f011",
		"wind": "f011"
	};

	if(name in ICON) {
		return "&#x" + ICON[name];
	} else {
		return "?";
	}
}*/

function rainIcon(value) {
	if (value < 0) {
		return -1;
	} else if (value == 0) {
		return 0
	} else if (value <= 2.5) {
		return 1;
	} else if (value <= 15) {
		return 2;
	} else {
		return 3;
	}
}


function precipitationLevel(value) {
	if (value < 0) {
		return -1;
	} else if (value == 0) {
		return 0;
	} else if (value < 0.4) {
		return 1;
	} else if (value < 2) {
		return 2;
	} else if (value < 5) {
		return 3;
	} else if (value < 10) {
		return 4;
	} else if (value < 15) {
		return 5;
	} else if (value < 30) {
		return 6;
	} else if (value < 75) {
		return 7;
	} else if (value < 150) {
		return 8;
	} else {
		return 9;
	}
}

function winddir(dir) {
	dir = dir - Math.floor(dir / 360) * 360

	const a = 360 / 8;
	const b = Math.round(dir / a);
	const str = ["N", "NO", "O", "SO", "S", "SW", "W", "NW", "N"];
	return str[b];
}