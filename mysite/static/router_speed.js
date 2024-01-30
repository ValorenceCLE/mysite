// Get references to the router speed chart elements
const routerSpeedSlider = document.getElementById('routerSpeedSlider');
const selectedTimeFrame = document.getElementById('selectedTimeFrame');
const routerSpeedChart = document.getElementById('routerSpeedChart').getContext('2d');
let routerChart; // Variable to store the router chart instance

// Function to update the displayed time frame and chart data for the router speed chart
function updateSelectedTimeFrame() {
    // Read the selected time frame from the slider
    const selectedTimeFrameValue = routerSpeedSlider.value;

    // Update the displayed time frame
    selectedTimeFrameRouter.textContent = `Selected Time Frame: ${selectedTimeFrameValue} hour(s)`; // Update the text

    // Load data from the CSV file
    fetch("/static/router_speed.csv") // Updated file path to the CSV file
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

            // Extract timestamps, download speeds, and upload speeds for the router speed chart
            const filteredTimestamps = filteredData.map(row => new Date(row[0]).toLocaleString('en-US', { month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' })); // Format timestamp
            const downloadSpeeds = filteredData.map(row => parseFloat(row[1]));
            const uploadSpeeds = filteredData.map(row => parseFloat(row[2]));

            // Destroy the existing router chart if it exists
            if (routerChart) {
                routerChart.destroy();
            }

            // Create and update the router speed chart
            routerChart = new Chart(routerSpeedChart, {
                type: 'line',
                data: {
                    labels: filteredTimestamps,
                    datasets: [
                        {
                            label: 'Download Speed (Mbps)',
                            data: downloadSpeeds,
                            borderColor: 'blue',
                            borderWidth: 2,
                            fill: false,
                            pointRadius: 1,
                        },
                        {
                            label: 'Upload Speed (Mbps)',
                            data: uploadSpeeds,
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
                            display: false, // Hide the x axis
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

// Add event listener to the slider for the router speed chart
routerSpeedSlider.addEventListener('input', updateSelectedTimeFrame);

// Initialize the router speed chart with the default data
updateSelectedTimeFrame();

// Function to periodically refresh router data
function refreshRouterData() {
    fetch("/static/router_speed.csv")
        .then(response => response.text())
        .then(csvData => {
            // Update the chart with the new data
            updateSelectedTimeFrame();
        });
}

// Set an interval to refresh the router data every 60 seconds (adjust as needed)
setInterval(refreshRouterData, 60000); // Refresh every 60 seconds (1 minute)
