$(document).ready(function(){
	$('.pop').popover({
		trigger: 'manual' ,
		placement: 'top',
		html: true
	})
	.on('mouseenter', function () {
	    var _this = this;
	    $(this).popover('show');
	    $('.popover').on('mouseleave', function () {
	        $(_this).popover('hide');
	    });
	}).on('mouseleave', function () {
	    var _this = this;
	    setTimeout(function () {
	        if (!$('.popover:hover').length) {
	            $(_this).popover('hide');
	        }
	    }, 300);
	});
})