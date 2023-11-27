from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "787e8425651f9a39e14928d50e464d98"



@app.route('/weather', methods=['GET'])
def weather_info():
    CITY_NAME = request.args.get('city')

    if not CITY_NAME:
        return jsonify({'error': 'City parameter is missing'}), 400

    params = {
        "q": CITY_NAME,
        "appid": API_KEY
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()

        main_info = data['main']
        weather_info = data['weather'][0]
        temperature = main_info['temp']
        description = weather_info['description']

        result = {
            'city': CITY_NAME,
            'temperature': temperature,
            'description': description,
        }

        return jsonify(result)


    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching weather data: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
