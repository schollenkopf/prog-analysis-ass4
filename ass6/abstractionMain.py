from abstraction import Abstraction
from filereader import find_method


class AbstractionMain:
    def __init__(self, am, abstraction: Abstraction, inital_memory={}):
        self.state_map = {
            0: (([], [], (am, 0)), inital_memory)
        }  # key is PC and value is the state
        self.work_queue = [0]
        self.abstraction = abstraction

    def execute(self, log):
        while len(self.work_queue) > 0:
            pc = self.work_queue.pop()
            (lv, os, (am_, i)), memory = self.state_map(pc)
            b = find_method(am_)["code"]["bytecode"][pc]

            log("----------------------------------------------")
            log(self.state_map)

            match (b["opr"]):
                case "return":
                    log("(return)")
                    states = self.handle_return(b, self.state_map(pc), log)
                case "push":
                    log("(push)")
                    states = self.abstraction.handle_push(b, state, log)
                case "load":
                    log("(load)")
                    states = self.handle_load(b, self.state_map(pc), log)
                case "binary":
                    log("(binary)")
                    states = self.abstraction.handle_binary(b, state, log)
                case "if":
                    log("(if)")
                    states = self.abstraction.handle_if(b, state, log)
                case "store":
                    log("(store)")
                    states = self.handle_store(b, state, log)
                case "ifz":
                    log("(ifz)")
                    states = self.abstraction.handle_ifz(b, state, log)
                case "incr":
                    log("(incr)")
                    states = self.abstraction.handle_incr(b, state, log)
                case "goto":
                    log("(goto)")
                    states = self.handle_goto(b, state, log)
                # case "get":
                #     log("(get)")
                #     self.handle_get(b, log)
                # case "invoke":
                #     log("(invoke)")
                #     self.handle_invoke(b, log)
                case _:
                    log("unsupported operation", b)
                    return None

            for state in states:
                self.state_map, add_work_queue = self.abstraction.join_state(
                    state, self.state_map
                )
                if add_work_queue != []:
                    self.work_queue.append(add_work_queue)

    def handle_return(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        log("RETURN: ", os.pop())
        return [], []

    def handle_load(self, b, state, log):
        (lv, os, (am_, i)), memory = state
        if b["index"] not in memory.keys():
            raise Exception("Nulllptr")
        return [((lv, os + [memory[b["index"]]], (am_, i + 1)), memory)]

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
