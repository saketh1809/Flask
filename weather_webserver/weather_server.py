from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

def fetch_weather():
    try:
        city = "hyderabad"
        url = f"https://www.google.com/search?q=weather+{city}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find temperature
        temperature_elem = soup.find('div', class_='BNeawe iBp4i AP7Wnd')
        temperature = temperature_elem.get_text() if temperature_elem else "N/A"

        # Find weather description
        weather_elem = soup.find('div', class_='BNeawe tAd8D AP7Wnd')
        weather_info = weather_elem.get_text().split('\n') if weather_elem else ["N/A", "N/A"]
        weather = weather_info[1]

        # Get current time
        current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %I:%M %p')

        return temperature, weather, current_time

    except requests.RequestException as e:
        print(f"Request error fetching weather: {e}")
    except Exception as e:
        print(f"Error fetching weather: {e}")

    return "N/A", "N/A", "N/A"

@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event handler for updating weather information
@socketio.on('request_weather')
def handle_weather_request():
    while True:
        eventlet.sleep(5)  
        temperature, weather, current_time = fetch_weather()
        emit('update_weather', {'temperature': temperature, 'weather': weather, 'current_time': current_time})

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)