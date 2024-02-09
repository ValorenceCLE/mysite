// Check if WebSocket is supported by the browser
if ("WebSocket" in window) {
  // Open a WebSocket connection to the Django server
  var ws = new WebSocket('ws://' + window.location.host + '/ws/sensor/data/');

  ws.onopen = function() {
    // WebSocket connection is open, you can send messages if needed
    console.log("WebSocket connection to sensor data is open.");
  };

  ws.onmessage = function(e) {
    // Message received from the server
    var data = JSON.parse(e.data);

    // Check if temperature data is present and update the CurrentTemp element
    if (data.temperature !== undefined) {
      document.getElementById('CurrentTemp').innerText = data.temperature + '°F';
    }

    // Check if voltage data is present and update the CurrentVolts element
    if (data.voltage_V !== undefined) {
      document.getElementById('CurrentVolts').innerText = data.voltage_V + 'V';
    }
  };

  ws.onclose = function() {
    // WebSocket connection is closed
    console.log("WebSocket connection to sensor data is closed.");
  };

  ws.onerror = function(error) {
    // WebSocket error
    console.log("WebSocket error: " + error);
  };
} else {
  // The browser doesn't support WebSocket
  alert("WebSocket NOT supported by your Browser!");
}
