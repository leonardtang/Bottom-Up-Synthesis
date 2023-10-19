from syntax_tree import ArithmeticSyntaxTree, StringSyntaxTree
from itertools import combinations_with_replacement

# Just start off with arithmetic for now
class Synthesizer:
    """
    Input: I/O examples (I, O)
    Output: Program consistent with (I, O)
    """
    def __init__(self, in_list, out_list, ast) -> None:
        self.inputs = in_list
        self.outputs = out_list
        self.ast_template = ast
        # How to factor in input from the in_list???
        # ArithmeticDSL terminals:
        # self.terminal_nodes = [ast(operator='identity', child=0), ast(operator='identity', child=1), ast(operator='input')]
        # StringDSL terminals
        self.terminal_nodes = []
        for inp in self.inputs:
            if type(inp) is list:
                assert len(inp) == 2
                self.terminal_nodes.append(ast(operator='input_x', child=inp[0]))
                self.terminal_nodes.append(ast(operator='input_y', child=inp[1]))
            elif type(inp) is str:
                self.terminal_nodes.append(ast(operator='input', child=inp))
        self.terminal_nodes.append(ast(operator='identity', child=' '))
        self.plist = self.terminal_nodes
        # for p in self.plist:
        #     print(p.combine())
        #     print(p.evaluate(self.inputs[0]))
        # Horribly hacky way of getting operators
        self.operators = self.plist[-1].operators
        self.uni_ops = self.plist[-1].unary_operators
        self.bin_ops = self.plist[-1].binary_operators

    def grow(self):
        # Given a list of expressions, return all 1) expressions and 2) values that can be obtained 
        # by applying one of the operations to expressions in the list
        # print(self.plist)
        # input()
        new_plist = []
        # Maybe need to split into binary vs. unary operators
        for child_prog in self.plist:
            for op in self.uni_ops:
                if op == 'input' or op == 'identity': continue
                # print('unary op', op)
                # print('unary outer child', child_prog.operator)
                candidate_prog = self.ast_template(op, child=child_prog)
                expression = candidate_prog.combine()
                # if expression.startswith('Concat(Concat(Input(x), )'):
                # print('unary Expression', expression)
                new_plist.append(candidate_prog)

        for pair in combinations_with_replacement(self.plist, 2):
            left_prog, right_prog = pair
            for op in self.bin_ops:
                # if op == 'input' or op == 'identity': continue
                # print('bin op', op)
                # print('bin outer left', left_prog.operator)
                # print('bin outer right', right_prog.operator)
                candidate_prog = self.ast_template(op, left=left_prog, right=right_prog)
                # expression = candidate_prog.combine()
                # test = right_prog.combine()
                # if test == 'Input(y)':
                #     print('bin Expression', expression)
                new_plist.append(candidate_prog)

        # Prune here...
        self.plist.extend(new_plist)

    def prune(self):
        # Do something to plist. Eliminate observational equivalents
        # Test on all inputs to see which ones are the same
        # Seems like you would only want to do this on non-terminals
        pass

    def sort(self):
        # Sort programs by size
        pass

    def synthesize(self):
        while True:
            self.grow()
            self.sort()
            for p in self.plist:
                try:
                    # print('p.evaluate on input:', self.inputs[0])
                    # print(p.combine())
                    # print(p.evaluate(self.inputs[0]))
                    if all([p.evaluate(self.inputs[i]) == self.outputs[i] for i in range(len(self.inputs))]):
                        return p.combine()
                except:
                    # If program executes with errors, ditch it
                    continue

def test_arithmetic():
    test_pairs = [
        ([1, 2, 3, 4, 5], [1, 1, 1, 1, 1]),
        ([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]),
        ([1, 2, 3, 4, 5], [4, 8, 12, 16, 20]),
        ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]),
        ([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]),
        ([1, 2, 3, 4, 5], [-1, -2, -3, -4, -5]),
        ([1, 2, 3, 4, 5], [-2, -4, -6, -8, -10])
    ]
    for inputs, outputs in test_pairs:
        print('Inputs:', inputs)
        print('Outputs:', outputs)
        synth = Synthesizer(inputs, outputs, ArithmeticSyntaxTree)
        result = synth.synthesize()
        print('Program:', result)

def test_string():
    test_pairs = [
        (['hello', 'world'], ['h', 'w']),
        (['hello', 'world'], ['o', 'd']),
        ([['hello', 'you'], ['world', 'domination']], ['helloyou', 'worlddomination']),
        ([['hello', 'you'], ['world', 'domination']], ['hello you', 'world domination']),
        (['hello', 'world', 'domination'], ['ho', 'wd', 'dn'])
    ]
    for inputs, outputs in test_pairs:
        print('Inputs:', inputs)
        print('Outputs:', outputs)
        synth = Synthesizer(inputs, outputs, StringSyntaxTree)
        result = synth.synthesize()
        print('Program:', result)

if __name__ == "__main__":
    test_arithmetic()
    test_string()
