from flask import Flask, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__)

def get_coord(zipcode):
    api_key = '03d39d0a4844727881ad16a48828f5f0'
    url = f'https://api.openweathermap.org/geo/1.0/zip?zip={zipcode}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def get_hour(timestamp):
    time = datetime.fromtimestamp(timestamp)
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S')
    hour = timeStr[11:13]
    if eval(hour) > 12:
        hourInt = eval(hour) - 12
        strhour = str(hourInt) + " PM"
    else:
        if hour == "00":
            strhour = "12 AM" 
        else:
            strhour = hour + " AM"
    return strhour

def get_response(data):
    response_data = {
            '1':
            {
                'time': data[0][0],
                'temp': data[0][1],
                'forecast': data[0][2]
            },
            '2':
            {
                'time': data[1][0],
                'temp': data[1][1],
                'forecast': data[1][2]
            },
            '3':
            {
                'time': data[2][0],
                'temp': data[2][1],
                'forecast': data[2][2]
            },
            '4':
            {
                'time': data[3][0],
                'temp': data[3][1],
                'forecast': data[3][2]
            },
            '5':
            {
                'time': data[4][0],
                'temp': data[4][1],
                'forecast': data[4][2]
            },
            '6':
            {
                'time': data[5][0],
                'temp': data[5][1],
                'forecast': data[5][2]
            }
        }
    return response_data


def get_hourly(lat, lon):
    api_key = '03d39d0a4844727881ad16a48828f5f0'
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,alerts&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        hourly_forecasts = data["hourly"][:6]
        for i in range(0,6):
            strhour = get_hour(hourly_forecasts[i]["dt"])
            data[i] = [strhour,
                hourly_forecasts[i]["temp"],
                hourly_forecasts[i]["weather"][0]["description"]]
        response_data = get_response(data)
        
    else:
        response_data = {
        'error': "unknown error"
    }
    return response_data
    
    

@app.route('/coord/<zipcode>', methods=['GET'])
def coord(zipcode):
    
    # Get the weather data for the provided zip code
    coord_data = get_coord(zipcode)

    if 'cod' in coord_data and coord_data['cod'] == '400':
        return jsonify({'error': 'Invalid Zip Code'}), 400
    
    if 'cod' in coord_data and coord_data['cod'] == '404':
        return jsonify({'error': 'Coordinates not found'}), 404

    # Extract relevant weather information
    lat = coord_data['lat']
    lon = coord_data['lon']
    data = get_hourly(lat, lon)
    

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
