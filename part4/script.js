/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesList = document.getElementById('places-list');

    // Only run this code if the login form actually exists on the current page
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); 
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Call our login function with those credentials
            await loginUser(email, password);
        });
    }


if (placesList) {
        checkAuthentication(); // 1. Kick out unauthenticated users
        fetchPlaces();         // 2. Fetch the real places
    }
});

// Helper function to read the cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// 1. The Bouncer
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html'; // Kick them to login
    }
}

// 2. Fetch the real data
async function fetchPlaces() {
    const token = getCookie('token');
    try {
        // MAKE SURE THIS URL MATCHES YOUR FLASK PLACES ENDPOINT
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // Show the wristband!
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places');
            if (response.status === 401) {
                window.location.href = 'login.html'; // Token expired/invalid
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// 3. Draw the HTML dynamically
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Wipe out the hardcoded HTML

    places.forEach(place => {
        const placeCard = document.createElement('article');
        placeCard.className = 'place-card';
        
        // Notice the href! We pass the ID in the URL so the next page knows what to load
        placeCard.innerHTML = `
            <h3>${place.title}</h3>
            <p>Price: ${place.price} Credits/Night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        
        placesList.appendChild(placeCard);
    });
}

async function loginUser(email, password) {
    try {
        // MAKE SURE THIS URL MATCHES YOUR FLASK API EXACTLY
        // It might be /login or /api/v1/login depending on your backend routes
        const apiUrl = 'http://127.0.0.1:5000/api/v1/auth/login'; 

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Convert the JavaScript object into a JSON string for the backend
            body: JSON.stringify({ email: email, password: password })
        });

        if (response.ok) {
            // If the backend returns a 200 OK, parse the JSON response
            const data = await response.json();
            
            // Store the JWT token securely in a browser cookie
            // 'path=/' ensures the cookie is accessible from all pages of your site
            document.cookie = `token=${data.access_token}; path=/`;
            
            // Redirect the user to the Hero Hangouts main page
            window.location.href = 'index.html';
        } else {
            // If the backend returns a 401 Unauthorized, alert the user
            const errorData = await response.json();
            alert('Login failed: ' + (errorData.message || response.statusText));
        }
    } catch (error) {
        // This catches network errors (like if your Flask server isn't running)
        console.error('Error during login:', error);
        alert('Could not connect to the API. Make sure your Flask server is running and CORS is enabled!');
    }
}