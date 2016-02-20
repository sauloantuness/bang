$(function () { 
    $('#myChart').highcharts({
        chart: {
            type: 'line'
        },
        xAxis: {
            categories: ['12/02', '13/02', '14/02', '15/02', '16/02', '17/02', '18/02']
        },
        yAxis: {
            title: {
                text: null
            }
        },
        series: [{
            data: [1, 0, 4, 0, 3, 1, 2]
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