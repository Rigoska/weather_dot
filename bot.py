import requests
import datetime
from loguru import logger
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import ow_token, tg_token

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 MB", compression="zip")

proxy_url = 'http://proxy.server:3128'
bot = Bot(token=tg_token, proxy=proxy_url)
dp = Dispatcher(bot)

logger.debug(proxy_url)
logger.debug(bot)
logger.debug(dp)

@dp.message_handler(commands=["start"])
async def start_command (message: types.Message):
        await message.reply("Привет! Напиши мне свой город и я предоставлю погодную сводку!")

@dp.message_handler()
async def get_weather(message: types.Message):
        code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

        try:
                r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={ow_token}&units=metric&lang=RU&exclude=minutely")
                data = r.json()

                logger.debug(r)
                logger.debug(data)

                weather_description = data["weather"][0]["main"]
                if weather_description in code_to_smile:
                        wd = code_to_smile[weather_description]
                else:
                        wd = "Посмотрите в окно, не пойму что там за погода!"

                city = data["name"]
                tmp = data["main"]["temp"]
                tmp_fls = data["main"]["feels_like"]
                hum = data["main"]["humidity"]
                prs = data["main"]["pressure"]
                wnd = data["wind"]["speed"]
                sun_r = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                sun_s = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

                await message.reply(
                                f"Температура воздуха в населенном пункте {city} составляет {tmp} °C, ощущается как {tmp_fls} °C.\n"
                                f"{wd}\n"
                                f"Влажность воздуха {hum} %.\n"
                                f"Скорость ветра {wnd} м/с.\n"
                                f"Атмосферное давление {prs} мм.рт.ст.\n"
                                f"Время восхода солнца {sun_r}.\n"
                                f"Время заката солнца {sun_s}.\n"
                                f"Хорошего дня!\n")

        except:
                await message.reply("Проверьте название города")

if __name__ == '__main__':
        executor.start_polling(dp)
        logger.debug(__name__)
