/****************************************************************************************************/
/*                                                                                                  */
/* Substitute v1.1 for jQuery 1.3+                                                                  */
/* Untested with previous version of jQuery, however it is assumed to work.                         */
/*                                                                                                  */
/* DESCRIPTION:                                                                                     */
/* Based on the substitute method for the Flex class StringUtil                                     */
/* (http://livedocs.adobe.com/flex/3/langref/mx/utils/StringUtil.html) and on the Prototype         */
/* Template method (http://www.prototypejs.org/api/template). Substitute replaces a word group with */
/* another specified group of words.                                                                */
/*                                                                                                  */
/* SYNTAC:                                                                                          */
/*    var str = "This is a {demo} to see if it {works}";                                            */
/*    var output = $.substitute(str, {demo:"test", works:"is working"};                             */
/*         // will output "This is a test to see if it is working"                                  */
/*                                                                                                  */
/* CHANGELOG:                                                                                       */
/*   090525                                                                                         */
/*     - Plugin started and completed.                                                              */
/*   090610                                                                                         */
/*     - Updated structure of extension.                                                            */
/*                                                                                                  */
/****************************************************************************************************/

(function($){
	$.extend({			
		substitute: function(str, obj, flag)
		{	
			flag = flag || "g";
			jQuery.each(obj, function(i, val){
				var re = new RegExp("(\{\s*(" + i + ")\s*})", flag);
				str = str.replace(re, val);
			});
			return str;
		}
	});
})(jQuery);
