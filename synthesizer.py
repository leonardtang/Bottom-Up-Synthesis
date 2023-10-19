import numpy as np
from collections import defaultdict
from itertools import combinations_with_replacement
from syntax_tree import ArithmeticSyntaxTree, StringSyntaxTree


class Synthesizer:
    """
    Input: I/O examples (I, O) and AST
    Output: Program consistent with (I, O)
    """

    def __init__(self, in_list, out_list, ast) -> None:
        self.inputs = in_list
        self.outputs = out_list
        self.ast_template = ast

        if ast is ArithmeticSyntaxTree:
            self.terminal_nodes = [
                ArithmeticSyntaxTree(operator="identity", child=0),
                ArithmeticSyntaxTree(operator="identity", child=1),
                ArithmeticSyntaxTree(operator="identity", child=5),
                ArithmeticSyntaxTree(operator="input")
            ]
        elif ast is StringSyntaxTree:
            self.terminal_nodes = []
            for inp in self.inputs:
                if type(inp) is list:
                    assert len(inp) == 2
                    self.terminal_nodes.append(ast(operator="input_x", child=inp[0]))
                    self.terminal_nodes.append(ast(operator="input_y", child=inp[1]))
                elif type(inp) is str:
                    self.terminal_nodes.append(ast(operator="input", child=inp))
            self.terminal_nodes.append(StringSyntaxTree(operator="identity", child=" "))
        
        self.plist = self.terminal_nodes
        # Horribly hacky way of getting operators
        self.operators = self.plist[-1].operators
        self.uni_ops = self.plist[-1].unary_operators
        self.bin_ops = self.plist[-1].binary_operators

    def grow(self):
        # Given a list of expressions, return all expressions that can be obtained by applying an operation
        new_plist = []
        # Apply unary operators
        for child_prog in self.plist:
            for op in self.uni_ops:
                if op == "input" or op == "identity":
                    continue
                # print('op?', op)
                candidate_prog = self.ast_template(op, child=child_prog)
                expression = candidate_prog.construct()
                if expression.startswith('Right(Input)'):
                    print('unary Expression', expression)
                new_plist.append(candidate_prog)

        # Apply binary operators
        for pair in combinations_with_replacement(self.plist, 2):
            left_prog, right_prog = pair
            for op in self.bin_ops:
                # if op == 'input' or op == 'identity': continue
                # print('bin op', op)
                # print('bin outer left', left_prog.operator)
                # print('bin outer right', right_prog.operator)
                candidate_prog = self.ast_template(op, left=left_prog, right=right_prog)
                expression = candidate_prog.construct()
                # test = right_prog.construct()
                # if test == 'Input(y)':
                # print('bin Expression', expression)
                new_plist.append(candidate_prog)
        
        # new_plist = self.sort(new_plist)
        # new_plist = self.prune(new_plist)
        self.plist.extend(new_plist)

    def prune(self, candidates):
        """
        Eliminate observational equivalents from a list of candidate programs
        """
        outputs_db = defaultdict(list)
        for idx, p in enumerate(candidates):
            try:
                outputs = [p.evaluate(self.inputs[i]) for i in range(len(self.inputs))]
                outputs_db[tuple(outputs)].append(idx)
            except:
                continue

        duplicates = [idx for indices in outputs_db.values() if len(indices) > 1 for idx in indices[1:] ]
        candidates = np.delete(candidates, duplicates).tolist()
        return candidates

    def sort(self, candidates):
        """
        Sort programs by parsimony (here, just by length)
        """
        return sorted(candidates, key=lambda p: len(p.construct()))

    def synthesize(self):
        while True:
            self.grow()
            self.plist = self.sort(self.plist)
            self.plist = self.prune(self.plist)
            for p in self.plist:
                try:
                    # print('p.evaluate on input:', self.inputs[0])
                    # print(p.construct())
                    # print(p.evaluate(self.inputs[0]))
                    if all(
                        [
                            p.evaluate(self.inputs[i]) == self.outputs[i]
                            for i in range(len(self.inputs))
                        ]
                    ):
                        return p.construct()
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
        ([1, 2, 3, 4, 5], [-2, -4, -6, -8, -10]),
        ([3, 4, 5], [9, 16, 25]),
        ([5, 10, 15], [1, 2, 3]),
        ([100, 50, 20], [10, 5, 2]),
        ([1, 2, 3], [3 * x + 5 for x in [1, 2, 3]]),
        # ([1, 2, 3], [x ** 2 + 6 * x for x in [1, 2, 3]])
    ]
    for inputs, outputs in test_pairs:
        print("------------------")
        print("Inputs:", inputs)
        print("Outputs:", outputs)
        synth = Synthesizer(inputs, outputs, ArithmeticSyntaxTree)
        result = synth.synthesize()
        print("Program:", result)


def test_string():
    test_pairs = [
        # (["hello", "world"], ["h", "w"]),
        # (["hello", "world"], ["o", "d"]),
        # ([["hello", "you"], ["world", "domination"]], ["helloyou", "worlddomination"]),
        # (
        #     [["hello", "you"], ["world", "domination"]],
        #     ["hello you", "world domination"],
        # ),
        # (["hello", "world", "domination"], ["ho", "wd", "dn"]),
        # (["llms", "are", "bad"], ["ls", "ae", "bd"]),
        # ([["the", "adults"], ["are", "talking"]], ["ta", "at"]),
        (["the", "adults", "are", "talking"], ["T", "A", "A", "T"]),
        (["mUltImodAL", "ArchiTecTure"], ["ml", "ae"]),
        ([" ", " hello world   "], ["", "hello world"])
    ]
    for inputs, outputs in test_pairs:
        print("------------------")
        print("Inputs:", inputs)
        print("Outputs:", outputs)
        synth = Synthesizer(inputs, outputs, StringSyntaxTree)
        result = synth.synthesize()
        print("Program:", result)


if __name__ == "__main__":
    test_arithmetic()
    test_string()
