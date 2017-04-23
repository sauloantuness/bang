var trip = new Trip([
  { 
    sel : $('.panel.panel-default').first(),
    content : 
    	'<h4>University Rank</h4>' +
    	'<p>You can also compete with other students from the same institution as you.</p>',
    expose : true,
    position: "t",
    delay: 5000
  },
  {
      // Step 12
      sel: $('#historic-panel'),
      position: 's',
      content: 
          '<h4>University Rank</h4>' +
          '<p>You can also compete with other students from the same institution as you.</p>',
      expose: true,
      delay: 5000
  },
  { 
    sel : $('#group'),
    content : 'This is element 1',
    expose : true,
    position: "e"
  }
]);

$(document).ready(function(){
	trip.start();
});
