// Function to handle fan on button click
document.getElementById('fan_on').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get the CSRF token from the form
    fetch('/fan_on/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken, // Include the CSRF token in the request headers
        },
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response, update UI, show a message, etc.
        console.log(data.message);
        document.getElementById('fan_status').textContent = 'Fan is ON';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to handle fan off button click
document.getElementById('fan_off').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get the CSRF token from the form
    fetch('/fan_off/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken, // Include the CSRF token in the request headers
        },
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response, update UI, show a message, etc.
        console.log(data.message);
        document.getElementById('fan_status').textContent = 'Fan is OFF';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to handle fan run for 5 minutes button click
document.getElementById('fan_5min').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get the CSRF token from the form
    fetch('/fan_run_for_5_minutes/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken, // Include the CSRF token in the request headers
        },
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response, show a message, etc.
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
