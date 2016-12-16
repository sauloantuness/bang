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
});

function maskDate(event){
    if(event.keyCode == 8)
        return true;

    if(event.target.value.length == 2 || event.target.value.length == 5)
        event.target.value += '/'

    return true;
}

function maskTime(event){
    if(event.keyCode == 8)
        return true;

    if(event.target.value.length == 2)
        event.target.value += ':'

    return true;
}

function filterNumber(event){
    if(event.charCode >= 48 && event.charCode <= 57)
       return;
    else 
        event.preventDefault();
}

function checkDateAndTime(event){
    var date_str = document.getElementsByName('date')[0].value;
    var time_str = document.getElementsByName('time')[0].value;
    var date = Date.parse(date_str + " " + time_str);
    if(date)
        return true;
    else{
        event.preventDefault();
        alert("Invalid date or time")
        return false;
    }
}

document.getElementsByName('date')[0].addEventListener('keypress', filterNumber);
document.getElementsByName('time')[0].addEventListener('keypress', filterNumber);
document.getElementsByName('date')[0].addEventListener('keyup', maskDate);
document.getElementsByName('time')[0].addEventListener('keyup', maskTime);
document.getElementById('contestForm').addEventListener('submit', checkDateAndTime);
