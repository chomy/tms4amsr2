function init() {
    var options = {
	controls: [
	    new OpenLayers.Control.Navigation({mouseWheelOptions: {interval: 100}}),
	    new OpenLayers.Control.PanZoomBar(),
	    new OpenLayers.Control.KeyboardDefaults(),
	    new OpenLayers.Control.LayerSwitcher(),
	    new OpenLayers.Control.Attribution()
	],
	projection: new OpenLayers.Projection("EPSG900913"),
	displayProjection: new OpenLayers.Projection("EPSG:4326"),
	units: "m",
	//		maxResolution: 156543.0339,
	maxExtent: new OpenLayers.Bounds(-20037508, -20037508, 20037508, 20037508.34)
    };
    var map = new OpenLayers.Map("canvas", options);
    map.addControl(new OpenLayers.Control.Attribution());
    var mapnik = new OpenLayers.Layer.OSM();
    
    var snd = new OpenLayers.Layer.TMS("Sea Surface Temperature", 
				       "http://tms.hi-rezclimate.org/amsr2/",
				       {url:'http://tms.hi-rezclimate.org/amsr2/', 
					layername:'sst', 
					type:'png',
					alpha: true,
					isBaseLayer: false,
					attribution: 'Original Data Provided by JAX/A <img src="http://tms.hi-rezclimate.org/amsr2/sst/sst_scale.png">',
					opacity: 0.7
				       }
				      );
    
    map.addLayers([mapnik, snd]);
    
    
//    var lonLat = new OpenLayers.LonLat(139.76, 35.68)
    var lonLat = new OpenLayers.LonLat(-170.42, 25.96)
        .transform(
            new OpenLayers.Projection("EPSG:4326"),
            new OpenLayers.Projection("EPSG:900913")
        );
    map.setCenter(lonLat, 3);
    
}