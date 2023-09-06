from utils import console
from utils import setup
import sys
import os
import time
import pyfiglet

from threading import Thread

from recognition.text.lexer import Lexer
from recognition.text.parser import Parser
from recognition.voice import stt
from recognition.voice import tts

from vosk import Model, KaldiRecognizer
import pvporcupine
from utils.setup import settings
from utils.setup import keys

from nodes.MainNode import MainNode
console.excepthook_init()
console.success("Modules loaded!")


def logo() -> None:
    f: pyfiglet.Figlet = pyfiglet.Figlet(font="slant")
    print(
        console.style(
            f.renderText("Friday"),
            "bright red"
        )
    )

    print(
        "Version:",
        setup.settings.get("version")
    )

    print(
        console.style(
            "By @weegex",
            "grey"
        )
    )


def create_models() -> tuple:
    console.log("Создание моделей")

    vosk_model: Model = Model(
        setup.stt_model
    )
    recorder: KaldiRecognizer = KaldiRecognizer(vosk_model, 16000)
    porcupine_model: pvporcupine.Porcupine = pvporcupine.create(
        access_key=keys.get("pvporcupine"),
        keyword_paths=setup.wake_word_model.get("keyword"),
        model_path=setup.wake_word_model.get("model")
    )

    console.success("Готов к работе!")

    return recorder, porcupine_model


class Assistant:
    def __init__(self) -> None:
        self.recorder, self.porcupine_model = create_models()

        # thread_1 = Thread(target=self.wait_input).start()
        # thread_2 = Thread(target=self.listen).start()

        self.listen()

    def wait_input(self) -> None:
        while True:
            self.command = console.get()
            if self.command:
                self.run()

    def listen(self) -> None:
        while True:
            self.process = True
            stt.wake_word(model=self.porcupine_model)
            while self.process:
                # self.command: str = str(console.get())
                self.command: str = stt.listen(
                    sound=True, recorder=self.recorder
                )
                if self.command:
                    console.log("Распознано: ", self.command)
                else:
                    console.warn("Не удалось распознать голос")

                self.run()

    def run(self) -> None:
        token_list: list = Lexer().analysis(self.command)
        # for token in token_list:
        #     console.debug(token.type.name)

        parser: Parser = Parser()
        main_node: MainNode = parser.parse(token_list, self.command)
        self.process: bool = parser.run(main_node)
        # for node in main_node.codeStrings:
        #     console.debug(str(node) + "\n-----\n" +
        #                   str(node.__dict__) + "\n-----")


if __name__ == "__main__":
    try:
        time.sleep(1)
        os.system("cls||clear")
        logo()
        print()
        Assistant()
    except KeyboardInterrupt:
        print("\n")
        console.success("Closed")
