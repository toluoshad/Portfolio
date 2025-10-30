document.addEventListener('DOMContentLoaded', function () {
    // Select elements
    const loginForm = document.getElementById('login-form');
    const forgotPasswordForm = document.getElementById('forgot-password-form');
    const showForgotPasswordLink = document.getElementById('show-forgot-password');
    const showLoginLink = document.getElementById('show-login');

    // Switch to Forgot Password Form
    showForgotPasswordLink.addEventListener('click', function (event) {
        event.preventDefault();
        loginForm.style.display = 'none';
        forgotPasswordForm.style.display = 'block';
    });

    // Switch back to Login Form from Forgot Password
    showLoginLink.addEventListener('click', function (event) {
        event.preventDefault();
        forgotPasswordForm.style.display = 'none';
        loginForm.style.display = 'block';
    });

    // Handle Forgot Password Form Submission
    forgotPasswordForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent form default submission

        // Get the entered username
        const username = document.getElementById('forgot-username').value.trim();

        try {
            // Send the username to the backend
            const response = await fetch('http://localhost:3000/forgot-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username }),
            });

            const result = await response.json();

            // Create a message element to display feedback
            const messageEl = document.createElement('p');
            messageEl.style.textAlign = 'center';
            messageEl.style.marginTop = '20px';

            if (response.ok) {
                messageEl.textContent = result.message;
                messageEl.style.color = 'green';
            } else {
                messageEl.textContent = result.error;
                messageEl.style.color = 'red';
            }

            // Append the message to the form
            forgotPasswordForm.appendChild(messageEl);
        } catch (error) {
            console.error('Error:', error);

            const messageEl = document.createElement('p');
            messageEl.textContent = 'An error occurred. Please try again.';
            messageEl.style.textAlign = 'center';
            messageEl.style.marginTop = '20px';
            messageEl.style.color = 'red';
            forgotPasswordForm.appendChild(messageEl);
        }
    });
});
