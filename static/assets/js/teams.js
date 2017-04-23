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

var selectBestTeam = function(){
		$('.fa-star').removeClass('fa-star').addClass('fa-circle-o-notch fa-spin');
		$('#best-team').prop('disabled', true);

		$.ajax({
			type: 'GET',
			url: '/teams/best_team',
			success: function(profiles) {
				$('#id_profiles').selectpicker('deselectAll');
				$('#id_profiles').val(profiles);
				$('#id_profiles').selectpicker('render');
				$('#id_profiles').trigger('change');
				$('.fa-circle-o-notch').removeClass('fa-circle-o-notch fa-spin').addClass('fa-star');
				$('#best-team').prop('disabled', false);
			}
		});
	};


$(document).ready(function(){
	$(".selectpicker").change(getSkills);
	getSkills();
});