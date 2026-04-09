/* Hero Hangouts - Frontend JavaScript */
// Map the place titles directly to your local images
const PLACE_IMAGES = {
    "The Batcave": "images/The_Batcave.webp",
    "Fortress of Solitude": "images/Fortress_of_Solitude.webp",
    "The Watchtower": "images/Watchtower_-_Annexes.webp",
    "Joker's Funhouse": "images/joker_base.jpg"
};

document.addEventListener('DOMContentLoaded', () => {
    const loginForm    = document.getElementById('login-form');
    const placesList   = document.getElementById('places-list');
    const placeDetails = document.getElementById('place-details');
    const reviewForm   = document.getElementById('review-form');

    // LOGIN PAGE
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email    = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // INDEX PAGE
    if (placesList) {
        checkAuthentication();

        document.getElementById('price-filter').addEventListener('change', (event) => {
            const selected = event.target.value;
            const cards    = document.querySelectorAll('.place-card');
            cards.forEach(card => {
                if (selected === 'all') {
                    card.style.display = 'block';
                } else {
                    const price = parseFloat(card.dataset.price);
                    card.style.display = price <= parseFloat(selected) ? 'block' : 'none';
                }
            });
        });
    }

    // PLACE DETAILS PAGE
    if (placeDetails) {
        checkAuthentication();

        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const token      = getCookie('token');
                const placeId    = getPlaceIdFromURL();
                const reviewText = document.getElementById('review').value;
                const rating     = document.getElementById('rating').value;
                await submitReview(token, placeId, reviewText, rating);
            });
        }
    }

    // ADD REVIEW PAGE (standalone add_review.html)
    if (reviewForm && !placeDetails) {
        const token   = getCookie('token');
        const placeId = getPlaceIdFromURL();

        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review').value;
            const rating     = document.getElementById('rating').value;
            await submitReview(token, placeId, reviewText, rating);
        });
    }

    const logoutLink   = document.getElementById('logout-link');

    // LOGOUT LOGIC
    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            // Destroy the cookie by setting its expiration date to the past
            document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            // Send them back to the homepage to refresh the state
            window.location.href = 'index.html';
        });
    }
});

// ==========================================
// AUTHENTICATION
// ==========================================

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token            = getCookie('token');
    const loginLink        = document.getElementById('login-link');
    const logoutLink       = document.getElementById('logout-link');
    const addReviewSection = document.getElementById('add-review');

    if (loginLink && logoutLink) {
        if (!token) {
            loginLink.style.display = 'block';
            logoutLink.style.display = 'none';
        } else {
            loginLink.style.display = 'none';
            logoutLink.style.display = 'block';
            
            // Only fetch places if we are on the index page
            if (document.getElementById('places-list')) {
                fetchPlaces(token);
            }
        }
    }
    // INDEX: show/hide login link
    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }

    // PLACE: show/hide review form, always fetch details
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
        fetchPlaceDetails(token, getPlaceIdFromURL());
    }
}

// ==========================================
// UTILITIES
// ==========================================

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// ==========================================
// LOGIN
// ==========================================

async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            alert('Login failed: ' + response.statusText);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Could not connect to the API. Make sure your Flask server is running!');
    }
}

// ==========================================
// INDEX — PLACES LIST
// ==========================================

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.status);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const card       = document.createElement('article');
        card.className   = 'place-card';
        
        // Defensive fallback: If the API forgets the price, default to 0 or '???'
        const price = place.price !== undefined ? place.price : '???';
        card.dataset.price = price;

        // Grab the image from our dictionary, or use the logo as a backup
        const imageUrl = PLACE_IMAGES[place.title] || "images/logo.png";

        // Added the image tag and wrapped the text in a 'card-content' div for styling
        card.innerHTML = `
            <img src="${imageUrl}" alt="${place.title}" class="place-image">
            <div class="card-content">
                <h3>${place.title}</h3>
                <p>Price: ${price} Credits/Night</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        `;

        placesList.appendChild(card);
    });
}

