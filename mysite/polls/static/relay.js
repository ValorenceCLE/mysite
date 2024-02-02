document.addEventListener('DOMContentLoaded', () => {
    // Establish WebSocket connection
    const ws = new WebSocket(`ws://${window.location.host}/ws/gpio/status/`);

    ws.onopen = function() {
        console.log('WebSocket connection established');
        // Request the initial status of GPIOs upon WebSocket connection
        ws.send(JSON.stringify({ action: 'get_status' }));
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        // Update GPIO statuses based on messages received from the server
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
            document.getElementById('RouterStatus').textContent = data.router ? 'On' : 'Off';
        }

        // Check if the "run for 5 minutes" buttons were pressed
        if (data.fan_5min) {
            // Fan should run for 5 minutes, update status to 'Running'
            document.getElementById('Fan5MinStatus').textContent = 'Running';

            // After 5 minutes, set the status back to 'Off'
            setTimeout(() => {
                document.getElementById('Fan5MinStatus').textContent = 'Off';
                // Send the action to stop the fan after 5 minutes
                ws.send(JSON.stringify({ action: 'FanOff' }));
            }, 300000); // 300000 milliseconds = 5 minutes
        }
        if (data.strobe_5min) {
            // Strobe should run for 5 minutes, update status to 'Running'
            document.getElementById('Strobe5MinStatus').textContent = 'Running';

            // After 5 minutes, set the status back to 'Off'
            setTimeout(() => {
                document.getElementById('Strobe5MinStatus').textContent = 'Off';
                // Send the action to stop the strobe after 5 minutes
                ws.send(JSON.stringify({ action: 'StrobeOff' }));
            }, 300000); // 300000 milliseconds = 5 minutes
        }
    };

    ws.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    ws.onclose = function(e) {
        console.log('WebSocket connection closed:', e.reason);
    };

    // Send action messages to the WebSocket based on button clicks
    const buttons = document.querySelectorAll('button[data-url]');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.id; // Use button ID as the action identifier
            console.log(`Button clicked: ${action}`); // Log the action

            if (action === 'RouterReset') {
                // Router Reset button logic
                ws.send(JSON.stringify({ action: action }));

                // Immediately update the RouterStatus to 'Resetting' on button click
                document.getElementById('RouterStatus').textContent = 'Resetting';

                // After 10 seconds, set the RouterStatus back to 'On'
                setTimeout(() => {
                    document.getElementById('RouterStatus').textContent = 'On';
                }, 10000);
            } else {
                // For other buttons, send the action to the WebSocket
                ws.send(JSON.stringify({ action: action }));
            }
        });
    });
});
