$(document).ready(function(){
	["#uri", "#uva", "#spoj"].forEach(function(id){
		$(id + " input").keyup(function(input){
			var value = input.target.value.toLowerCase();

			$(id).find("a").each(function(index, item){
				var title = $(item).attr("title").toLowerCase();
				var code = $(item).html().toLowerCase();

				if(title.indexOf(value) == -1 && code.indexOf(value) == -1){
					$(item).parent().hide();
				}
				else {
					$(item).parent().show();
				}
			});
		});

		var minWidth = 0;
		$(id + " li").each(function(index, item){
			if($(item).width() > minWidth)
				minWidth = $(item).width();
		});

		minWidth += 10;

		$(id + " li").each(function(index, item){
			$(item).css("width", minWidth);
		});

	});
})