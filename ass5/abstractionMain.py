from abstraction import Abstraction
from filereader import find_method


class AbstractionMain:
    def __init__(self, am, abstraction: Abstraction, inital_memory={}):
        self.states = [(([], [], (am, 0)), inital_memory)]
        self.error_states = [(str, ())]
        self.abstraction = abstraction

    def execute(self, log):
        for i in range(10):
            log("->", self.states, self.error_states, end="")
            for s, memory in self.states:
                nextStates = []

                (lv, os, (am_, i)) = s
                b = find_method(am_)["code"]["bytecode"][i]
                match (b["opr"]):
                    case "return":
                        log("(return)")
                        states, errorstates = self.handle_return(b, s, log)
                        nextStates.append(states)
                        self.error_states.append(errorstates)
                    # case "push":
                    #     log("(push)")
                    #     self.handle_push(b, log)
                    case "load":
                        log("(load)")
                        self.handle_load(b, s, memory, log)
                    case "binary":
                        log("(binary)")
                        nextStacks, errorStacks = self.abstraction.handle_binary(b, s)
                        for x in nextStacks:
                            nextStates.append((x, memory))
                        for xe in errorStacks:
                            self.error_states.append(xe + memory)
                    # case "if":
                    #     log("(if)")
                    #     self.handle_if(b, log)
                    # case "store":
                    #     log("(store)")
                    #     self.handle_store(b, log)
                    # case "ifz":
                    #     log("(ifz)")
                    #     self.handle_ifz(b, log)
                    # case "incr":
                    #     log("(incr)")
                    #     self.handle_incr(b, log)
                    # case "goto":
                    #     log("(goto)")
                    #     self.handle_goto(b, log)
                    # case "get":
                    #     log("(get)")
                    #     self.handle_get(b, log)
                    # case "invoke":
                    #     log("(invoke)")
                    #     self.handle_invoke(b, log)
                    case _:
                        log("unsupported operation", b)
                        return None
                self.states.append(nextStates)

    def handle_return(self, b, s, log):
        return (s, [])

    def handle_load(self, b, s, memory, log):
        (lv, os, (am_, i)) = s
        if b["index"] not in memory.keys():
            return [], ["Nullptr", (lv, os, (am_, i + 1))]
        return [(lv, os + [memory[b["index"]]], (am_, i + 1))], []
