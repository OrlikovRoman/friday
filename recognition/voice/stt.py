import pyaudio
import struct
import json

import pvporcupine

from vosk import Model, KaldiRecognizer
from vosk import SetLogLevel
from recognition.voice import tts
from utils.setup import settings
from utils.setup import keys

SetLogLevel(-1)

opts: dict[str, tuple] = {
    'alias': ('ева', 'его', 'нива', 'и во'),
    'tbr': ()
}


def listen(*, sound=False, recorder: KaldiRecognizer) -> str:
    p: pyaudio.PyAudio = pyaudio.PyAudio()
    stream: pyaudio.Stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=16000
    )
    print('Распознание...')
    if sound:
        tts.play_sound('assets/audio/start.wav')
    stream.start_stream()

    while True:
        data: bytes = stream.read(8000)
        if len(data) == 0:
            break

        if recorder.AcceptWaveform(data):
            result_json: str = recorder.Result()
            result: dict = json.loads(result_json)
            result: str = f"{result.get('text')}"
            return result

    return ""


def wake_word(*, model: pvporcupine.Porcupine) -> None:
    porcupine: pvporcupine.Porcupine = model
    p: pyaudio.PyAudio = pyaudio.PyAudio()
    stream: pyaudio.Stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=model.frame_length
    )

    while True:
        audio: bytes = stream.read(porcupine.frame_length)
        audio_unpacked: tuple = struct.unpack_from(
            "h" * porcupine.frame_length, audio)
        keyword_index: int = porcupine.process(audio_unpacked)
        if keyword_index >= 0:
            break
