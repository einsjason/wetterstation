async function init() {
	console.info("init");

	setInterval(clock, 1000);
	clock();

	await getSpotlight();

	await updateWeather();

	setPage("clock"); // Radar muss geladen werden, bevor die Seite mit dem Radar unsichtbar wird
}

/****************************************************************************/

const SPOTLIGHT_UPDATE_INTERVAL = 86400000;//21600000;
const DATA_UPDATE_INTERVAL = 300000;
const DATA_UPDATE_DELAY = 15000;

const pages = Array.from(document.getElementsByTagName("main"));
const menu = document.getElementsByTagName("menu")[0];
const menu_btn = document.getElementById("home");

let touch = {
	start_x: 0,
	end_x: 0,
	start_y: 0,
	end_y: 0
};
let mousewheel = {
	x: 0,
	y: 0
}

document.addEventListener('touchstart', event => {
	touch.start_x = event.changedTouches[0].screenX;
	touch.start_y = event.changedTouches[0].screenY;
});

document.addEventListener('touchend', event => {
	touch.end_x = event.changedTouches[0].screenX;
	touch.end_y = event.changedTouches[0].screenY;
	touchEvent();
});

/*document.addEventListener('mousedown', event => {
	touch.start_x = event.screenX;
	touch.start_y = event.screenY;
});
document.addEventListener('mouseup', event => {
	touch.end_x = event.screenX;
	touch.end_y = event.screenY;
	touchEvent();
});*/

document.addEventListener("wheel", (event) => {
	mousewheel.x = event.deltaX;
	mousewheel.y = event.deltaY;
	wheelEvent();
});

window.onload = (event) => {
	init();
};