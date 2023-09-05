from tokens.token import TokenType
from tokens.token import type_list
from utils import console

from nodes.Node import Node
from nodes.MainNode import MainNode
from nodes.DefaultNode import DefaultNode
from nodes.TestNode import TestNode
from nodes.ExitNode import ExitNode
from nodes.UnarOperationNode import UnarOperationNode
from nodes.BinOperationNode import BinOperationNode
from nodes.StringNode import StringNode
from nodes.NumberNode import NumberNode

from dataclasses import dataclass


@dataclass
class Frame:
    vars: dict
    node: Node
    result: any = None
    segment: int = 0
    state: int = 0


class Stack:
    def __init__(self) -> None:
        self.__frames: list = []

    def push(self, frame: Frame) -> Frame:
        self.__frames.append(frame)
        return frame

    def pop(self) -> Frame:
        return self.__frames.pop()

    def peek(self) -> Frame:
        return self.__frames[-1]

    def size(self) -> int:
        return len(self.__frames)


class Parser:
    def match(self, *expected: TokenType):
        if self.position < len(self.token_list):
            currentToken = self.token_list[self.position]
            for element in expected:
                if element.name == currentToken.type.name:
                    self.position += 1
                    return currentToken
        return None

    def require(self, expected: TokenType, parent):
        if not parent:
            console.error('Не указан родитель require')
        token = self.match(expected)
        if not token:
            console.error(
                f'После команды "{parent.text}" ожидается аргумент или текст')
        return token

    def parse(self, token_list, command) -> MainNode:
        self.position: int = 0
        self.token_list = token_list
        self.command = command

        root: MainNode = MainNode()
        while self.position < len(self.token_list):
            codeStringNode: DefaultNode = self.parseExpression()
            root.addNode(codeStringNode)

        return root

    def parseExpression(self) -> DefaultNode:
        string = self.match(type_list.get("string"))
        if string:
            return StringNode(string)

        write = self.match(type_list.get("write"))
        if write:
            operand = self.match(type_list.get("string"))
            if operand:
                return UnarOperationNode(write, StringNode(operand))

        open = self.match(type_list.get("open"))
        if open:
            operand = self.match(type_list.get("string"))
            if operand:
                return UnarOperationNode(open, StringNode(operand))

        sleep = self.match(type_list.get("sleep"))
        if sleep:
            return ExitNode()

        return self.parseDefault()

    def parseDefault(self) -> DefaultNode:
        try:
            default: DefaultNode = DefaultNode(self.token_list[self.position])
            self.position += 1
            return default
        except IndexError:
            return

    def run(self, main_node: MainNode) -> bool:
        stack: Stack = Stack()
        if len(list(filter(
            lambda x: not isinstance(x, StringNode),
            main_node.codeStrings
        ))) == 0:
            return False

        for node in main_node.codeStrings:
            stack.push(Frame(vars={}, node=node))
            result = None
            while stack.size() != 0:
                match stack.peek():
                    case frame if frame.segment == 0:
                        if isinstance(frame.node, DefaultNode):
                            frame.node.token.type.callback()

                        if isinstance(frame.node, TestNode):
                            print("test complete")

                        if isinstance(frame.node, ExitNode):
                            type_list.get("sleep").callback()
                            return False

                        if isinstance(frame.node, StringNode):
                            result: str = str(frame.node.token.text)

                        if isinstance(frame.node, UnarOperationNode):
                            if frame.node.operator.type.name == "write":
                                if isinstance(frame.node.operand, StringNode):
                                    if frame.state == 0:
                                        stack.push(
                                            Frame(
                                                vars={},
                                                node=frame.node.operand
                                            )
                                        )

                                        frame.state = 1
                                        continue

                                text: str = result
                                frame.node.operator.type.callback(text)
                            if frame.node.operator.type.name == "open":
                                if isinstance(frame.node.operand, StringNode):
                                    if frame.state == 0:
                                        stack.push(
                                            Frame(
                                                vars={},
                                                node=frame.node.operand
                                            )
                                        )

                                        frame.state = 1
                                        continue

                                text: str = result
                                frame.node.operator.type.callback(text)

                        frame.segment = 1
                        continue
                    case frame if frame.segment == 1:
                        stack.pop()
                        continue
        return True
