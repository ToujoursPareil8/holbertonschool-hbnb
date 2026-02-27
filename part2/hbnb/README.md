# HBnB Project - REST API & Facade Pattern

## Overview
This project is the backend RESTful API for **HBnB**, an application inspired by Airbnb. It is built using **Python 3**, **Flask**, and **Flask-RESTx**. 

The core focus of this phase of the project is to implement a **Layered Architecture** utilizing the **Facade Design Pattern** and an **In-Memory Repository** for data persistence. This ensures a clean separation of concerns between the Presentation Layer (API endpoints), the Business Logic Layer (Facade), and the Data Access Layer (Repository).

## Architecture
The application is structured into three main layers:
1. **Presentation Layer (`app/api/`)**: Defines the Flask-RESTx Namespaces and Resources. Handles incoming HTTP requests, validates input payloads, and returns JSON responses.
2. **Business Logic Layer (`app/services/facade.py`)**: The `HBnBFacade` acts as the single entry point for the API to interact with the underlying data. It handles all business rules, validations, and object instantiation.
3. **Persistence Layer (`app/persistence/`)**: Currently uses an `InMemoryRepository` to store Python objects (`User`, `Place`, `Review`, `Amenity`) in memory (dictionaries) during the application lifecycle.

## Project Structure
```text
hbnb/
├── app/
│   ├── __init__.py           # App factory & Blueprint registration
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py   # Flask-RESTx API and Namespaces setup
│   │       ├── users.py      # User endpoints
│   │       ├── places.py     # Place endpoints
│   │       └── reviews.py    # Review endpoints
│   ├── models/
│   │   ├── base_model.py     # Base class with UUID and timestamps
│   │   ├── user.py           # User entity
│   │   ├── place.py          # Place entity
│   │   └── review.py         # Review entity
│   └── services/
│       └── facade.py         # HBnBFacade pattern implementation
├── tests/
│   ├── test_users.py         # Unit tests for User endpoints
│   ├── test_places.py        # Unit tests for Place endpoints
│   └── test_reviews.py       # Unit tests for Review endpoints
├── run.py                    # Main entry point to start the server
└── README.md

## API Endpoints
The API is versioned at `/api/v1/` and provides the following operations:

### Users
* `POST /api/v1/users/` - Create a new user.
* `GET /api/v1/users/` - Retrieve all users.
* `GET /api/v1/users/<user_id>` - Retrieve specific user details.
* `PUT /api/v1/users/<user_id>` - Update user information.

### Places
* `POST /api/v1/places/` - Register a new place (requires a valid `owner_id`).
* `GET /api/v1/places/` - Retrieve all places.
* `GET /api/v1/places/<place_id>` - Retrieve specific place details (includes Owner and Reviews).
* `PUT /api/v1/places/<place_id>` - Update place information.
* `GET /api/v1/places/<place_id>/reviews` - Retrieve all reviews for a specific place.

### Reviews
* `POST /api/v1/reviews/` - Create a new review (requires valid `user_id` and `place_id`).
* `GET /api/v1/reviews/` - Retrieve all reviews.
* `GET /api/v1/reviews/<review_id>` - Retrieve specific review details.
* `PUT /api/v1/reviews/<review_id>` - Update review text and rating.
* `DELETE /api/v1/reviews/<review_id>` - Delete a review.

## Installation & Setup
1. Clone the repository to your local machine.
2. Ensure you have Python 3.8+ installed.
3. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install the required dependencies:

```bash
pip install flask flask-restx

## Running the Server

To start the Flask development server, run the following command from the root directory:
Bash

python run.py

Once the server is running, you can access the Swagger UI interactive documentation at: http://127.0.0.1:5000/api/v1/

## Running the Test Suite

The project includes a comprehensive suite of automated unit tests using Python's built-in unittest framework.

To run the entire test suite with verbose output:
Bash

python -m unittest discover tests -v

To run a specific test file (e.g., reviews):
Bash

python -m unittest tests/test_reviews.py -v

## Authors

Jason JL, Farid G