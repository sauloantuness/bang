$(document).ready(function(){
    $('#skills-chart').highcharts({
        chart: {
            polar: true,
            type: 'line'
        },

        title: {
        	text: null
        },

        pane: {
            size: '80%'
        },

        xAxis: {
            categories: ['Beginner', 'Ad-Hoc', 'Strings', 'Data Structures', 'Mathematics', 'Paradigms', 'Graph', 'Computational Geometry', 'Uncategorized'],
            tickmarkPlacement: 'on',
            lineWidth: 0
        },

        yAxis: {
            gridLineInterpolation: null,
            lineWidth: 0,
            min: 0
        },

        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: false
                }
            }
        },
        series: series || []
    });
});