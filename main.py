from interpret import Interpreter


cases = [
    # ("dtu/compute/exec/Simple", "noop"),
    # ("dtu/compute/exec/Simple", "zero"),
    # ("dtu/compute/exec/Simple", "hundredAndTwo"),
    # ("dtu/compute/exec/Simple", "identity"),
    # ("dtu/compute/exec/Simple", "add"),
    # ("dtu/compute/exec/Simple", "min"),
    ("dtu/compute/exec/Simple", "factorial")
    # ("dtu/compute/exec/Simple", "main"),
]

for case in cases:
    print("---", case, "---")
    ci = Interpreter(case, {0: 6, 1: 3})
    res = ci.execute(print)
    print(res)
    print("--- done ---")
