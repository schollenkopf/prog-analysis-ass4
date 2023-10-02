from abstraction import Abstraction
from filereader import find_method


class AbstractionMain:
    def __init__(self, am, abstraction: Abstraction, inital_memory={}):
        self.states = [(([], [], (am, 0)), inital_memory)]
        self.error_states = []
        self.abstraction = abstraction

    def execute(self, log):
        for i in range(30):
            log("----------------------------------------------")
            log("Round: ", i + 1, ", nr of states: ", len(self.states))
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
                    case "push":
                        log("(push)")
                        s, es = self.abstraction.handle_push(b, state, log)
                    case "load":
                        log("(load)")
                        s, es = self.handle_load(b, state, log)
                    case "binary":
                        log("(binary)")
                        s, es = self.abstraction.handle_binary(b, state, log)
                    case "if":
                        log("(if)")
                        s, es = self.abstraction.handle_if(b, state, log)
                    case "store":
                        log("(store)")
                        s, es = self.handle_store(b, state, log)
                    case "ifz":
                        log("(ifz)")
                        s, es = self.abstraction.handle_ifz(b, state, log)
                    case "incr":
                        log("(incr)")
                        s, es = self.abstraction.handle_incr(b, state, log)
                    case "goto":
                        log("(goto)")
                        s, es = self.handle_goto(b, state, log)
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
            else:
                log("----------------------------------------------")
                log(
                    "Finished after: ",
                    i + 1,
                    "rounds, nr of final states: ",
                    len(self.states),
                )
                log("States: ", self.states)
                log(
                    "ErrorStates: ",
                    self.error_states,
                )
                break

    def handle_return(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        log("RETURN: ", os.pop())
        return [], []

    def handle_load(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        if b["index"] not in memory.keys():
            return [], ["Nullptr", ((lv, os, (am_, i + 1)), memory)]
        return [((lv, os + [memory[b["index"]]], (am_, i + 1)), memory)], []

    def handle_store(self, b, state, log) -> ([()], [(str, ())]):
        (lv, os, (am_, i)), memory = state
        match b["type"]:
            case "int":
                memory[b["index"]] = os.pop()
                return [((lv, os, (am_, i + 1)), memory)], []
            case _:
                log("unsupported operation", b)
                return None

    def handle_goto(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        return [((lv, os, (am_, b["target"])), memory)], []
