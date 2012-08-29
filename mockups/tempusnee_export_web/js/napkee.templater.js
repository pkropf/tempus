function showMockup(url,params){
	var finalUrl = url + "?";
	if (params!=null){
		jQuery.each(params, function(par, field){
			finalUrl += par + "=" + $("#"+field).val() + "&";
		});
	}
	location.href = finalUrl;
}

function hideElement(elementID){
	$("#"+elementID).hide();
}

function showElement(elementID){
	$("#"+elementID).show();
}

function toggleElement(elementID){
	$("#"+elementID).toggle();
}

function applyValue(field,qsInput){
	if (field!=null && field!=""){
		if ($.getQueryString({ ID:qsInput }) != "undefined"){
			eval('$("#"+field).text($.substitute($("#"+field).text(), { '+qsInput+': $.getQueryString({ ID:qsInput })}));');
		}
	}
}

function supportsSvg() {
    return document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#BasicStructure", "1.1");
}