class Abstraction:
    def handle_binary(b, s) -> ([()], [(str, ())]):
        pass

    def handle_if(b, s) -> ([()], [(str, ())]):
        pass

    def handle_incr(b, s) -> ([()], [(str, ())]):
        pass

    def handle_store(b, s) -> ([()], [(str, ())]):
        pass

    def handle_ifz(b, s) -> ([()], [(str, ())]):  # if zero
        pass

    def join_state(self, state, stateMap) -> ({}, []):
        pass


class SignAbstraction(Abstraction):
    values = ["-", "+", "0"]

    def join_state(self, state, state_map):
        (lv, os, (am_, i)), memory = state
        if not i in state_map.keys():
            state_map[i] = state
        (old_lv, old_os, (old_am_, i)), old_memory = state_map[i]
        hasChanged = False
        for key in memory.keys():
            if memory[key] != old_memory[key]:
                hasChanged = True
                memory[key] = memory[key].union(old_memory[key])  # not sure
        for si, o in enumerate(os):  # si is stack index
            if os[si] != old_os[si]:
                hasChanged = True
                os[si] = o.union(old_os)
        state_map[i] = state
        add_work_queue = []
        if hasChanged:
            add_work_queue.append(i)
        return (state_map, add_work_queue)

    def handle_binary(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        val1 = os.pop()
        val2 = os.pop()

        match b["operant"]:
            case "add":
                if val1 == "+" and val2 == "+":
                    return ([((lv, os + ["+"], (am_, i + 1)), memory)], [])
                elif (val1 == "+" and val2 != "-") or (val1 != "-" and val2 == "+"):
                    return ([((lv, os + ["+"], (am_, i + 1)), memory)], [])
                elif (val1 == "-" and val2 != "+") or (val1 != "+" and val2 == "-"):
                    return ([((lv, os + ["-"], (am_, i + 1)), memory)], [])
                elif val1 == "0" and val2 == "0":
                    return ([((lv, os + ["0"], (am_, i + 1)), memory)], [])
                else:
                    return (
                        [
                            ((lv, os.copy() + ["+"], (am_, i + 1)), memory.copy()),
                            ((lv, os.copy() + ["0"], (am_, i + 1)), memory.copy()),
                            ((lv, os.copy() + ["-"], (am_, i + 1)), memory.copy()),
                        ],
                        [],
                    )
            case "mul":
                if val1 == "0" or val2 == "0":
                    return ([((lv, os + ["0"], (am_, i + 1)), memory)], [])
                elif val1 == "-" or val2 == "-":
                    return ([((lv, os + ["+"], (am_, i + 1)), memory)], [])
                else:
                    return ([((lv, os + ["+"], (am_, i + 1)), memory)], [])
            case _:
                return ([], [("Unsupported", ((lv, os, (am_, i)), memory))])

    def handle_if(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        match b["condition"]:
            case "gt":
                val2 = os[-2]
                val1 = os[-1]
                if val2 == "+":
                    if val1 == "+":
                        return (
                            [
                                ((lv, os.copy(), (am_, i + 1)), memory.copy()),
                                ((lv, os.copy(), (am_, b["target"])), memory.copy()),
                            ],
                            [],
                        )
                    else:
                        return ([((lv, os, (am_, i + 1)), memory)], [])
                elif val2 == "0":
                    if val1 == "+":
                        return ([((lv, os, (am_, b["target"])), memory)], [])
                    elif val1 == "-":
                        return ([((lv, os, (am_, i + 1)), memory)], [])
                    else:
                        return ([((lv, os, (am_, b["target"])), memory)], [])
                else:
                    if val1 == "-":
                        return (
                            [
                                ((lv, os.copy(), (am_, i + 1)), memory.copy()),
                                ((lv, os.copy(), (am_, b["target"])), memory.copy()),
                            ],
                            [],
                        )
                    else:
                        return ([((lv, os, (am_, b["target"])), memory)], [])

            case _:
                log("unsupported operation", b)
                return ([], [("Unsupported", ((lv, os, (am_, i)), memory))])

    def handle_push(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        v = b["value"]
        if isinstance(v["value"], int):
            if v["value"] > 0:
                return [((lv, os + ["+"], (am_, i + 1)), memory)], []
            elif v["value"] == 0:
                return [((lv, os + ["0"], (am_, i + 1)), memory)], []
            else:
                return [((lv, os + ["-"], (am_, i + 1)), memory)], []
        return [((lv, os + [v["value"]], (am_, i + 1)), memory)], []

    def handle_incr(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        if b["amount"] > 0:
            match memory[b["index"]]:
                case "+":
                    return [((lv, os, (am_, i + 1)), memory)], []
                case "0":
                    memory[b["index"]] = "+"
                    return [((lv, os, (am_, i + 1)), memory)], []
                case "-":
                    mem2 = memory.copy()
                    memory[b["index"]] = "0"
                    return [
                        ((lv, os.copy(), (am_, i + 1)), memory.copy()),
                        ((lv, os.copy(), (am_, i + 1)), mem2.copy()),
                    ], []
        elif b["amount"] < 0:
            match memory[b["index"]]:
                case "+":
                    mem2 = memory.copy()
                    memory[b["index"]] = "0"
                    return [
                        ((lv, os.copy(), (am_, i + 1)), memory.copy()),
                        ((lv, os.copy(), (am_, i + 1)), mem2.copy()),
                    ], []
                case "0":
                    memory[b["index"]] = "-"
                    return [((lv, os, (am_, i + 1)), memory)], []
                case "-":
                    return [((lv, os, (am_, i + 1)), memory)], []
        else:
            return [((lv, os, (am_, i + 1)), memory)], []

    def handle_ifz(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        match b["condition"]:
            case "le":
                val1 = os[-1]
                if val1 == "0":
                    return ([((lv, os, (am_, b["target"])), memory)], [])
                elif val1 == "-":
                    return ([((lv, os, (am_, b["target"])), memory)], [])
                else:
                    return ([((lv, os, (am_, i + 1)), memory)], [])

            case _:
                log("unsupported operation", b)
                return ([], [("Unsupported", ((lv, os, (am_, i)), memory))])


class RangeAbstraction(Abstraction):
    def handle_binary(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        (l1, h1) = os.pop()
        (l2, h2) = os.pop()

        match b["operant"]:
            case "add":
                return ([((lv, os + [(l1 + l2, h1 + h2)], (am_, i + 1)), memory)], [])
            case "mul":
                return ([((lv, os + [(l1 * l2, h1 * h2)], (am_, i + 1)), memory)], [])
            case _:
                return ([], [("Unsupported", ((lv, os, (am_, i)), memory))])

    def handle_if(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        match b["condition"]:
            case "gt":
                (l2, h2) = os[-2]
                (l1, h1) = os[-1]
                if l2 > h1:
                    return ([((lv, os, (am_, b["target"])), memory)], [])
                elif not h2 > l1:
                    return ([((lv, os, (am_, i + 1)), memory)], [])
                else:
                    return (
                        [
                            ((lv, os.copy(), (am_, i + 1)), memory.copy()),
                            ((lv, os.copy(), (am_, b["target"])), memory.copy()),
                        ],
                        [],
                    )
            case _:
                log("unsupported operation", b)
                return ([], [("Unsupported", ((lv, os, (am_, i)), memory))])

    def handle_push(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        v = b["value"]
        if isinstance(v["value"], int):
            os.append((v["value"], v["value"]))
            return [((lv, os, (am_, i + 1)), memory)], []
        return [((lv, os + [v["value"]], (am_, i + 1)), memory)], []

    def handle_incr(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        (l1, h1) = memory[b["index"]]
        memory[b["index"]] = (l1 + b["amount"], h1 + b["amount"])
        return [((lv, os, (am_, i + 1)), memory)], []

    def handle_ifz(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        match b["condition"]:
            case "le":
                (l1, h1) = os[-1]
                if l1 > 0:
                    return ([((lv, os, (am_, i + 1)), memory)], [])
                elif h1 < 0:
                    return ([((lv, os, (am_, b["target"])), memory)], [])
                else:
                    return (
                        [
                            ((lv, os.copy(), (am_, i + 1)), memory.copy()),
                            ((lv, os.copy(), (am_, b["target"])), memory.copy()),
                        ],
                        [],
                    )

            case _:
                log("unsupported operation", b)
                return ([], [("Unsupported", ((lv, os, (am_, i)), memory))])
