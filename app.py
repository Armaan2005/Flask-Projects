from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

API_KEY = "61775e42f72ad0fc85447ef0195ec8e4"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/WeatherForm', methods=['GET'])
def weather_form():
    return render_template("index2.html")

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get("city")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        
        weather = {'error': f"City '{city}' not found!"}
        return render_template("index2.html", **weather)

    
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    condition = data['weather'][0]['main'].lower()

    
    if "rain" in condition:
        weather_class = "rain"
    elif "snow" in condition:
        weather_class = "snow"
    elif "cloud" in condition:
        weather_class = "clouds"
    elif "clear" in condition:
        weather_class = "clear"
    else:
        weather_class = "default"

    weather = {
        'city': city,
        'temperature': temp,
        'description': desc,
        'weather_class': weather_class
    }

    return render_template("index2.html", **weather)

if __name__ == '__main__':
    app.run(debug=True)
    