/* JQueryString v1.6.1
   By James Campbell 
   Many thanks to Mike Willis for his suggestions and additions to this jQuery plugin.
*/
(function($) {
$.getAllQueryStrings = function(options){
	defaults = {DefaultValue:"undefined", URL:window.location.href} ;
	options = $.extend(defaults , options);
	var qs;
	var args = new Array();
	if(typeof(options.URL.split( "?" )[1]) != "undefined"){
		qs = options.URL.split( "?" )[1].replace(/\+/g, ' ').split('&');
		$.each(qs, function(i){
			var currentArg = this.split('=');
			if(currentArg.length == 2){		
				args[i] = {name:currentArg[0], value:currentArg[1]};
				args[currentArg[0]] = {name:currentArg[0], value:currentArg[1]};
			}else{
				args[i] = {name:currentArg[0], value:currentArg[1]};
				args[currentArg[0]] = {name:currentArg[0], value:currentArg[0]};
			}
		});
	}
	if (args.length <= 0) {};
	return args;
}
$.getQueryString = function(options)
{
	defaults = {DefaultValue:"undefined", URL:window.location.href} ;
	options = $.extend(defaults , options);
	if(typeof($.getAllQueryStrings({URL:options.URL})[options.ID]) == "undefined"){
		return options.DefaultValue;
	}else{
		return $.getAllQueryStrings({DefaultValue:options.DefaultValue, URL:options.URL})[options.ID].value;
	}
};
})(jQuery);
