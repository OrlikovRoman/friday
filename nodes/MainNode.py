from .Node import Node


class MainNode(Node):
    def __init__(self) -> None:
        self.codeStrings: Node = []

    def addNode(self, node: Node):
        self.codeStrings.append(node)
