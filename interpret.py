from filereader import find_method


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


class Interpreter:
    def __init__(self, am, inital_memory={}):
        self.memory = inital_memory
        self.mstack = [([], [], (am, 0))]

    def execute(self, log):
        for i in range(100):
            log("->", self.mstack, self.memory, end="")

            (lv, os, (am_, i)) = self.mstack[-1]
            b = find_method(am_)["code"]["bytecode"][i]
            match (b["opr"]):
                case "return":
                    log("(return)")
                    return self.handle_return(b, log)
                case "push":
                    log("(push)")
                    self.handle_push(b, log)
                case "load":
                    log("(load)")
                    self.handle_load(b, log)
                case "binary":
                    log("(binary)")
                    self.handle_binary(b, log)
                case "if":
                    log("(if)")
                    self.handle_if(b, log)
                case "store":
                    log("(store)")
                    self.handle_store(b, log)
                case "ifz":
                    log("(ifz)")
                    self.handle_ifz(b, log)
                case "incr":
                    log("(incr)")
                    self.handle_incr(b, log)
                case "goto":
                    log("(goto)")
                    self.handle_goto(b, log)
                case "get":
                    log("(get)")
                    self.handle_get(b, log)
                case "invoke":
                    log("(invoke)")
                    self.handle_invoke(b, log)
                case _:
                    log("unsupported operation", b)
                    return None

    def handle_goto(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        self.mstack.pop()
        self.mstack.append((lv, os, (am_, b["target"])))

    def handle_invoke(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        arg_list = []
        for arg in b["method"]["args"]:
            arg_list.append(os.pop())

        objectRef = lambda x: x
        match b["access"]:
            case "virtual":
                objectRefString = os.pop()
                if objectRefString == "java/io/PrintStream":
                    objectRef = JavaMethod.println

                ret = objectRef(*arg_list)

            case "static":
                objectRefString = b["method"]["ref"]["name"]
                initial_memory = {}
                for i, arg in enumerate(arg_list):
                    initial_memory[i] = arg
                interpreter = Interpreter(
                    (objectRefString, b["method"]["name"]), initial_memory
                )
                ret = interpreter.execute(print)

            case _:
                log("unsupported operation", b)
                return None
        if b["method"]["returns"] != None:
            os = os + [ret]
        self.mstack.pop()
        self.mstack.append((lv, os, (am_, i + 1)))

    def handle_incr(self, b, log):
        self.memory[b["index"]] = self.memory[b["index"]] + b["amount"]
        (lv, os, (am_, i)) = self.mstack[-1]
        self.mstack.pop()
        self.mstack.append((lv, os, (am_, i + 1)))

    def handle_store(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        match b["type"]:
            case "int":
                self.memory[b["index"]] = os.pop()
                self.mstack.pop()
                self.mstack.append((lv, os, (am_, i + 1)))
            case _:
                log("unsupported operation", b)
                return None

    def handle_if(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        match b["condition"]:
            case "gt":
                if os[-2] > os[-1]:
                    self.mstack.pop()
                    self.mstack.append((lv, os, (am_, b["target"])))
                else:
                    self.mstack.pop()
                    self.mstack.append((lv, os, (am_, i + 1)))

            case _:
                log("unsupported operation", b)
                return None

    def handle_ifz(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        match b["condition"]:
            case "le":
                if os[-1] <= 0:
                    self.mstack.pop()
                    self.mstack.append((lv, os, (am_, b["target"])))
                else:
                    self.mstack.pop()
                    self.mstack.append((lv, os, (am_, i + 1)))

            case _:
                log("unsupported operation", b)
                return None

    def handle_return(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        match (b["type"]):
            case None:
                return None
            case "int":
                return os[-1]
            case _:
                log("unsupported operation", b)
                return None

    def handle_push(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        v = b["value"]
        _ = self.mstack.pop()
        self.mstack.append((lv, os + [v["value"]], (am_, i + 1)))

    def handle_load(self, b, log):
        (lv, os, (am_, i)) = self.mstack[-1]
        _ = self.mstack.pop()
        self.mstack.append((lv, os + [self.memory[b["index"]]], (am_, i + 1)))

    def handle_get(self, b, log):
        (lv, os, (am_, i)) = self.mstack.pop(-1)
        value = getattr(JavaMethod, "get")(b["field"])
        self.mstack.append((lv, os + [value], (am_, i + 1)))

    def handle_binary(self, b, log):
        match b["operant"]:
            case "add":
                (lv, os, (am_, i)) = self.mstack[-1]
                a = os.pop()
                b = os.pop()
                _ = self.mstack.pop()
                self.mstack.append((lv, os + [a + b], (am_, i + 1)))
            case "mul":
                (lv, os, (am_, i)) = self.mstack[-1]
                a = os.pop()
                b = os.pop()
                _ = self.mstack.pop()
                self.mstack.append((lv, os + [a * b], (am_, i + 1)))
            case _:
                log("unsupported operation", b)
                return None
