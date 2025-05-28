from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import logging

app = Flask(__name__, static_folder='static')

# Set up logging
LOG_FILE = "weather_app_errors.log"
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# In-memory search history (list of dicts)
search_history = []

def get_coordinates(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    try:
        resp = requests.get(geo_url)
        data = resp.json()
        if data.get("results"):
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
            return lat, lon
        else:
            raise ValueError("City not found")
    except Exception as e:
        logging.error(f"Failed to get coordinates for city '{city}': {e}")
        raise

def get_weather_for_city(city):
    try:
        lat, lon = get_coordinates(city)
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        )
        resp = requests.get(weather_url)
        data = resp.json()
        if "current_weather" in data:
            humidity = None
            if "hourly" in data and "relativehumidity_2m" in data["hourly"]:
                humidity = data["hourly"]["relativehumidity_2m"][0]
            return {
                "city": city,
                "temperature": data["current_weather"]["temperature"],
                "windspeed": data["current_weather"]["windspeed"],
                "humidity": humidity
            }
        else:
            error_msg = "Weather data not found"
            logging.error(f"Weather API error for city '{city}': {error_msg}")
            return {"city": city, "error": error_msg}
    except Exception as e:
        logging.error(f"Failed to get weather for city '{city}': {e}")
        return {"city": city, "error": str(e)}

@app.route('/api/weather', methods=['POST'])
def weather():
    try:
        data = request.json
        cities = data.get('cities')
        if not cities or not isinstance(cities, list):
            error_msg = "Cities must be a list"
            logging.error(f"Bad request: {error_msg}")
            return jsonify({"error": error_msg}), 400
        results = []
        for city in cities:
            result = get_weather_for_city(city)
            results.append(result)
        # Add to search history (latest first)
        search_history.insert(0, {"cities": cities, "results": results})
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error in /api/weather endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/history/last5', methods=['GET'])
def history_last_five():
    try:
        # Return only the last five search entries (latest first)
        return jsonify(search_history[:5])
    except Exception as e:
        logging.error(f"Error in /api/history/last5 endpoint: {e}")
        return jsonify([]), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    try:
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logging.error(f"Error serving static file '{path}': {e}")
        return "Internal server error", 500

if __name__ == '__main__':
    app.run(debug=True)