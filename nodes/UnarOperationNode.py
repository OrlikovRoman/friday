from .Node import Node
from tokens.token import Token


class UnarOperationNode:
    def __init__(self, operator: Token, operand: Node) -> None:
        self.operator: Token = operator
        self.operand: Node = operand
