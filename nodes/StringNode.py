from tokens.token import Token


class StringNode:
    def __init__(self, string: Token) -> None:
        self.token: Token = string
