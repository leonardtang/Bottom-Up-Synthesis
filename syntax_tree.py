from abc import ABC, abstractmethod


class AbstractSyntaxTree(ABC):
    def __init__(self, operator, left, right, child):
        self.operators = None
        self.operator = operator
        self.left = left
        self.right = right
        self.child = child

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def construct(self):
        pass


class ArithmeticSyntaxTree(AbstractSyntaxTree):
    def __init__(self, operator, left=None, right=None, child=None):
        self.operators = ["+", "x", "/", "-", "input", "identity"]
        self.operator = operator
        self.unary_operators = ["input", "identity"]
        self.binary_operators = ["+", "x", "/", "-"]
        assert self.operator in self.operators
        if operator == "input":
            self.left = None
            self.right = None
            self.child = None
        elif operator == "identity":
            assert child is not None
            self.left = None
            self.right = None
            self.child = child
        else:
            assert left is not None and right is not None
            self.left = left
            self.right = right
            self.child = None

    def evaluate(self, input_val):
        """
        Calculate the numerical value of the given program
        """
        # print('operator', self.operator)
        # print('left', self.left)
        # print('right', self.right)

        # Hit UnaryExpression: retrieve single numerical value
        if self.operator == "input":
            return input_val
        if self.operator == "identity":
            return self.child

        # BinaryExpressions
        if self.operator == "+":
            return self.left.evaluate(input_val) + self.right.evaluate(input_val)
        elif self.operator == "x":
            return self.left.evaluate(input_val) * self.right.evaluate(input_val)
        elif self.operator == "/":
            return self.left.evaluate(input_val) / self.right.evaluate(input_val)
        elif self.operator == "-":
            return self.left.evaluate(input_val) - self.right.evaluate(input_val)
        else:
            assert False

    def construct(self):
        """
        Recursively construct a program (i.e. use grammar to generate code)
        """
        if self.operator == "input":
            return f"y"
        if self.operator == "identity":
            return f"{self.child}"

        if self.operator == "+":
            return f"({self.left.construct()} + {self.right.construct()})"
        elif self.operator == "x":
            return f"({self.left.construct()} x {self.right.construct()})"
        elif self.operator == "/":
            return f"({self.left.construct()} / {self.right.construct()})"
        elif self.operator == "-":
            return f"({self.left.construct()} - {self.right.construct()})"
        else:
            assert False


class StringSyntaxTree(AbstractSyntaxTree):
    def __init__(self, operator, left=None, right=None, child=None):
        self.operators = [
            "concat",
            "right",
            "left",
            "input",
            "input_x",
            "input_y",
            "identity",
        ]
        self.unary_operators = [
            "right",
            "left",
            "input",
            "input_x",
            "input_y",
            "identity",
        ]
        self.binary_operators = ["concat"]
        self.operator = operator
        assert self.operator in self.operators
        if operator in {"input", "input_x", "input_y"}:
            self.left = None
            self.right = None
            self.child = None
        elif operator in {"identity", "left", "right"}:
            assert child is not None
            self.left = None
            self.right = None
            self.child = child
        else:
            assert left is not None and right is not None
            self.left = left
            self.right = right
            self.child = None

    def evaluate(self, input_val):
        """
        Calculate the string value of the given program
        """
        # Unary
        if self.operator == "input":
            return input_val
        elif self.operator == "input_x":
            assert type(input_val) == list
            assert len(input_val) == 2
            return input_val[0]
        elif self.operator == "input_y":
            assert type(input_val) == list
            assert len(input_val) == 2
            return input_val[1]
        elif self.operator == "identity":
            return self.child
        elif self.operator == "left":
            return self.child.evaluate(input_val)[0]
        elif self.operator == "right":
            return self.child.evaluate(input_val)[-1]

        # Binary
        if self.operator == "concat":
            return self.left.evaluate(input_val) + self.right.evaluate(input_val)
        else:
            assert False

    def construct(self):
        """
        Recursively construct a program (i.e. use grammar to generate code)
        """
        # Unary
        if self.operator in ["input", "input_x"]:
            return "Input(x)"
        elif self.operator == "input_y":
            return "Input(y)"
        elif self.operator == "identity":
            return f"{self.child}"
        elif self.operator == "left":
            return f"Left({self.child.construct()})"
        elif self.operator == "right":
            return f"Right({self.child.construct()})"

        # Binary
        if self.operator == "concat":
            return f"Concat({self.left.construct()}, {self.right.construct()})"
        else:
            assert False


# TODO: extend left/right to more than just most left and most right?
