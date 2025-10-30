document.addEventListener('DOMContentLoaded', function () {
    console.log("Login.js loaded successfully!");

    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('login-username');
    const passwordInput = document.getElementById('login-password');

    if (!loginForm || !usernameInput || !passwordInput) {
        console.error("Error: Form or input fields not found!");
        return;
    }

    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        console.log("Form submission prevented");

        const data = {
            username: usernameInput.value.trim(),
            password: passwordInput.value.trim(),
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/api/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
        
            console.log("Raw Response Status:", response.status);
            const responseText = await response.text();
            console.log("Raw Response Body:", responseText);
        
            let result;
            try {
                result = JSON.parse(responseText);  // Ensure it's parsed as JSON
            } catch (e) {
                console.error("Non-JSON response received:", responseText);
                showErrorMessage("Unexpected server response. Please try again.");
                return;
            }
        
            console.log("Parsed JSON:", result);
        
            if (response.ok) {
                console.log("Login successful, redirecting...");
        
                // Store tokens
                localStorage.setItem("access_token", result.access);
                localStorage.setItem("refresh_token", result.refresh);
        
                // Store success message flag
                sessionStorage.setItem("showSuccess", "true");
        
                // Redirect instantly
                window.location.href = "../Dashboard.html";
            } else {
                console.warn("Login failed. Status:", response.status);
        
                // Display the exact error message from API
                if (result.error) {
                    showErrorMessage(result.error);
                } else {
                    showErrorMessage("Oops! Something went wrong. Please try again.");
                }
            }
        } catch (error) {
            console.error("Network or Server Error:", error);
            showErrorMessage("Cannot connect to the server. Please check your internet connection.");
        }
        
    });
});

/**
 * Displays an error message with fade-in and fade-out effects.
 */
function showErrorMessage(errorText) {
    const errorMessage = document.getElementById("error-message");
    const errorTextElement = document.getElementById("error-text");

    // Set error message text
    errorTextElement.textContent = errorText;

    // Show error message with fade-in
    errorMessage.style.display = "flex";
    setTimeout(() => {
        errorMessage.classList.add("show"); // Apply fade-in
    }, 10); // Slight delay to allow CSS transition

    // Fade out after 3 seconds
    setTimeout(() => {
        errorMessage.classList.remove("show"); // Start fade-out
        errorMessage.classList.add("fade-out");

        // Fully hide the message after fade-out
        setTimeout(() => {
            errorMessage.style.display = "none";
            errorMessage.classList.remove("fade-out"); // Reset for next use
        }, 500); // Adjust to match CSS fade-out duration
    }, 3000);
}
//Show password
document.addEventListener("DOMContentLoaded", function () {
    console.log("Login.js loaded successfully!");

    const passwordInput = document.getElementById("login-password");
    const togglePassword = document.getElementById("toggle-password");

    if (passwordInput && togglePassword) {
        togglePassword.addEventListener("click", function () {
            // Toggle password visibility
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                togglePassword.classList.replace("bx-show", "bx-hide"); // Change icon
            } else {
                passwordInput.type = "password";
                togglePassword.classList.replace("bx-hide", "bx-show"); // Change icon back
            }
        });
    }
});



