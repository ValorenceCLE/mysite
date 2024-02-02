console.log('relay.js loaded and executed');

document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('button[data-url]');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const url = button.getAttribute('data-url');

      if (url) {
        // Log button click for debugging
        console.log(`Button clicked for URL: ${url}`);

        // Get CSRF token
        const csrfToken = getCookie('csrftoken');
        console.log('CSRF Token:', csrfToken);

        // Send a POST request to the URL with CSRF token
        fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken, // Include the CSRF token
          },
          body: JSON.stringify({ action: button.id }), // Use the button's ID as the action
        })
        .then(response => {
          if (response.ok) {
            console.log(`Successfully sent a command to ${url}`);
          } else {
            console.error(`Failed to send a command to ${url}`);
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
      } else {
        console.error('Button does not have a data-url attribute.');
      }
    });
  });
});

// Function to get the CSRF token from cookies (same as before)
function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}
