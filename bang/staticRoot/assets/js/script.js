$(function () { 
    $('#myChart').highcharts({
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
            data: problems_solved
        }],
        legend: {
        	enabled: false
        },
        title: {
        	text: null
        },
        tooltip: {
        	formatter: function(){
        		return 'Resolvidos <b>' + this.y + '</b>';
        	}
        }
    });
});