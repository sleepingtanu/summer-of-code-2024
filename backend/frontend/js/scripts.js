
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const productForm = document.getElementById('productForm');
    const productContainer = document.getElementById('productContainer');
    
    if (signupForm) {
        signupForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const username = document.getElementById('signupUsername').value;
            const email = document.getElementById('signupEmail').value;
            const password = document.getElementById('signupPassword').value;
            
            try {
                const response = await fetch('http://localhost:5000/api/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, email, password })
                });
                const result = await response.json();
                console.log('Signup Response:', result);
                if (response.ok) {
                    alert('Signup successful! Redirecting to login...');
                    window.location.href = '/login.html';
                } else {
                    alert(result.error);
                }
            } catch (error) {
                console.error('Error during signup:', error);
                alert('Error during signup');
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            try {
                const response = await fetch('http://localhost:5000/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                const result = await response.json();
                console.log('Login Response:', result);
                if (response.ok) {
                    alert('Login successful!');
                    localStorage.setItem('token', result.token);
                    window.location.href = '/dashboard.html';  // Redirect to your dashboard
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('Error during login');
            }
        });
    }

    if (productForm) {
        productForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const name = document.getElementById('productName').value;
            const description = document.getElementById('productDescription').value;
            const quantity = document.getElementById('productQuantity').value;
            const price = document.getElementById('productPrice').value;
            console.log('Product Creation Attempt:', { name, description, quantity, price });

            try {
                const response = await fetch('http://localhost:5000/api/products', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, description, quantity, price })
                });
                const result = await response.json();
                console.log('Product Creation Response:', result);
                if (response.ok) {
                    alert('Product created successfully!');
                    // Optionally, you could reset the form or update the product list
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error during product creation:', error);
                alert('Error during product creation');
            }
        });
    }

    const loadProducts = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/products', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            const products = await response.json();
            console.log('Loaded Products:', products);
            if (response.ok) {
                productContainer.innerHTML = '';
                products.forEach(product => {
                    const productElement = document.createElement('div');
                    productElement.className = 'product';
                    productElement.innerHTML = `
                        <h3>${product.name}</h3>
                        <p>${product.description}</p>
                        <p>Quantity: ${product.quantity}</p>
                        <p>Price: $${product.price}</p>
                    `;
                    productContainer.appendChild(productElement);
                });
            } else {
                alert('Failed to load products');
            }
        } catch (error) {
            console.error('Error during product loading:', error);
            alert('Error during product loading');
        }
    };

    if (productContainer) {
        loadProducts();
    }
});
