$(document).ready(function(){

	var historic = Historic();

	historic.setupButtons();
	historic.setupChart();
});

var Historic = function(){
	var chart;

	var setupButtons = function(){
		$('#historic-panel .btn-group button').click(function(el){
			$('#historic-panel .btn-group button.active').removeClass('active');
			var btn = el.target;
			$(btn).addClass('active');
			document.activeElement.blur();

			var period = $(btn).data('period');
			updateChart(period);
		});
	}

	var setupChart = function(){
		$('#historic-chart').highcharts({
		    chart: {
		        type: 'line'
		    },
		    xAxis: {
		        categories: days
		    },
		    yAxis: {
		        title: {
		            text: null
		        }
		    },
		    series: [{
		        data: problems_solved,
		        type: 'spline',
		        marker: {
		            enabled: false
		        }
		    }],
		    legend: {
		    	enabled: false
		    },
		    title: {
		    	text: null
		    },
		    tooltip: {
		    	formatter: function(){
		    		return 'Solved <b>' + this.y + '</b>';
		    	}
		    }
		});

		chart = $('#historic-chart').highcharts();
	}

	var updateChart = function(period){
		var type = $('#historic-panel').data('type');
		var id = $('#historic-panel').data('id');

		$.getJSON('/api/historic/' + period + '/' + type + '/' + id, function(response){
			chart.xAxis[0].update({
				categories: response.xAxis
			})
			
			chart.series[0].update({
				data: response.series
			});
		});
	};

	return {
		setupButtons: setupButtons,
		setupChart: setupChart,
		updateChart: updateChart
	};
}
