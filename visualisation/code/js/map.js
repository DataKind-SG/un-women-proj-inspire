var hcMap;

function initMap(mapDivId) {
	var hcMapOptions = {
			chart : {
				borderWidth : 1,
				renderTo : mapDivId
			},

			legend: {
				enabled: false
			},

			mapNavigation: {
				enabled: true,
				buttonOptions: {
					verticalAlign: 'bottom'
				}
			},

			exporting: {
				fallbackToExportServer: false
			}

		};
	hcMap  = new Highcharts.Map (hcMapOptions);
}

function renderMapData(cTitle, cSubtitle, data) {
	var mapData = Highcharts.geojson(Highcharts.maps['custom/world']);

	var hcMapOptions = hcMap.options;
	console.log(hcMapOptions);
	console.log(cTitle + " - " + cSubtitle);

	hcMapOptions.title = {text : cTitle};
	hcMapOptions.subtitle = {text : cSubtitle};

	hcMapOptions.series = new Array();
	hcMapOptions.series.push({
				name: 'Countries',
				mapData: mapData,
				color: '#E0E0E0',
				enableMouseTracking: false
			}); 
	hcMapOptions.series.push({
				type: 'mapbubble',
				mapData: mapData,
				name: cSubtitle,
				joinBy: ['iso-a2', 'code'],
				data: data,
				minSize: 4,
				maxSize: '12%',
				tooltip: {
					pointFormat: '{point.country}: {point.z}'
				}
			});
	hcMap = new Highcharts.Map (hcMapOptions);
}