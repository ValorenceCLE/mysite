document.addEventListener('DOMContentLoaded', () => {
    const wsGPIO = new WebSocket(`ws://${window.location.host}/ws/gpio/status/`);
    const wsSensor = new WebSocket(`ws://${window.location.host}/ws/sensor/data/`);

    function updateStatus(data) {
        if (data.camera !== undefined) {
            document.getElementById('CameraStatus').textContent = data.camera ? 'On' : 'Off';
        }
        if (data.fan !== undefined) {
            document.getElementById('FanStatus').textContent = data.fan ? 'On' : 'Off';
        }
        if (data.strobe !== undefined) {
            document.getElementById('StrobeStatus').textContent = data.strobe ? 'On' : 'Off';
        }
        if (data.router !== undefined) {
            document.getElementById('RouterStatus').textContent = data.router ? 'On' : 'Restarting';
        }
    }

    wsGPIO.onopen = function() {
        console.log('WebSocket connection for GPIO status established');
        wsGPIO.send(JSON.stringify({ action: 'get_status' }));
    };

    wsGPIO.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateStatus(data);
    };

    wsGPIO.onerror = function(error) {
        console.error('WebSocket error (GPIO status):', error);
    };

    wsGPIO.onclose = function(e) {
        console.log('WebSocket connection for GPIO status closed:', e.reason);
    };

    wsSensor.onopen = function() {
        console.log('WebSocket connection for sensor data established');
    };

    wsSensor.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.temperature !== undefined && data.temperature > 100) {
            document.getElementById('FanStatus').textContent = 'On'; // Visual feedback for fan status
            wsGPIO.send(JSON.stringify({ action: 'FanOn' }));
        }
    };

    wsSensor.onerror = function(error) {
        console.error('WebSocket error (sensor data):', error);
    };

    wsSensor.onclose = function(e) {
        console.log('WebSocket connection for sensor data closed:', e.reason);
    };

   const buttons = document.querySelectorAll('button[data-url]');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.id;
            wsGPIO.send(JSON.stringify({ action: action }));

            // Immediate UI update for router reset button
            if (action === 'RouterReset') {
                document.getElementById('RouterStatus').textContent = 'Restarting';
                alert("Are you sure you want to restart the router?")
            }
        });
    });
});
