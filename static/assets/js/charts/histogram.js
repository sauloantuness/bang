histogramChart = Highcharts.chart('histogram-chart', {
    chart: {
        type: 'column'
    },
    title: {
        text: null
    },
    xAxis: {
        categories: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        title: {
            text: 'Level'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Solutions',
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        formatter: function () {
            return 'Level <b>' + this.x + '</b>' + 
             	     ' had <b>' + this.y + ' </b> solutions';
        }
    },
    credits: {
        enabled: false
    },
    series: [{
    	showInLegend: false,
        name: 'Solutions',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }]
});

var MyDate = (function(){
	var $histogramDate = $("#histogram-date"); 
	var monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];

	var next = function() {
		var year = $histogramDate.data('year')
		var month = $histogramDate.data('month')
		
		month = month + 1;

		if (month == 12) {
			year = year + 1;
			month = 0;
		}

		$histogramDate.data('year', year);
		$histogramDate.data('month', month);
		$histogramDate.text(monthNames[month] + '/' + (year % 100))
	}

	var prev = function() {
		var year = $histogramDate.data('year')
		var month = $histogramDate.data('month')
	
		month = month - 1;

		if (month == -1) {
			year = year - 1;
			month = 11;
		}

		$histogramDate.data('year', year);
		$histogramDate.data('month', month);
		$histogramDate.text(monthNames[month] + '/' + (year % 100))
	}

	return {
		next: next,
		prev: prev
	}
})();


$(document).ready(function() {
	$('#histogram-prev').on('click', function(ev) {
		MyDate.prev();
		$(ev.target).blur()
		updateHistogramChart();
	})
	
	$('#histogram-next').on('click', function(ev) {
		MyDate.next();
		$(ev.target).blur()
		updateHistogramChart();
	})

	$('#histogram-category').on('click', 'a', function(ev) {
		ev.preventDefault();
		var category = $(ev.target).data('category');
		$('#histogram-category').data('category', category);

		$('#histogram-category button span').first().text($(ev.target).text())
		updateHistogramChart()
	})

	updateHistogramChart();
})

var updateHistogramChart = function(){
	var type = $('#histogram-panel').data('type');
	var id = $('#histogram-panel').data('id');
	var year = $('#histogram-date').data('year');
	var month = $('#histogram-date').data('month');
	var category = $('#histogram-category').data('category');

	$.getJSON('/api/histogram/' + type + '/' + id + '/' + year + '/' + (month + 1) + '/' + category, function(response){
		histogramChart.series[0].setData(response.series);
	});
};