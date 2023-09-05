from Token import Token
from AST.ExpressionNode import ExpressionNode

class VariableNode(ExpressionNode):
    def __init__(self, variable:Token) -> None:
        super().__init__()
        self.variable:Token = variable