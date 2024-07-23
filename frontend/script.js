// URL of the API endpoint
const apiEndpoint = 'http://localhost:5000/api';  // Ensure this matches your Flask server's URL

// Signup form submission
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${apiEndpoint}/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    });

    if (response.ok) {
        alert('Signup successful! Redirecting to login page.');
        window.location.href = 'login.html';
    } else {
        const errorData = await response.json();
        alert(`Signup failed: ${errorData.message}`);
    }
});

// Login form submission
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${apiEndpoint}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        alert('Login successful! Redirecting to dashboard.');
        window.location.href = 'dashboard.html'; // Update this to your actual dashboard URL
    } else {
        const errorData = await response.json();
        alert(`Login failed: ${errorData.message}`);
    }
});
