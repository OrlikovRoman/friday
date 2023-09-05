import keyboard
import os
import AppOpener as aopen

from recognition.voice import tts
from utils import console
from utils.setup import settings
from utils.setup import keys
from utils import setup

import pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps


def test() -> None:
    tts.speak("Здравствуйте!")


def time() -> None:
    tts.speak("Текущее время: " + console.get_short_time())


def weather() -> None:
    owm: OWM = OWM(keys.get("pyowm"))
    manager = owm.weather_manager()
    observation = manager.weather_at_place(setup.city)
    weather = observation.weather

    tts.speak(
        f"Сейчас на улице {round(weather.temperature('celsius').get('temp'))} градусов")


def write(text: str) -> None:
    keyboard.write(
        console.correct(
            str(text)
        )
    )


def enter() -> None:
    keyboard.send("enter")


def open(text: str) -> None:
    programm_list = {
        "блокнот": "start notepad",
        "браузер": "start https://yandex.com/",
        "ютуб": "start https://youtube.com/",
        "телеграмм": 'start /D "C:\\Users\\Alian\\AppData\\Roaming\\Telegram Desktop\\" Telegram',
        "проводник": "start explorer",
        "диспетчер": "start taskmgr"
    }

    if text in programm_list:
        os.system(programm_list.get(text))


def close() -> None:
    keyboard.send("alt+f4")


def save() -> None:
    keyboard.send("ctrl+s")


def sleep() -> None:
    tts.speak("Всегда к вашим услугам")
