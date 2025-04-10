function clock() { //Uhr
	const hand_hour = document.getElementById("hand-hour");
	const hand_minute = document.getElementById("hand-minute");
	const hand_second = document.getElementById("hand-second");

	const time = new Date();

	const second = time.getSeconds();
	const minute = time.getMinutes();
	const hour = time.getHours();

	const secondDeg = (second / 60) * 360;
	hand_second.style.transform = "rotate(" + secondDeg + "deg)";

	const minuteDeg = ((minute + (second / 60)) / 60) * 360;
	hand_minute.style.transform = "rotate(" + minuteDeg + "deg)";

	const hourDeg = ((hour + ((minute + (second / 60)) / 60)) / 12) * 360;
	hand_hour.style.transform = "rotate(" + hourDeg + "deg)";

	const text_full_date = document.getElementById("text-full-date");
	const text_full_time = document.getElementById("text-full-time");
	const text_full_time_seconds = document.getElementById("text-full-time-seconds");

	const time_string = time.toLocaleTimeString("de-DE", {
		hour: '2-digit',
		minute: '2-digit',
		second: '2-digit'
	});

	text_full_time.innerHTML = time_string.substring(0, time_string.lastIndexOf(":"));
	text_full_time_seconds.innerHTML = time_string.substring(time_string.lastIndexOf(":") + 1);
	text_full_date.innerHTML = time.toLocaleDateString("de-DE", {
		weekday: 'long',
		/*year: 'numeric',*/
		month: 'long',
		day: 'numeric'
	});
}

async function getSpotlight(set_autoupdate = true) { //Hintergrundbild
	console.info("update spotlight");
	document.querySelector(":root").style.setProperty('--bg0', "var(--bg0-default)");
	document.querySelector(":root").style.setProperty('--bg1', "var(--bg1-default)");
	await fetchData("/api/update_spotlight");
	document.querySelector(":root").style.setProperty('--bg0', "url(/spotlight/image.jpg?t=" + Date.now() + ")");

	let info = JSON.parse(await fetchData("/spotlight/info.json"));
	document.getElementById("spotlight_info").innerText = info.description;
	document.querySelector(":root").style.setProperty('--bg1', info.color)

	if (set_autoupdate) {
		const now = Date.now() - (new Date().getTimezoneOffset() * 60000); //Zeitzonenverschiebung
		const next_update = (parseInt(now / SPOTLIGHT_UPDATE_INTERVAL) * SPOTLIGHT_UPDATE_INTERVAL) + SPOTLIGHT_UPDATE_INTERVAL;
		const time_to_next_update = next_update - now;

		console.info("next spotlight update:", time_to_next_update);

		setTimeout(getSpotlight, time_to_next_update);
	}
}

function setPage(content = null) {
	pages.forEach(e => {
		e.style.display = "none";
	});

	document.querySelector("main#" + content).style.display = "";
}

function switchPage(count) {
	let page = -1;
	pages.forEach((p, i) => {
		if (p.style.display != "none") {
			page = i;
		}
	});
	page += count;
	if (page >= pages.length) {
		page = 0;
	} else if (page < 0) {
		page = pages.length - 1;
	}

	setPage(pages[page].getAttribute("id"));
}

function switchMenu(value = null) {
	if (value == null) {
		value = menu.style.display == "none";
	}
	if (value) {
		menu.style.display = "";
		menu_btn.style.color = "currentColor";

	} else {
		menu.style.display = "none";
		menu_btn.style.color = "";
	}
}

async function fetchData(url) {
	const request = await fetch(url);
	const response = await request.text();
	return response;
}

function leadingZero(value) {
	if (value < 10) {
		return "0" + String(value);
	} else {
		return String(value);
	}
}

function formatNumber(number, digits = 1, mark_digits = true) {
	number = parseFloat(number);
	let num = number.toFixed(digits);
	if (mark_digits && digits > 0) {
		const i = num.indexOf(".");
		num = num.substring(0, i) + "<span class='digit'>" + num.substring(i) + "</span>";
	}
	return num;
}

function timeZoneOffset() {
	const offset = -new Date().getTimezoneOffset();
	let result = "";
	if (offset < 0) {
		result += "-";
	} else {
		result += "+";
	}
	const hours = parseInt(offset / 60);
	result += leadingZero(hours);
	const minutes = offset - (hours * 60);
	result += ":" + leadingZero(minutes);
	return result;
}

function formatUnixTime(value) {
	if (isNaN(value)) {
		return value;
	} else {
		return value * 1000;
	}
}

function setLoadStatus(element, status = null) {
	element.classList.remove("load_data");
	element.classList.remove("load_data_error");

	switch (status) {
		case "load":
			element.classList.add("load_data");
			break;

		case "error":
			element.classList.add("load_data_error");
			break;
	}
}

function wheelEvent() {
	if(mousewheel.y > 0 || mousewheel.x > 0) {
		switchPage(1);
		switchMenu(false);
	} else if(mousewheel.y < 0 || mousewheel.x < 0) {
		switchPage(-1);
		switchMenu(false);
	}
}

function touchEvent() {
	const vec = {
		x: touch.end_x - touch.start_x,
		y: touch.end_y - touch.start_y,
		len: Math.sqrt((touch.end_x - touch.start_x) ** 2 + (touch.end_y - touch.start_y) ** 2)
	};
	const vec0 = {
		x: 0,
		y: 1,
		len: 1
	};
	if(vec.len >= 32) {
		let deg = Math.acos((vec0.x * vec.x + vec0.y * vec.y) / (vec0.len * vec.len));
		deg *= (180 / Math.PI);
		if (vec.x < 0) {
			deg = 360 - deg;
		}
		resolution = 360 / 4;
		deg += resolution / 2;
		deg = Math.floor(deg / resolution) * resolution;
		deg = deg - Math.floor(deg / 360) * 360;

		switch(deg) {
			case 90:
				switchPage(-1);
				switchMenu(false);
				break;

			case 270:
				switchPage(1);
				switchMenu(false);
				break;

			case 180:
				switchMenu(true);
				break;
			
			case 0:
				switchMenu(false);
				break;
		}
	}
}