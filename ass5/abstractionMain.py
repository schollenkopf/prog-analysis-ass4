from abstraction import Abstraction
from filereader import find_method


class AbstractionMain:
    def __init__(self, am, abstraction: Abstraction, inital_memory={}):
        self.states = [(([], [], (am, 0)), inital_memory)]
        self.error_states = []
        self.abstraction = abstraction

    def execute(self, log):
        for i in range(10):
            log("----------------------------------------------")
            log("Round: ", i, ", nr of states: ", len(self.states))
            log("States: ", self.states)
            log(
                "ErrorStates: ",
                self.error_states,
            )
            nextStates = []
            errorStates = []
            for state in self.states:
                s = []
                es = []
                log("->", state, end="")
                (lv, os, (am_, i)), memory = state
                b = find_method(am_)["code"]["bytecode"][i]
                match (b["opr"]):
                    case "return":
                        log("(return)")
                        s, es = self.handle_return(b, state, log)
                    # case "push":
                    #     log("(push)")
                    #     self.handle_push(b, log)
                    case "load":
                        log("(load)")
                        s, es = self.handle_load(b, state, log)
                    case "binary":
                        log("(binary)")
                        s, es = self.abstraction.handle_binary(b, state)
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
                if s != []:
                    nextStates += s
                if es != []:
                    errorStates += es
            if errorStates != []:
                self.error_states = errorStates
                # self.error_states.append(errorStates)
            if nextStates != []:
                self.states = nextStates
                # self.states.append(nextStates)

    def handle_return(self, b, s, log):
        return (s, [])

    def handle_load(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        if b["index"] not in memory.keys():
            return [], ["Nullptr", ((lv, os, (am_, i + 1)), memory)]
        return [((lv, os + [memory[b["index"]]], (am_, i + 1)), memory)], []
