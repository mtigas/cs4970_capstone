var NBMap = window.NBMap || {};

try {
    OpenLayers.IMAGE_RELOAD_ATTEMPTS = 2;
    OpenLayers.Util.onImageLoadErrorColor = "transparent";
} catch (e) {}

// In case OpenLayers doesn't load, define these out here
// since some functions may call on them on the global namespace (and null
// is way better than undefined).
NBMap.map = null;
NBMap.wkt_parser = null;
NBMap.sourceProj = null;
NBMap.targetProj = null;
NBMap.shapes = null;

// global var so this can be disabled on certain conditions (like when mousing
// over the list -- we don't want it to scroll then)
NBMap.list_autoscroll = true;

NBMap.wkt_to_vector = function(wkt) {
    // Converts WKT text (in WGS84) to a vector image (in the Google spherical mercator)

    // Punt on empty polygons or other bad data.
	var tempObj = NBMap.wkt_parser.read(wkt);
	if (!tempObj) return null;
	if (!NBMap.sourceProj) return null;
	if (!NBMap.targetProj) return null;
	
	var tempGeom = tempObj.geometry.clone();
	tempGeom.transform(NBMap.sourceProj, NBMap.targetProj);
	var obj = NBMap.wkt_parser.read(tempGeom);
	return obj
};
NBMap.cloneObj = function(what) {
    for (i in what) {
        this[i] = what[i];
    }
};

