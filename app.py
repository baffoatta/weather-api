from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import requests
import os
import traceback
import logging

load_dotenv()
app = Flask(__name__)
CORS(app)

# Configuration
def get_env_variable(key, default=None):
    return os.environ.get(key, default)

api_key = get_env_variable("WEATHER_API_KEY", "3332dad34986")
base_url = "http://api.openweathermap.org/data/2.5/weather"

logging.basicConfig(level=logging.DEBUG)

def get_weather_data(city):
    """Retrieve weather data for the specified city."""
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  
        }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        return data
    except requests.RequestException as e:
        return jsonify({"error": f"Network error: {str(e)}"}), 500
    except KeyError as e:
        return jsonify({"error": f"An error occured: {str(e)}"}), 400
    
    
    
    
@app.route('/weather', methods=['GET'])
def weather():
    """Endpoint to get weather information based on the provided city parameter."""
    city = request.args.get('city')

    if not city:
        app.logger.error('City parameter is required')
        return jsonify({'error': 'City parameter is required'}), 400

    weather_data = get_weather_data(city)

    if 'error' in weather_data:
        print('Error in get_weather_data:', weather_data['error'])
        traceback.print_exc()  # Print the traceback
        return jsonify(weather_data), 500

    print('Full response from OpenWeatherMap API:', weather_data)
    
    # Ensure 'weather' key is present in the response
    if 'weather' not in weather_data:
        print('Error: Weather information not found in the response.')
        return jsonify({'error': 'Weather information not found in the response'}), 500


    # Extract relevant information from the API response
    main_weather = weather_data['weather'][0]['main']
    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    result = {
        'city': city,
        'weather': main_weather,
        'description': description,
        'temperature': temperature,
        'humidity': humidity
    }

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)