function fetchAndUpdateUptime(button) {
    const url = button.getAttribute('data-url');

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Format the uptime data
            const formattedUptime = formatUptime(data.output);

            // Get the elements by their IDs
            const uptimePlaceholder = document.getElementById(`${button.id}-placeholder`);

            if (uptimePlaceholder) {
                uptimePlaceholder.textContent = `${formattedUptime}`;
            }
        })
        .catch(error => {
            console.error(`Error fetching uptime data: ${error}`);
            const uptimePlaceholder = document.getElementById(`${button.id}-placeholder`);

            if (uptimePlaceholder) {
                uptimePlaceholder.textContent = `Router Uptime: (N/A)`;
            }
        });
}

// Function to format uptime data as "X days, Y hours, Z minutes, A seconds"
function formatUptime(rawUptimeData) {
    const { days, hours, minutes, seconds } = rawUptimeData;

    let formattedUptime = '';

    if (days > 0) {
        formattedUptime += `${days} day${days > 1 ? 's' : ''}, `;
    }

    if (hours > 0) {
        formattedUptime += `${hours} hour${hours > 1 ? 's' : ''}, `;
    }

    if (minutes > 0) {
        formattedUptime += `${minutes} minute${minutes > 1 ? 's' : ''}, `;
    }

    formattedUptime += `${Math.round(seconds)} second${Math.round(seconds) > 1 ? 's' : ''}`;

    return formattedUptime;
}

// Add event listener for the "Refresh" buttons using event delegation
document.body.addEventListener('click', function (event) {
    const button = event.target.closest('button[data-url]');
    if (button) {
        fetchAndUpdateUptime(button);
    }
});