// ==========================================
// PLACE DETAILS
// ==========================================

async function fetchPlaceDetails(token, placeId) {
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    try {
        const headers = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            alert('Place not found!');
            window.location.href = 'index.html';
        }
    } catch (error) {
        console.error('Error fetching place:', error);
    }
}

function displayPlaceDetails(place) {
    const section  = document.getElementById('place-details');
    section.innerHTML = '';

    const price = place.price !== undefined ? place.price : '???';
    
    // THE FIX: Check if place.owner exists, and if it does, combine the first and last name!
    let host = 'Classified Identity';
    if (place.owner && place.owner.first_name) {
        host = `${place.owner.first_name} ${place.owner.last_name}`;
    } else if (place.owner_id) {
        host = place.owner_id; // Fallback just in case
    }

    const imageUrl = PLACE_IMAGES[place.title] || "images/logo.png";

    // Main info block with image injected
    const info = document.createElement('div');
    info.className = 'place-info';
    info.innerHTML = `
        <img src="${imageUrl}" alt="${place.title}" class="place-detail-image">
        <div class="detail-text">
            <h1>${place.title}</h1>
            <p><strong>Host:</strong> ${host}</p>
            <p><strong>Price:</strong> ${price} Credits/Night</p>
            <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
        </div>
    `;
    section.appendChild(info);

    // Amenities (Keep this exactly the same)
    if (place.amenities && place.amenities.length > 0) {
        const h3 = document.createElement('h3');
        h3.textContent = 'Amenities';
        section.appendChild(h3);

        const ul = document.createElement('ul');
        ul.className = 'amenities-list';
        
        place.amenities.forEach(amenity => {
            const li = document.createElement('li');
            
            // 1. Convert the name to lowercase so it's easy to check
            const lowerName = amenity.name.toLowerCase();
            let iconHtml = '';

            // 2. Check for keywords and pick the right image path
            if (lowerName.includes('wifi')) {
                iconHtml = `<img src="images/icon_wifi.png" alt="WiFi" class="amenity-icon">`;
            } else if (lowerName.includes('bed') || lowerName.includes('pod')) {
                iconHtml = `<img src="images/icon_bed.png" alt="Bed" class="amenity-icon">`;
            } else if (lowerName.includes('bath') || lowerName.includes('shower')) {
                iconHtml = `<img src="images/icon_bath.png" alt="Bath" class="amenity-icon">`;
            }

            // 3. Inject the icon (if found) right next to the amenity text
            li.innerHTML = `${iconHtml} ${amenity.name}`;
            
            ul.appendChild(li);
        });
        
        section.appendChild(ul);
    }

    // Reviews (Keep this exactly the same)
    const reviewsSection      = document.getElementById('reviews-list');
    reviewsSection.innerHTML  = '<h2>Reviews from the League</h2>';

    if (place.reviews && place.reviews.length > 0) {
place.reviews.forEach(review => {
            const card       = document.createElement('article');
            card.className   = 'review-card';
            
            // Generate the HTML for the icons based on the rating number
            let ratingIconsHtml = '';
            for (let i = 0; i < review.rating; i++) {
                // Change 'favicon.svg' if you decided to use the .png instead!
                ratingIconsHtml += `<img src="images/favicon.svg" alt="Rating Icon" class="rating-icon">`;
            }

            card.innerHTML   = `
                <p><strong>${review.user_name || 'Anonymous'}:</strong> ${review.text}</p>
                <div class="review-rating">${ratingIconsHtml}</div>
            `;
            reviewsSection.appendChild(card);
        });
    } else {
        const empty       = document.createElement('p');
        empty.textContent = 'No reviews yet. Be the first!';
        reviewsSection.appendChild(empty);
    }
}

// ==========================================
// SUBMIT REVIEW
// ==========================================

async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text:     reviewText,
                rating:   parseInt(rating)
            })
        });

        handleResponse(response);
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Could not connect to the API.');
    }
}

function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        document.getElementById('review-form').reset();
    } else {
        alert('Failed to submit review');
    }
}