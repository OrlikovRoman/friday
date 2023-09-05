from utils import console
from tokens import execute


class TokenType:
    def __init__(self, name: str, regex: str, callback=lambda: None, is_owner_string: bool = False) -> None:
        self.name: str = name
        self.regex: str = regex
        self.callback = callback
        self.is_owner_string: bool = is_owner_string

    def __str__(self) -> str:
        return "<Type of \"" + str(self.name) + "\">"


class Token:
    def __init__(self, type: TokenType, text: str, position: int) -> None:
        self.type: TokenType = type
        self.text: str = text
        self.position: int = position

    def __str__(self) -> str:
        return "<Token: " + str(self.type) + ">"


no_lex_type_list: dict = {

}

type_list: dict[str, TokenType] = {
    "test": TokenType("test", [r"привет"], execute.test),
    "time": TokenType("time", [r"время", r"времени"], execute.time),
    "weather": TokenType("weather", [r"погода", r"погоду", r"погоды"], execute.weather),
    "write": TokenType("write", [r"напиши"], execute.write, True),
    "enter": TokenType("enter", [r"отправить", r"отправь", r"следующая строка"], execute.enter),
    "open": TokenType("open", [r"открой", r"открыть"], execute.open),
    "close": TokenType("close", [r"закрыть", r"закрой"], execute.close),
    "save": TokenType("save", [r"сохранить", r"сохрани"], execute.save),
    "end": TokenType("end", [r"конец текста", r"конец"]),
    "sleep": TokenType("sleep", [r"спасибо", r"отдохни"], execute.sleep),
    "space": TokenType("space", [r"\s+"]),
    "string": TokenType("string", [r"\w+"])
}
