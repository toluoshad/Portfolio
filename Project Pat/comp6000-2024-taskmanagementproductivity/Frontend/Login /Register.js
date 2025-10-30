document.addEventListener('DOMContentLoaded', function () {
  const wrapper = document.querySelector('.wrapper');
  const loginForm = document.getElementById('login-form');
  const registerLink = document.querySelector('.register-link a');

  // Create the registration form
  const registerForm = document.createElement('form');
  registerForm.setAttribute('id', 'register-form');
  registerForm.setAttribute('action', 'http://127.0.0.1:8000/api/register/');
  registerForm.setAttribute('method', 'POST');
  registerForm.innerHTML = `
      <h1>Register</h1>
      <div class="input-box">
        <input type="text" id="first-name" name="firstName" placeholder="First Name" required>
        <i class='bx bxs-user'></i>
      </div>
      <div class="input-box">
         <input type="text" id="last-name" name="lastName" placeholder="Last Name" required>
         <i class='bx bxs-user'></i>
      </div>
      <div class="input-box">
          <input type="email" id="email" name="email" placeholder="Email" required>
          <i class='bx bxs-envelope'></i>
      </div>
      <div class="input-box">
          <input type="text" id="register-username" name="username" placeholder="Username" required>
          <i class='bx bxs-user-circle'></i>
      </div>
      <div class="input-box">
          <input type="password" id="register-password" name="password" placeholder="Password" required>
          <i class='bx bxs-lock-alt'></i>
      </div>
      <button type="submit" class="btn">Register</button>
      <div class="register-link">
          <p>Already have an account? <a href="#" id="show-login-register">Login</a></p>
      </div>
  `;
  registerForm.style.display = 'none';
  wrapper.appendChild(registerForm);

  // Register link event to show the registration form
  registerLink.addEventListener('click', function (event) {
      event.preventDefault();
      loginForm.style.display = 'none';
      registerForm.style.display = 'block';
  });

  // Check if the URL has a query parameter indicating "Sign Up"
  const urlParams = new URLSearchParams(window.location.search);
  const signUpParam = urlParams.get('signup');

  if (signUpParam === 'true') {
      loginForm.style.display = 'none';
      registerForm.style.display = 'block';
  }

  // Handle Registration Submission
  registerForm.addEventListener('submit', async function (event) {
    event.preventDefault(); 

      const data = {
          firstName: document.getElementById('first-name').value.trim(),
          lastName: document.getElementById('last-name').value.trim(),
          email: document.getElementById('email').value.trim(),
          username: document.getElementById('register-username').value.trim(),
          password: document.getElementById('register-password').value.trim(),
      };

      try {
        const response = await fetch('http://127.0.0.1:8000/api/register/', {
            method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
          });

          const result = await response.json();

          if (response.ok) {
              alert(result.message);
              alert("Registration successful!");  // ✅ Show success message
            window.location.reload();  // ✅ Reload page or redirect to login
          } else {
            alert(result.error || "Registration failed. Please try again.");
          }
      } catch (error) {
          console.error('Error:', error);
          alert('An error occurred. Please try again.');

      }
  });
});
