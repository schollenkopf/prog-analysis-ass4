class Abstraction:
    values = []

    def handle_binary(b, s) -> ([()], [(str, ())]):
        pass

    def handle_if(b, s) -> ([()], [(str, ())]):
        pass

    def handle_incr(b, s) -> ([()], [(str, ())]):
        pass

    def handle_store(b, s) -> ([()], [(str, ())]):
        pass

    def handle_ifz(b, s) -> ([()], [(str, ())]):
        pass

    def handle_return(b, s) -> ([()], [(str, ())]):
        pass

    def handle_push(b, s) -> ([()], [(str, ())]):
        pass

    def handle_push(b, s) -> ([()], [(str, ())]):
        pass


class SignAbstraction(Abstraction):
    values = ["-", "+", "0"]

    def handle_binary(self, b, state) -> ([()], [(str, ())]):
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
                            ((lv, os + ["+"], (am_, i + 1)), memory),
                            ((lv, os + ["0"], (am_, i + 1)), memory),
                            ((lv, os + ["-"], (am_, i + 1)), memory),
                        ],
                        [],
                    )
            case "mul":
                if val1 == "0" or val2 == "0":
                    return ([((lv, os + ["0"], (am_, i + 1)), memory)], [])
                elif val1 == "-" or val2 == "-":
                    return ([((lv, os + ["-"], (am_, i + 1)), memory)], [])
                else:
                    return ([((lv, os + ["+"], (am_, i + 1)), memory)], [])
            case _:
                ([], [("Unsupported", ((lv, os, (am_, i)), memory))])
                return None

    def handle_if(b, s) -> ([()], [(str, ())]):
        pass

    def handle_incr(b, s) -> ([()], [(str, ())]):
        pass

    def handle_store(b, s) -> ([()], [(str, ())]):
        pass

    def handle_ifz(b, s) -> ([()], [(str, ())]):
        pass

    def handle_return(b, s) -> ([()], [(str, ())]):
        pass

    def handle_push(b, s) -> ([()], [(str, ())]):
        pass

    def handle_push(b, s) -> ([()], [(str, ())]):
        pass
