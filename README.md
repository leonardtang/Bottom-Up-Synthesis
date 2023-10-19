# Bottom-Up Enumerative Search

> *Baby program synthesis, or is it actually SOTA?*

We consider synthesizing two DSLs/Syntax Trees:
- ArithmeticSyntaxTree, consisting of `+`, `-`, `x`, `/` operations
- StringSyntaxTree, consisting of `Concat`, `Left`, `Right`, `Upper`, `Lower`, `Trim` operations

`Synthesizer` implements bottom-up enumerative search with pruning and parsimonious priority for both DSLs.

But first, there is an env file believe it or not:
```
conda env create --name synth --file=synth.yml
```

Given an inputs/outputs pairing and appropriate Syntax Tree, synthesize a program as follows:

```
synth = Synthesizer(inputs, outputs, ArithmeticSyntaxTree)
```
```
synth = Synthesizer(inputs, outputs, StringSyntaxTree)
```

To test synthesis in both settings, run:
```
python synthesizer.py
```