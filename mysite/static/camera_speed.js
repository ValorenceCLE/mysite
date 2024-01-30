// Get references to the camera speed chart elements
const cameraSpeedSlider = document.getElementById('cameraSpeedSlider');
const selectedTimeFrameCamera = document.getElementById('selectedTimeFrameCamera');
const cameraSpeedChart = document.getElementById('cameraSpeedChart').getContext('2d');
let cameraChart; // Variable to store the camera chart instance

// Function to update the displayed time frame and chart data for the camera speed chart
function updateSelectedTimeFrameCamera() {
    // Your update logic here (e.g., read the selected time frame from the slider)
    const selectedTimeFrameValue = cameraSpeedSlider.value;
    selectedTimeFrameCamera.textContent = `Selected Time Frame: ${selectedTimeFrameValue} hour(s)`; // Update the text
    // Load data from the CSV file
    fetch("/static/camera_speed.csv") // Updated file path to the CSV file
        .then(response => response.text())
        .then(csvData => {
            // Parse CSV data into arrays
            const lines = csvData.trim().split('\n');
            const headers = lines[0].split(',');
            const data = lines.slice(1).map(line => line.split(','));

            // Convert timestamps to Date objects
            const timestamps = data.map(row => new Date(row[0]));

            // Calculate the time frame boundary (e.g., last hour, last day)
            const currentTime = new Date();
            const timeFrameBoundary = new Date(currentTime);
            timeFrameBoundary.setHours(currentTime.getHours() - selectedTimeFrameValue);

            // Filter data based on the selected time frame
            const filteredData = data.filter((row, index) => timestamps[index] >= timeFrameBoundary);

            // Extract timestamps, download speeds, and upload speeds for the camera speed chart
            const filteredTimestamps = filteredData.map(row => new Date(row[0]).toLocaleString('en-US', { month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' })); // Format timestamp
            const downloadSpeedsCamera = filteredData.map(row => parseFloat(row[1]));
            const uploadSpeedsCamera = filteredData.map(row => parseFloat(row[2]));

            // Destroy the existing camera chart if it exists
            if (cameraChart) {
                cameraChart.destroy();
            }

            // Create and update the camera speed chart
            cameraChart = new Chart(cameraSpeedChart, {
                type: 'line',
                data: {
                    labels: filteredTimestamps,
                    datasets: [
                        {
                            label: 'Download Speed (Mbps)',
                            data: downloadSpeedsCamera,
                            borderColor: 'blue',
                            borderWidth: 2,
                            fill: false,
                            pointRadius: 1,
                        },
                        {
                            label: 'Upload Speed (Mbps)',
                            data: uploadSpeedsCamera,
                            borderColor: 'green',
                            borderWidth: 2,
                            fill: false,
                            pointRadius: 1,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    responsiveAnimationDuration: 0, // Disable animation on resize
                    plugins: {
                        legend: {
                            display: true,
                            position: 'bottom',
                        }
                    },
                    scales: {
                        x: {
                            display: false,

                        },

                        y: {
                            title: {
                                display: true,
                                text: 'Speed (Mbps)'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Error loading CSV:", error));
}

// Add event listener to the slider for the camera speed chart
cameraSpeedSlider.addEventListener('input', updateSelectedTimeFrameCamera);

// Initialize the camera speed chart with the default data
updateSelectedTimeFrameCamera();

// Function to periodically refresh camera data
function refreshCameraData() {
    fetch("/static/camera_speed.csv")
        .then(response => response.text())
        .then(csvData => {
            // Update the chart with the new data
            updateSelectedTimeFrameCamera();
        });
}

// Set an interval to refresh the camera data every 60 seconds (adjust as needed)
setInterval(refreshCameraData, 60000); // Refresh every 60 seconds (1 minute)