jQuery(function() {
	NBMap.sourceProj = new OpenLayers.Projection("EPSG:4326");
	NBMap.targetProj = new OpenLayers.Projection("EPSG:900913");
    
    NBMap.state_pop_style = new OpenLayers.Style({
    	strokeColor : '#777777',
    	strokeWidth: 1,
    	strokeOpacity: 0.5,
    	fillColor : '#FFFFFF', // Should be overridden by data styles
    	fillOpacity : 0.7,
    	pointRadius : 3,
    	strokeLinecap: "round"
    });
    NBMap.county_pop_style = new OpenLayers.Style({
    	strokeColor : '#777777',
    	strokeWidth: 1,
    	strokeOpacity: 0.5,
    	fillColor : '#FFFFFF', // Should be overridden by data styles
    	fillOpacity : 0.7,
    	pointRadius : 3,
    	strokeLinecap: "round"
    });
    NBMap.pop_density_style = new OpenLayers.Style({
    	strokeColor : '#777777',
    	strokeWidth: 1,
    	strokeOpacity: 0.5,
    	fillColor : '#FFFFFF', // Should be overridden by data styles
    	fillOpacity : 0.7,
    	pointRadius : 3,
    	strokeLinecap: "round"
    });
    NBMap.crime_rate_style = new OpenLayers.Style({
    	strokeColor : '#777777',
    	strokeWidth: 1,
    	strokeOpacity: 0.5,
    	fillColor : '#FFFFFF', // Should be overridden by data styles
    	fillOpacity : 0.7,
    	pointRadius : 3,
    	strokeLinecap: "round"
    });
    NBMap.per_capita_income_style = new OpenLayers.Style({
    	strokeColor : '#777777',
    	strokeWidth: 1,
    	strokeOpacity: 0.5,
    	fillColor : '#FFFFFF', // Should be overridden by data styles
    	fillOpacity : 0.7,
    	pointRadius : 3,
    	strokeLinecap: "round"
    });
    NBMap.hover_style = new OpenLayers.Style({
    	fillOpacity : 1,
    	strokeWidth: 3,
    	strokeOpacity: 1,
    	strokeColor : '#000000'
    });
    NBMap.create_rule_style_array = function(rule_property,in_arr) {
        // OpenLayers has the most verbose rule definition syntax
        // ever. Add the ability to create quick color-shading rules
        // based on a given attribute.

        // [[0,"#FEE391"],[10000,"FEC44F"],...]
        
        var out_arr = new Array();
        for(var i = 0; i<in_arr.length; i++){
            out_arr.push(new OpenLayers.Rule({
                filter: new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.GREATER_THAN_OR_EQUAL_TO,
                    property: rule_property,
                    value: in_arr[i][0]
                }),
                symbolizer: {
                    fillColor:in_arr[i][1]
                }
            }));
        }
        return out_arr;
    };

    NBMap.crime_rate_style.addRules(NBMap.create_rule_style_array(
        "violent_crime_rate", [
        [0,"#555555"],
        [1,"#FFFFE5"],
        [25,"#FFF7BC"],
        [50,"#FEE391"],
        [100,"#FE9929"],
        [250,"#EC7014"],
        [500,"#993404"]
    ]));
    NBMap.pop_density_style.addRules(NBMap.create_rule_style_array(
        "pop_density", [
        [0,"#FFFFE5"],
        [25,"#FFF7BC"],
        [50,"#FEE391"],
        [100,"#FEC44F"],
        [250,"#FE9929"],
        [500,"#EC7014"],
        [1000,"#CC4C02"],
        [2500,"#993404"],
        [5000,"#662506"]
    ]));
    NBMap.state_pop_style.addRules(NBMap.create_rule_style_array(
        "total_pop", [
        [0,"#FFFFE5"],
        [500000,"#FFF7BC"],
        [750000,"#FEE391"],
        [1000000,"#FE9929"],
        [5000000,"#EC7014"],
        [7500000,"#CC4C02"],
        [10000000,"#993404"],
        [15000000,"#662506"]
    ]));
    NBMap.county_pop_style.addRules(NBMap.create_rule_style_array(
        "total_pop", [
        [0,"#FFFFE5"],
        [10000,"#FFF7BC"],
        [50000,"#FEE391"],
        [75000,"#FEC44F"],
        [100000,"#FE9929"],
        [250000,"#EC7014"],
        [500000,"#CC4C02"],
        [1000000,"#993404"],
        [2000000,"#662506"]
    ]));
    NBMap.per_capita_income_style.addRules(NBMap.create_rule_style_array(
        "per_capita_income", [
        [0,"#555555"],
        [1,"#DEEBF7"],
        [10000,"#C6DBEF"],
        [20000,"#9ECAE1"],
        [30000,"#6BAED6"],
        [50000,"#4292C6"],
        [75000,"#2171B5"],
        [100000,"#084594"]
    ]));
    NBMap.state_pop_map = new OpenLayers.StyleMap({
        "default":NBMap.state_pop_style,
        "select":NBMap.hover_style
    });
    NBMap.county_pop_map = new OpenLayers.StyleMap({
        "default":NBMap.county_pop_style,
        "select":NBMap.hover_style
    });
    NBMap.pop_density_map = new OpenLayers.StyleMap({
        "default":NBMap.pop_density_style,
        "select":NBMap.hover_style
    });
    NBMap.crime_map = new OpenLayers.StyleMap({
        "default":NBMap.crime_rate_style,
        "select":NBMap.hover_style
    });
    NBMap.per_capita_income_map = new OpenLayers.StyleMap({
        "default":NBMap.per_capita_income_style,
        "select":NBMap.hover_style
    });
    
    
    jQuery(".map_to_crime").click(function(){
        NBMap.vectors.addOptions({
            styleMap: NBMap.crime_map
        });
        NBMap.vectors.refresh();
        NBMap.vectors.redraw();
        jQuery("#map_type_label").text("violent crime rate (per 100k residents)");
        return false;
    });
    jQuery(".map_to_state_pop").click(function(){
        NBMap.vectors.addOptions({
            styleMap: NBMap.state_pop_map
        });
        NBMap.vectors.refresh();
        NBMap.vectors.redraw();
        jQuery("#map_type_label").text("population size");
        return false;
    });
    jQuery(".map_to_county_pop").click(function(){
        NBMap.vectors.addOptions({
            styleMap: NBMap.county_pop_map
        });
        NBMap.vectors.refresh();
        NBMap.vectors.redraw();
        jQuery("#map_type_label").text("population size");
        return false;
    });
    jQuery(".map_to_density").click(function(){
        NBMap.vectors.addOptions({
            styleMap: NBMap.pop_density_map
        });
        NBMap.vectors.refresh();
        NBMap.vectors.redraw();
        jQuery("#map_type_label").text("population density (residents per sq. mi.)");
        return false;
    });
    jQuery(".map_to_per_capita").click(function(){
        NBMap.vectors.addOptions({
            styleMap: NBMap.per_capita_income_map
        });
        NBMap.vectors.refresh();
        NBMap.vectors.redraw();
        jQuery("#map_type_label").text("per-capita income");
        return false;
    });
});