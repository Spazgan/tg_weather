import requests
import datetime
from pprint import pprint
from config import open_weather_token 

def get_weather(city, open_weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Tunderstrom": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_descripption = data["weather"][0]["main"]
        if weather_descripption in code_to_smile:
            wd = code_to_smile[weather_descripption]
        else:
            wd = "Посмотри в окно, не пойму что там за погода"
            
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        lenght_of_the_day = sunset_timestamp - sunrise_timestamp

        weather_data = {
            "city": city,
            "cur_weather": cur_weather,
            "wd": wd, 
            "humidity": humidity,
            "pressure": pressure,
            "wind": wind,
            "sunrise_timestamp": sunrise_timestamp,
            "sunset_timestamp": sunset_timestamp,
            "lenght_of_the_day": lenght_of_the_day
        }
        return weather_data
    
    except Exception as ex:
        print(ex)
        print("Проверьте город")

def print_weather(weather_data):
    if weather_data:
        print(f"\n***{datetime.datetime.now().strftime('%d-%Volgogradm-%Y %H:%M')}***")
        print (f"\nПогода в городе: {weather_data['city']}\nТемпиратура: {weather_data['cur_weather']}C° {weather_data['wd']}\n"
               f"Влажность: {weather_data['humidity']}%\nДавление: {weather_data['pressure']} мм.рт.ст.\nСкорость ветра: {weather_data['wind']}м/с\nРассвет: {weather_data['sunrise_timestamp']}\n"
               f"Закат: {weather_data['sunset_timestamp']}\nСветовой день: {weather_data['lenght_of_the_day']}")
    else: 
        print("Не удаётся получить данные о погоде!")

def main():
    city = input("Введите названия города: ")
    weather_data = get_weather(city, open_weather_token)
    print_weather(weather_data)


if __name__ == "__main__":
    main()




# print(f"\n***{datetime.datetime.now().strftime('%d-%Volgogradm-%Y %H:%M')}***")
        # print (f"\nПогода в городе: {city}\nТемпиратура: {cur_weather}C° {wd}\n"
        #        f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\nСкорость ветра: {wind}м/с\nРассвет: {sunrise_timestamp}\n"
        #        f"Закат: {sunset_timestam}\nСветовой день: {lenght_of_the_day}")