from abstraction import RangeAbstraction, SignAbstraction
from abstractionMain import AbstractionMain


cases = [
    # ("dtu/compute/exec/Simple", "noop"),
    # ("dtu/compute/exec/Simple", "zero"),
    # ("dtu/compute/exec/Simple", "hundredAndTwo"),
    # ("dtu/compute/exec/Simple", "identity"),
    # ("dtu/compute/exec/Simple", "add"),
    # ("dtu/compute/exec/Simple", "min"),
    ("dtu/compute/exec/Simple", "div")
    # ("dtu/compute/exec/Simple", "factorial")‚
    # ("dtu/compute/exec/Simple", "main"),
    # ("dtu/exceptional/Arrays", "alwaysThrows")
]

for case in cases:
    print("---", case, "---")
    # ci = AbstractionMain(case, SignAbstraction(), {0: "+", 1: "+"})
    ci = AbstractionMain(case, RangeAbstraction(), {0: (1, 4), 1: (1, 3)})
    res = ci.execute(print)
    print(res)
    print("--- done ---")
