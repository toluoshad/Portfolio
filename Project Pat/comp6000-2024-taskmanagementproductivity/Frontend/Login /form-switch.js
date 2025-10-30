document.addEventListener('DOMContentLoaded', function () {
    // Select elements
    const loginForm = document.getElementById('login-form');
    const forgotPasswordForm = document.getElementById('forgot-password-form');
    const registerForm = document.getElementById('register-form');

    const showForgotPasswordLink = document.getElementById('show-forgot-password');
    const showRegisterLink = document.getElementById('show-register');
    const showLoginFromRegisterLink = document.getElementById('show-login-register');
    const showLoginFromForgotPasswordLink = document.getElementById('show-login');

    // Switch to Forgot Password Form
    showForgotPasswordLink.addEventListener('click', function (event) {
        event.preventDefault();
        loginForm.style.display = 'none';
        forgotPasswordForm.style.display = 'block';
        registerForm.style.display = 'none';
    });

    // Switch to Register Form
    showRegisterLink.addEventListener('click', function (event) {
        event.preventDefault();
        loginForm.style.display = 'none';
        forgotPasswordForm.style.display = 'none';
        registerForm.style.display = 'block';
    });

    // Switch to Login Form from Register Form
    showLoginFromRegisterLink.addEventListener('click', function (event) {
        event.preventDefault();
        loginForm.style.display = 'block';
        forgotPasswordForm.style.display = 'none';
        registerForm.style.display = 'none';
    });

    // Switch back to Login Form from Forgot Password
    showLoginFromForgotPasswordLink.addEventListener('click', function (event) {
        event.preventDefault();
        loginForm.style.display = 'block';
        forgotPasswordForm.style.display = 'none';
        registerForm.style.display = 'none';
    });
});
