$(document).ready(function() {
    var marker = 'black';
    var markerWidth = 10;
  
    var lastEvent;
    var mouseDown = false;
  
    var $animalCanvas = $('#animalCanvas');
    var contextAnimal = $animalCanvas[0].getContext('2d');
    contextAnimal.fillStyle = "white";
    contextAnimal.fillRect(0, 0, $animalCanvas[0].width, $animalCanvas[0].height);
  
    // Mouse events
    $animalCanvas.mousedown(function(e) {
      lastEvent = e;
      mouseDown = true;
    }).mousemove(function(e) {
      if (mouseDown) {
        contextAnimal.beginPath();
        contextAnimal.moveTo(lastEvent.offsetX, lastEvent.offsetY);
        contextAnimal.lineTo(e.offsetX, e.offsetY);
        contextAnimal.lineWidth = markerWidth;
        contextAnimal.strokeStyle = marker;
        contextAnimal.lineCap = 'round';
        contextAnimal.stroke();
        lastEvent = e;
      }
    }).mouseup(function() {
      mouseDown = false;
    });
  
    // Touch events for mobile support
    $animalCanvas[0].addEventListener('touchstart', function(e) {
      e.preventDefault();
      var touch = e.touches[0];
      var rect = $animalCanvas[0].getBoundingClientRect();
      lastEvent = {
        offsetX: touch.clientX - rect.left,
        offsetY: touch.clientY - rect.top
      };
      mouseDown = true;
    });
  
    $animalCanvas[0].addEventListener('touchmove', function(e) {
      if (mouseDown) {
        e.preventDefault();
        var touch = e.touches[0];
        var rect = $animalCanvas[0].getBoundingClientRect();
        contextAnimal.beginPath();
        contextAnimal.moveTo(lastEvent.offsetX, lastEvent.offsetY);
        contextAnimal.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
        contextAnimal.lineWidth = markerWidth;
        contextAnimal.strokeStyle = marker;
        contextAnimal.lineCap = 'round';
        contextAnimal.stroke();
        lastEvent = {
          offsetX: touch.clientX - rect.left,
          offsetY: touch.clientY - rect.top
        };
      }
    });
  
    $animalCanvas[0].addEventListener('touchend', function() {
      mouseDown = false;
    });
  
    // Clear button functionality for Animal Canvas
    $('#clearAnimal').click(function() {
      contextAnimal.clearRect(0, 0, $animalCanvas[0].width, $animalCanvas[0].height);
      contextAnimal.fillStyle = "white";
      contextAnimal.fillRect(0, 0, $animalCanvas[0].width, $animalCanvas[0].height);
    });
});
