from abstraction import Abstraction
from filereader import find_method


class AbstractionMain:
    def __init__(
        self, am, abstraction: Abstraction, inital_memory={}
    ):  # am is the case (method) we are considering, abstraction is the type
        # of abstraction, and the initial_memory is empty
        self.state_map = {
            0: (inital_memory, [], (am, 0))
        }  # key is PC and value is the state --> (([], [], (am, 0)), inital_memory)
        self.work_queue = [0]
        self.abstraction = abstraction  # in this case could be RangeAbstraction()

    def execute(self, log):
        while len(self.work_queue) > 0:
            log("----------------------------------------------")
            # log(self.state_map)
            pc = self.work_queue.pop()
            log("Looking at pc:", pc)
            log("With state", self.state_map[pc])
            lv, os, (am_, i) = self.state_map[pc]
            b = find_method(am_)["code"]["bytecode"][pc]

            match (b["opr"]):
                case "return":
                    log("(return)")
                    states = self.handle_return(b, self.state_map[pc], log)
                case "push":
                    log("(push)")
                    states = self.abstraction.handle_push(b, self.state_map[pc], log)
                case "load":
                    log("(load)")
                    states = self.handle_load(b, self.state_map[pc], log)
                case "binary":
                    log("(binary)")
                    states = self.abstraction.handle_binary(b, self.state_map[pc], log)
                case "if":
                    log("(if)")
                    states = self.abstraction.handle_if(b, self.state_map[pc], log)
                case "store":
                    log("(store)")
                    states = self.handle_store(b, self.state_map[pc], log)
                case "ifz":
                    log("(ifz)")
                    states = self.abstraction.handle_ifz(b, self.state_map[pc], log)
                case "incr":
                    log("(incr)")
                    states = self.abstraction.handle_incr(b, self.state_map[pc], log)
                case "goto":
                    log("(goto)")
                    states = self.handle_goto(b, self.state_map[pc], log)
                case "newarray":
                    log("(newarray)")
                    states = self.handle_newarray(b, self.state_map[pc], log)
                case "array_store":
                    log("(array_store)")
                    states = self.abstraction.handle_arraystore(
                        b, self.state_map[pc], log
                    )
                case "array_load":
                    log("(array_load)")
                    states = self.abstraction.handle_arraystore(
                        b, self.state_map[pc], log
                    )
                case "arraylength":
                    log("(arraylength)")
                    states = self.abstraction.handle_arraylength(
                        b, self.state_map[pc], log
                    )
                case "get":
                    log("(get)")
                    states = self.handle_get(b, self.state_map[pc], log)
                case "new":
                    log("(new)")
                    states = self.handle_new(b, self.state_map[pc], log)
                case "dup":
                    log("(dup)")
                    states = self.handle_dup(b, self.state_map[pc], log)
                case "invoke":
                    log("(invoke)")
                    states = self.handle_invoke(b, self.state_map[pc], log)
                case _:
                    log("unsupported operation", b)
                    return None

            for state in states:
                self.state_map, add_work_queue = self.abstraction.join_state(
                    state, self.state_map
                )

                if add_work_queue != []:
                    self.work_queue += add_work_queue

    def handle_return(self, b, state, log):
        lv, os, (am_, i) = state
        log("RETURN: ", os.pop())
        return []

    def handle_load(self, b, state, log):
        lv, os, (am_, i) = state
        if b["index"] not in lv.keys():
            raise Exception("Nulllptr", b)
        return [(lv, os + [lv[b["index"]]], (am_, i + 1))]

    def handle_newarray(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        return [(lv, os + [[None for _ in range(b["dim"])]], (am_, i + 1))]

    def handle_dup(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        return [(lv, os + [os[-1]], (am_, i + 1))]

    def handle_new(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        if b["class"] == "java/lang/AssertionError":
            return [(lv, os + [AssertionError], (am_, i + 1))]
        raise Exception("Unsupported", b)

    def handle_store(self, b, state, log) -> ([()], [(str, ())]):
        lv, os, (am_, i) = state
        match b["type"]:
            case "int":
                lv[b["index"]] = os.pop()
                return [(lv, os, (am_, i + 1))]
            case "ref":
                lv[b["index"]] = os.pop()
                return [(lv, os, (am_, i + 1))]
            case _:
                raise Exception("Unsupported", b)

    def handle_goto(self, b, state, log):
        lv, os, (am_, i) = state
        return [(lv, os, (am_, b["target"]))]

    def handle_get(self, b, state, log):
        lv, os, (am_, i) = state
        value = getattr(JavaMethod, "get")(b["field"])
        return [(lv, os + [value], (am_, i + 1))]

    def handle_invoke(self, b, state, log):
        lv, os, (am_, i) = state
        args = []
        for arg in b["method"]["args"]:
            args.append(os.pop())
        ref = os.pop()
        method = ref[b["method"]["ref"]["name"]]
        value = method(*args)
        if b["method"]["returns"] is not None:
            return [(lv, os + [value], (am_, i + 1))]
        return [(lv, os, (am_, i + 1))]


class JavaMethod:
    @staticmethod
    def get(field_dict):
        valid_dict = {
            "class": "java/lang/System",
            "name": "out",
            "type": {"kind": "class", "name": "java/io/PrintStream"},
        }

        return (
            field_dict.get("type", {}).get("name") if field_dict == valid_dict else None
        )

    @staticmethod
    def println(string):
        print(string)
