from services.user_service import UserService
from weather import get_weather_data

class WeatherService:
    def __init__(self):
        self.user_service = UserService()

    async def get_weather(self, username: str, city: str = None):
        if not city:
            city = self.user_service.get_user_city(username)
            if not city:
                return None, "Город не зарегистрирован"
        
        weather_data = await get_weather_data(city)
        return weather_data, None