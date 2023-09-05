import json


with open("settings.json", "r", encoding="utf-8") as file:
    settings: dict = json.load(file)
    lang: str = settings.get("language")
    city: str = settings.get("city")


tts = settings.get("tts")
stt = settings.get("stt")
wake_word = settings.get("wake_word")


tts_model = settings.get("assets").get("models").get("tts").get(lang).get(tts)
stt_model = settings.get("assets").get("models").get("stt").get(lang).get(stt)
wake_word_model = settings.get("assets").get(
    "models").get("stt").get(lang).get(wake_word)


keys = settings.get("assets").get("keys")
