import pyttsx3
import wave
import pyaudio
import re
from utils.setup import settings
from utils import setup

speak_engine: pyttsx3.Engine = pyttsx3.init()


def filter_text(text: str) -> str:
    filter_words_list: dict[str, str] = {
        "пожалуйста": "пожалуста",
        "помочь": "памочь",
        "весилить": "висилить",
    }

    doubled_letters: dict[str, str] = {
        'нн': "н",
        "сс": "с",
    }

    filter_special_letters: str = r"[\?\[\]\(\)\{\}\\\./'\":;<>\$%\^\&#@\!\,`~\+\-№\*]+"

    # text: str = re.sub(
    #     filter_special_letters, text.lower(), ""
    # )
    for word, replace_word in filter_words_list.items():
        text = text.replace(word, replace_word)

    for doubled_letter, letter in doubled_letters.items():
        text = text.replace(doubled_letter, letter)

    return text


def speak(text: str, tts_text: str = "") -> str:
    voice_id: str = setup.tts_model
    tts_text: str = filter_text(text)
    if tts_text:
        tts_text: str = filter_text(tts_text)

    print(tts_text)

    speak_engine.setProperty('voice', voice_id)
    speak_engine.say(tts_text)
    speak_engine.runAndWait()
    speak_engine.stop()
    return text.capitalize()


def play_sound(sound) -> None:
    CHUNK: int = 1024
    wf: wave.Wave_read = wave.open(sound, 'rb')
    p: pyaudio.PyAudio = pyaudio.PyAudio()
    stream: pyaudio.Stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                    channels=wf.getnchannels(),
                                    rate=wf.getframerate(),
                                    output=True)

    data: bytes = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
