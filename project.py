import requests
from gtts import gTTS
import os
import json

api_key = '*****************'

state = input("Enter state name: ").capitalize()
city = input("Enter a city name: ")
limit = 10

geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state}&limit={limit}&appid={api_key}'
geo_response = requests.get(geo_url)

if geo_response.status_code != 200 or not geo_response.json():
    print("Failed to retrieve geographic data.")
    exit()

geo_data = geo_response.json()
lati, longi = next(((entry["lat"], entry["lon"]) for entry in geo_data if entry.get("state") == state), (None, None))

if lati is None or longi is None:
    print("Coordinates not found.")
    exit()

api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
weather_response = requests.get(api_url)

if weather_response.status_code != 200:
    print("Failed to retrieve weather data.")
    exit()

weather_data = weather_response.json()

weather_info = (f"Weather in {city}:\n"
                f"Temperature: {weather_data['main']['temp']}°C\n"
                f"Weather: {weather_data['weather'][0]['description']}\n"
                f"Humidity: {weather_data['main']['humidity']}%\n"
                f"Wind Speed: {weather_data['wind']['speed']} m/s\n"
                f"Pressure: {weather_data['main']['pressure']} hPa\n")
print(weather_info)

air_quality_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lati}&lon={longi}&appid={api_key}'
air_quality_response = requests.get(air_quality_url)

if air_quality_response.status_code == 200:
    air_quality_data = air_quality_response.json()
    if "list" in air_quality_data and air_quality_data["list"]:
        aqi = air_quality_data["list"][0]["main"]["aqi"]
        aqi_description = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }.get(aqi, "AQI: " + str(aqi))
        air_quality_info = f"Air Quality in {city}: {aqi_description}\n"
    else:
        air_quality_info = "Air pollution data not found.\n"
else:
    air_quality_info = "Failed to retrieve air quality data.\n"

print(air_quality_info)

text = (f"Good morning! Here's the weather update for {city}. "
        f"The temperature is {weather_data['main']['temp']} degrees Celsius, "
        f"with {weather_data['weather'][0]['description']} weather. "
        f"Humidity is at {weather_data['main']['humidity']} percent, "
        f"wind speed is {weather_data['wind']['speed']} meters per second, "
        f"and atmospheric pressure is {weather_data['main']['pressure']} hPa. "
        f"The air quality is {aqi_description}. Stay safe and have a great day!")

speech = gTTS(text=text, lang="en", slow=False)
speech.save("weather.mp3")
print("Audio file saved as weather.mp3")

print("if you want to play weather news enter 1 else 0")
enter=int(input("enter 1 or 0 :"))
if enter == 1 :
 def play_audio(file_path):
        os.system(f"start {file_path}")

 play_audio("weather.mp3")

else:
    print("thank you ,have a great day")
    
with open("weather_news.txt", "w") as file:
    file.write(weather_info)
    file.write(air_quality_info)
    file.write(f"{text}\n")

print("Weather news saved to weather_news.txt")
    
