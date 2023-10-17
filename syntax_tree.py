from abc import ABC, abstractmethod

class Node:
    pass

class Statement(Node):
    pass

class Expression(Statement):
    pass

class BinaryExpression(Expression):
    def __init__(self, left: Expression, op: str, right: Expression):
        self.left = left
        # String representing the operator (e.g., "+", "-", "*", "/")
        self.op = op
        self.right = right

class UnaryExpression(Expression):
    def __init__(self, op):
        self.op = op

class Identifier(Expression):
    def __init__(self, identifier: str):
        self.identity = identifier

class NumericLiteral(Expression):
    def __init__(self, value):
        self.value = value

class AbstractSyntaxTree(ABC):

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def do_something(self):
        pass
