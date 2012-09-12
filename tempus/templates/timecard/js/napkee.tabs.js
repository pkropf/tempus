(function($){
	$.fn.napkeeTabs = function(options) {
		var defaults = {
			position: 'top',
			alignment: 'left',
			selectedTab: 0,
			width: 247,
			height: 100
		},
		settings = $.extend({}, defaults, options);
		var mainTabs = this;
		
		//console.log($("#" + this.attr("id") + "n").width());
		if (settings.position == "left" || settings.position == "right" ){
			$("#" + mainTabs.attr("id")+"t > div").height(settings.height);
			$("#" + mainTabs.attr("id")+"t").width(settings.width-$("#" + this.attr("id") + "n").width());
			$("#" + mainTabs.attr("id")+"n").addClass("napkeeVerticalTabs");
			if (settings.position=="left"){
				$("#" + mainTabs.attr("id")+"n").addClass("napkeeVerticalTabsLeft");
				$("#" + mainTabs.attr("id")+"t").css("margin-left",($("#" + this.attr("id") + "n").width()-1)+"px");
			}
			if (settings.position=="right"){
				$("#" + mainTabs.attr("id")+"n").addClass("napkeeVerticalTabsRight");
			}
		}
		if (settings.position == "top" || settings.position == "bottom"){
			$("#" + mainTabs.attr("id")+"n").addClass("napkeeHorizontalTabs");
			$("#" + mainTabs.attr("id")+"t").width(settings.width);
			$("#" + mainTabs.attr("id")+"t > div").height(settings.height-$("#" + this.attr("id") + "n").height());
			if (settings.position=="top"){
				$("#" + mainTabs.attr("id")+"n").addClass("napkeeHorizontalTabsTop");
				$("#" + mainTabs.attr("id")+" tr td").filter(":first").attr("align",settings.alignment);
			}
			if (settings.position=="bottom"){
				$("#" + mainTabs.attr("id")+"n").addClass("napkeeHorizontalTabsBottom");
				$("#" + mainTabs.attr("id")+"n").css("margin-top",(settings.height-$("#" + mainTabs.attr("id")+"n").height()+9)+"px")
				$("#" + mainTabs.attr("id")+" tr td").filter(":last").attr("align",settings.alignment);
			}
		}
        var tabContainers = $("#" + mainTabs.attr("id")+"t > div");
        tabContainers.hide().filter(':first').show();
        $("#" + mainTabs.attr("id")+"n a").click(function () {
                tabContainers.hide();
                tabContainers.filter(this.hash).show();
                $("#" + mainTabs.attr("id")+"n a").removeClass('selected');
				$("#" + mainTabs.attr("id")+"n li").removeClass('selected');
                $(this).addClass('selected');
				$(this).parent().addClass('selected');
                return false;
        }).filter(':eq('+settings.selectedTab+')').click();
		
		return this;
	}
})(jQuery);