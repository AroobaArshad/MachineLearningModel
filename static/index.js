$(document).ready(function() {
  var marker = 'black';
  var markerWidth = 10;

  var lastEvent;
  var mouseDown = false;

  var $canvas = $('canvas');
  var context = $canvas[0].getContext('2d');
  context.fillStyle = "white";
  context.fillRect(0, 0, $canvas[0].width, $canvas[0].height);

  // Mouse events
  $canvas.mousedown(function(e) {
    lastEvent = e;
    mouseDown = true;
  }).mousemove(function(e) {
    if (mouseDown) {
      context.beginPath();
      context.moveTo(lastEvent.offsetX, lastEvent.offsetY);
      context.lineTo(e.offsetX, e.offsetY);
      context.lineWidth = markerWidth;
      context.strokeStyle = marker;
      context.lineCap = 'round';
      context.stroke();
      lastEvent = e;
    }
  }).mouseup(function() {
    mouseDown = false;
  });

  // Touch events for mobile support
  $canvas[0].addEventListener('touchstart', function(e) {
	e.preventDefault(); // Prevent scrolling while drawing
	var touch = e.touches[0];
	var rect = $canvas[0].getBoundingClientRect();  // Accurate canvas position
	lastEvent = { 
	  offsetX: touch.clientX - rect.left, 
	  offsetY: touch.clientY - rect.top 
	};
	mouseDown = true;
  });
  
  $canvas[0].addEventListener('touchmove', function(e) {
	if (mouseDown) {
	  e.preventDefault(); // Prevent scrolling while drawing
	  var touch = e.touches[0];
	  var rect = $canvas[0].getBoundingClientRect();  // Accurate canvas position
	  context.beginPath();
	  context.moveTo(lastEvent.offsetX, lastEvent.offsetY);
	  context.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
	  context.lineWidth = markerWidth;
	  context.strokeStyle = marker;
	  context.lineCap = 'round';
	  context.stroke();
	  lastEvent = { 
		offsetX: touch.clientX - rect.left, 
		offsetY: touch.clientY - rect.top 
	  };
	}
  });
  
  $canvas[0].addEventListener('touchend', function() {
    mouseDown = false;
  });

  // Clear button functionality
  $('#clear').click(function() {
    context.clearRect(0, 0, $canvas[0].width, $canvas[0].height);
    context.fillStyle = "white";
    context.fillRect(0, 0, $canvas[0].width, $canvas[0].height);
  });
});
