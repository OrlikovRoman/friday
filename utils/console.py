import sys
import os
import linecache
from datetime import datetime
from itertools import islice
from colorama import init
from colorama import Fore, Back, Style, Cursor
from textblob import TextBlob
init()


def correct(text: str) -> str:
    corrector: TextBlob = TextBlob(text)
    return str(corrector.correct())


tokens = {
    "white": Fore.WHITE,
    "black": Fore.BLACK,
    "grey": Style.BRIGHT + Fore.BLACK,
    "green": Fore.GREEN,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "red": Fore.RED,
    "yellow": Fore.YELLOW,
    "reset.fore": Fore.RESET,
    "white.back": Back.WHITE,
    "black.back": Back.BLACK,
    "grey.back": Style.BRIGHT + Back.BLACK,
    "green.back": Back.GREEN,
    "blue.back": Back.BLUE,
    "cyan.back": Back.CYAN,
    "magenta.back": Back.MAGENTA,
    "red.back": Back.RED,
    "yellow.back": Back.YELLOW,
    "reset.back": Back.RESET,
    "reset": Style.RESET_ALL,
    "bright": Style.BRIGHT,
    "dim": Style.DIM,
    "normal": Style.NORMAL
}


def remove_styles(text: str):
    for token in tokens.values():
        text = text.replace(token, "")
    return text


def get_style(pattern: str) -> str:
    word_list = pattern.split(" ")
    result = []
    for word in word_list:
        if word in tokens:
            result.append(tokens.get(word))

    return "".join(result)


def style(text: str, pattern: str) -> str:
    return get_style(pattern) + text + get_style("reset")


def get_time() -> str:
    now = datetime.now()
    time = now.time()
    return str(time)


def get_short_time() -> str:
    now = datetime.now()
    hour: str = str(now.hour)
    minute: str = str(now.minute).rjust(2, "0")

    return hour + ":" + minute


def log(*text: str, separator=" ") -> None:
    parts = []
    for item in text:
        parts.append(str(item))

    print(
        style(
            "[" + get_time() + "]",
            "dim grey"
        ),
        style(
            " Info ",
            "grey.back white"
        ),
        separator.join(parts)
    )


def warn(*text: str, separator=" ") -> None:
    parts = []
    for item in text:
        parts.append(str(item))

    print(
        style(
            "[" + get_time() + "]",
            "dim bright yellow"
        ),
        style(
            " Warn ",
            "bright yellow.back white"
        ),
        separator.join(parts)
    )


def success(*text: str, separator=" ") -> None:
    parts = []
    for item in text:
        parts.append(str(item))

    print(
        style(
            "[" + get_time() + "]",
            "dim bright green"
        ),
        separator.join(parts),
        "✅"
    )


def debug(*text: str, separator=" ") -> None:
    parts = []
    for item in text:
        parts.append(str(item))

    print(
        style(
            "⚙️  [" + get_time() + "]",
            "dim grey"
        ),
        separator.join(parts)
    )


def error(*text: str, error=Exception, separator=" ") -> None:
    parts = []
    for item in text:
        parts.append(str(item))

    raise Exception(separator.join(parts))


def get(title: str = "") -> any:
    return input(style(str(title) + " > ", "grey"))


def mult(char: str, count: int) -> str:
    return str(char) * int(count)


def get_file_line(path, line_number: int) -> str:
    return linecache.getline(path, line_number)


def get_file_lines(path: str, line: int) -> str:
    numbers = [
        line - 2,
        line - 1,
        line,
        line + 1,
        line + 2
    ]

    lines = []

    for number in numbers:
        lines.append(get_file_line(path, number).strip("\n"))

    return lines, numbers


def excepthook(type, value, traceback) -> None:
    width, _ = os.get_terminal_size()
    table = [""]
    lines = [
        style(
            "Detail:",
            "bright red"
        )
    ]
    corner = [" ╔", "╗ ", " ╚", "╝ "]
    border_head = "═"
    border_side = " ║ "
    # corner = [" ┏", "┓ ", " ┗", "┛ "]
    # border_head = "━"
    # border_side = " ┃ "
    # corner = [" ╭", "╮ ", " ╰", "╯ "]
    # border_head = "─"
    # border_side = " │ "

    while traceback:
        path = traceback.tb_frame.f_code.co_filename
        name = traceback.tb_frame.f_code.co_name
        line = traceback.tb_lineno

        lines.append(
            style("File ", "grey") + path +
            style(" in ", "grey") + name +
            style(" ↴", "bright red")
        )
        lines.append("")

        file_lines, numbers = get_file_lines(path, line)
        for index, file_line in enumerate(file_lines):
            line_number = numbers[index]
            if line_number == line:
                cursor = style(
                    " ►  ",
                    "bright red"
                )
            else:
                cursor = "    "

            lines.append(
                cursor +
                style(
                    str(line_number),
                    "grey"
                ) + "  " +
                file_line
            )

        lines.append("")

        traceback = traceback.tb_next

    lines.append(
        style(
            "[" + get_time() + "]",
            "dim bright red"
        ) + " " +
        style(
            f" {type.__name__} ",
            "bright red.back white"
        ) + " " +
        str(value)
    )

    # table
    actual_width = width - 6
    table.append(
        style(
            corner[0] +
            " Traceback ".center(width - 4, border_head) + corner[1],
            "bright red"
        )
    )

    for line in lines:
        table.append(
            style(border_side, "bright red") + line + mult(" ", actual_width - len(remove_styles(line))) +
            style(border_side, "bright red")
        )

    table.append(
        style(
            corner[2] + mult(border_head, width - 4) + corner[3],
            "bright red"
        )
    )

    print("\n".join(table))


def excepthook_init():
    sys.excepthook = excepthook
