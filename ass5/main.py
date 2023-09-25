from abstraction import SignAbstraction
from abstractionMain import AbstractionMain


cases = [
    # ("dtu/compute/exec/Simple", "noop"),
    #  ("dtu/compute/exec/Simple", "zero"),
    # ("dtu/compute/exec/Simple", "hundredAndTwo"),
    # ("dtu/compute/exec/Simple", "identity"),
    ("dtu/compute/exec/Simple", "add"),
    # ("dtu/compute/exec/Simple", "min"),
    # ("dtu/compute/exec/Simple", "factorial")
    # ("dtu/compute/exec/Simple", "main"),
]

for case in cases:
    print("---", case, "---")
    ci = AbstractionMain(case, SignAbstraction())
    res = ci.execute(print)
    print(res)
    print("--- done ---")
