class Abstraction:
    values = []

    def handle_binary(b, s) -> ([], [(str, ())]):
        pass

    def handle_if(b, s) -> ((int, []), [str]):
        pass

    def handle_incr(b, s) -> ((int, []), [str]):
        pass

    def handle_store(b, s) -> ((int, []), [str]):
        pass

    def handle_ifz(b, s) -> ((int, []), [str]):
        pass

    def handle_return(b, s) -> ((int, []), [str]):
        pass

    def handle_push(b, s) -> ((int, []), [str]):
        pass

    def handle_push(b, s) -> ((int, []), [str]):
        pass


class SignAbstraction(Abstraction):
    values = ["-", "+", "0"]

    def handle_binary(b, s) -> ((int, []), [str]):
        (lv, os, (am_, i)) = s
        a = os.pop()
        b = os.pop()

        match b["operant"]:
            case "add":
                if a == "+" and b == "+":
                    return ([(lv, os + ["+"], (am_, i + 1))], [])
                elif (a == "+" and b != "-") or (a != "-" and b == "+"):
                    return ([(lv, os + ["+"], (am_, i + 1))], [])
                elif (a == "-" and b != "+") or (a != "+" and b == "-"):
                    return ([(lv, os + ["-"], (am_, i + 1))], [])
                elif a == "0" and b == "0":
                    return ([(lv, os + ["0"], (am_, i + 1))], [])
                else:
                    return (
                        [
                            (lv, os + ["+"], (am_, i + 1)),
                            (lv, os + ["0"], (am_, i + 1))(
                                lv, os + ["-"], (am_, i + 1)
                            ),
                        ],
                        [],
                    )
            case "mul":
                if a == "0" or b == "0":
                    return ([(lv, os + ["0"], (am_, i + 1))], [])
                elif a == "-" or b == "-":
                    return ([(lv, os + ["-"], (am_, i + 1))], [])
                else:
                    return ([(lv, os + ["+"], (am_, i + 1))], [])
            case _:
                ([], [("Unsupported", (lv, os, (am_, i)))])
                return None

    def handle_if(b, s) -> ((int, []), [str]):
        pass

    def handle_incr(b, s) -> ((int, []), [str]):
        pass

    def handle_store(b, s) -> ((int, []), [str]):
        pass

    def handle_ifz(b, s) -> ((int, []), [str]):
        pass

    def handle_return(b, s) -> ((int, []), [str]):
        pass

    def handle_push(b, s) -> ((int, []), [str]):
        pass

    def handle_push(b, s) -> ((int, []), [str]):
        pass
