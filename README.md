# Тг бот для прогноза погоды на день

## Возможности
* Узнать прогноз в любом городе на данный момент времени.

## Запуск

Для работы с ботом понадобятся следующие файлы:
* Телеграм токен, полученный через [BotFather](https://web.telegram.org/a/#93372553).
* Токен с [OpenWeatherMap](https://openweathermap.org/) для получения данных о погоде (указан в `config.py`).

### Шаги для запуска:

1. Установите зависимости:
   
   ```bash
   pip install -r requirements.txt
2. Настройте файлы конфигурации (config.py) с вашими токенами от Telegram и OpenWeatherMap.
3. Запустите бота
   ```bash
   python run.py
4. Напишите название города в Telegram, и бот отправит прогноз погоды на данный момент времени.

## Структура файлов
  
1. **`run.py`**: Этот файл является точкой входа в приложение. Он запускает бота и инициализирует процесс обработки сообщений.

2. **`handler.py`**: Логика обработки команд и взаимодействия между моделью и представлением. Он управляет запросами от пользователей, получением данных от модели и передачей их в представление.

3. **`weather.py`**: Модель данных о погоде. Этот файл отвечает за запросы и обработку данных о текущей погоде с использованием API OpenWeather.

4. **`view.py`**: Форматирует и отправляет данные пользователю. Этот файл отвечает за то, как бот передает информацию о погоде пользователю (например, через сообщения в Telegram).

5. **`data.py`**: Работает с базой данных. Определяет модели базы данных, создает и извлекает данные пользователей (например, хранение города пользователя).

## Пример работы
После запуска бота напишите название города, и бот предоставит актуальную информацию о погоде в этом городе. Например:  

      Moscow
      
Бот ответит сообщением с текущими данными о погоде, включая температуру, влажность, давление и другие параметры:
```bash
Прогноз для города: Moscow
Температура: 5°C ☀️
Влажность: 60%
Давление: 1015 мм.рт.ст.
Скорость ветра: 3 м/с
Рассвет: 06:00
Закат: 18:30
```