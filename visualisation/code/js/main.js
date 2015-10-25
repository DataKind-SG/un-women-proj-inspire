var animate_intervalid;
var animate_interval_year;


$( document ).ready(function() {
	console.log("Loading....");
	initMap("map");
	renderMapData("Title","Subtitle",applicationsPerYearPerCountryJSON);
	$(".year_button").bind("click", function (){
		loadButtonData(this.id);
	});
});

function loadButtonData(buttonId) {
	console.log("Clicked " + buttonId);
	window[buttonId]();	
}

function year_2011() {
	var yearData = applicationsPerYearPerCountryJSON.year_2011;
//	console.log(yearData);
	renderMapData("UN Women : Inspire Project","Year 2011",yearData);
}
function year_2012() {
	var yearData = applicationsPerYearPerCountryJSON.year_2012;
//	console.log(yearData);
	renderMapData("UN Women : Inspire Project","Year 2012",yearData);
}
function year_2013() {
	var yearData = applicationsPerYearPerCountryJSON.year_2013;
//	console.log(yearData);
	renderMapData("UN Women : Inspire Project","Year 2013",yearData);
}
function year_2014() {
	var yearData = applicationsPerYearPerCountryJSON.year_2014;
//	console.log(yearData);
	renderMapData("UN Women : Inspire Project","Year 2014",yearData);
}
function year_2015() {
	var yearData = applicationsPerYearPerCountryJSON.year_2015;
//	console.log(yearData);
	renderMapData("UN Women : Inspire Project","Year 2015",yearData);
}

function animate() {
	if (animate_intervalid) {
		clearInterval(animate_intervalid);
	}
	else {
		animate_interval_year = 2010;
		animate_intervalid = setInterval(function() {
			if (animate_interval_year == 2015 ) {
				animate_interval_year = 2011;
			}
			else {
				animate_interval_year++;
			}
			window['year_' + animate_interval_year]();
		}, 2000);
	}
}