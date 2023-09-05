from .Node import Node
from tokens.token import Token


class DefaultNode(Node):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
