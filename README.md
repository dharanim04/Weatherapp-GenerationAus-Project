# Weather App

A simple web application to fetch and display weather information (temperature, wind speed, humidity) for multiple cities using the [Open-Meteo API](https://open-meteo.com/).  
The backend is built with Python Flask, and the frontend is a responsive HTML/JavaScript interface.

---

## Features

- Search weather for one or more cities at once.
- Displays temperature, wind speed, and humidity.
- Maintains and displays the last five search histories.
- Logs all errors to a file (`weather_app_errors.log`).

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd weather-app


2. Install Python Dependencies
Make sure you have Python 3.7+ installed.

pip install Flask requests

Or, using the provided requirements file:

pip install -r requirements.txt


3. Run the Application
python app.py



The app will start on http://localhost:5000.

File Structure
weather-app/
├── app.py
├── requirements.txt
├── weather_app_errors.log
├── static/
│   ├── index.html
│   └── script.js
└── README.md


API Documentation
1. POST /api/weather
Description:
Fetch weather data for one or more cities.

Request Body (JSON):

{
  "cities": ["London", "Paris", "Tokyo"]
}


Response (JSON):

[
  {
    "city": "London",
    "temperature": 15.2,
    "windspeed": 10.5,
    "humidity": 70
  },
  {
    "city": "Paris",
    "temperature": 18.1,
    "windspeed": 8.2,
    "humidity": 65
  }
]


If a city is not found or an error occurs:

{
  "city": "UnknownCity",
  "error": "City not found"
}


2. GET /api/history/last5
Description:
Get the last five search entries (latest first).

Response (JSON):

[
  {
    "cities": ["London", "Paris"],
    "results": [
      {
        "city": "London",
        "temperature": 15.2,
        "windspeed": 10.5,
        "humidity": 70
      },
      {
        "city": "Paris",
        "temperature": 18.1,
        "windspeed": 8.2,
        "humidity": 65
      }
    ]
  },
  ...
]

Future Enhancements
Here are some suggestions for future improvements and features:

User Authentication: Allow users to register and log in, so each user can have a personalized search history.
Persistent Storage: Store search history and logs in a database (e.g., SQLite, PostgreSQL) instead of in-memory and flat files.
Weather Forecasts: Add support for multi-day forecasts, not just current weather.
Geolocation: Automatically detect the user's location and show local weather.
Unit Selection: Allow users to choose between Celsius/Fahrenheit and km/h/mph.
Mobile App: Develop a mobile version using React Native or Flutter.
Notifications: Enable weather alerts or notifications for favorite cities.
Internationalization: Support multiple languages for a global audience.
Improved Error Handling: Provide more user-friendly error messages and retry options.
API Rate Limiting: Implement rate limiting to prevent abuse of the backend API.
Dark Mode: Add a dark mode toggle for better accessibility.
Deployment: Provide Docker support and deployment instructions for cloud platforms.

Logging
All errors and failures are logged to weather_app_errors.log in the project root.
Check this file for troubleshooting and debugging.
Usage
Open http://localhost:5000 in your browser.
Enter one or more city names, separated by commas (e.g., London, Paris, Tokyo).
Click "Get Weather" to view the results.
The last five searches will be displayed in a grid below the search form.


## Customization
Frontend: Edit static/index.html and static/script.js for UI changes.
Backend: Edit app.py for API or logic changes.
Logging: Adjust logging settings in app.py as needed.
License
MIT License (add your license here if needed).

Credits
Open-Meteo API
Flask, Requests
