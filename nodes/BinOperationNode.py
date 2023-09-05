from tokens.token import Token
from .Node import Node


class BinOperationNode(Node):
    def __init__(self, operator: Token, leftNode: Node, rightNode: Node) -> None:
        # super().__init__()
        self.operator: Token = operator
        self.leftNode: Node = leftNode
        self.rightNode: Node = rightNode
