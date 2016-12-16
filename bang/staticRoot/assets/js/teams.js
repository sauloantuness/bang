var getSkills = function(){
		$.ajax({
			type: 'GET',
			url: '/teams/skills',
			data: $("form").serialize(),
			success: function(skills) {
				var chart = $('#skills-chart').highcharts();
				
				while(chart.series.length > 0)
				    chart.series[0].remove();

				for(var i = 0; i < skills.length; i++)
					chart.addSeries(skills[i])
			}
		});
	};

$(document).ready(function(){
	$(".selectpicker").change(getSkills);
	getSkills();
});