$(document).ready(function() {

	$('#event-left').on('click', function(ev) {
		var $currentEvent = $('#events .event:visible');
		var $prevEvent = $currentEvent.prev('.event');

		if($prevEvent.length) {
			$currentEvent.addClass('slideOutRight');
			
			setTimeout(function(){
				$currentEvent.hide().removeClass('slideOutRight');
				$prevEvent.show();
			}, 300)
		}
	})
	
	$('#event-rigth').on('click', function(ev) {
		var $currentEvent = $('#events .event:visible');
		var $nextEvent = $currentEvent.next('.event');

		if($nextEvent.length) {
			$currentEvent.addClass('slideOutLeft');

			setTimeout(function(){
				$currentEvent.hide().removeClass('slideOutLeft');
				$nextEvent.show();
			}, 300)
		}
	})
})