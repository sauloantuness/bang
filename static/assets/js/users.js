var options = {
    useEasing : true, 
    useGrouping : true, 
    separator : ',', 
    decimal : '.', 
    prefix : '', 
    suffix : '' 
};

$("#profile strong").each(function(index, item){
	var demo = new CountUp(item, 0, $(item).html(), 0, 5, options);
	demo.start();	
});
