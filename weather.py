import requests
import logging
import datetime
from config import open_weather_token

# Токен для доступа к OpenWeather API
open_weather_token = open_weather_token  # Замените на свой токен

async def get_weather_data(city_name: str):
    code_to_smile = {
        "Clear": "Ясно ☀️",
        "Clouds": "Облачно ☁️",
        "Rain": "Дождь 🌧",
        "Drizzle": "Дождь 🌧",
        "Thunderstorm": "Гроза ⚡",
        "Snow": "Снег ❄️",
        "Mist": "Туман 🌫"
    }
    try:
        logging.info(f"Запрос погоды для города: {city_name}")

        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        if data.get("cod") != 200:
            return None

        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода")

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        weather_data = {
            "city": city,
            "cur_weather": cur_weather,
            "wd": wd,
            "humidity": humidity,
            "pressure": pressure,
            "wind": wind,
            "sunrise_timestamp": sunrise_timestamp.strftime('%H:%M'),
            "sunset_timestamp": sunset_timestamp.strftime('%H:%M'),
            "length_of_the_day": str(length_of_the_day)
        }
        return weather_data
    except Exception as ex:
        logging.error(f"Ошибка при получении данных: {ex}")
        return None
