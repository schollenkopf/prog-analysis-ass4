from filereader import find_method


class Interpreter:

    def __init__(self,am,inital_memory={}):
        self.memory = inital_memory
        self.mstack = [([],[],(am,0))]

    def execute(self,log):
        for i in range(10):
            log("->", self.mstack, end="")
            (lv, os, (am_,i)) = self.mstack[-1]
            b = find_method(am_)["code"]["bytecode"][i]
            match (b["opr"]):
                case "return":
                    log("(return)")
                    return self.handle_return(b,log)
                case "push":
                    log("(push)")
                    self.handle_push(b,log)
                case "load":
                    log("(load)")
                    self.handle_load(b,log)
                case "binary":
                    log("(binary)")
                    self.handle_binary(b,log)
                case "if":
                    log("(if)")
                    self.handle_if(b,log)
                case "store":
                    log("(store)")
                    self.handle_store(b,log)
                case "ifz":
                    log("(ifz)")
                case _:
                    log("unsupported operation",b)
                    return None
                

    def handle_store(self,b,log):
        (lv, os, (am_,i)) = self.mstack[-1]
        match b["type"]:
            case "int":
                self.memory["index"] = os.pop()
                self.mstack.pop()
                self.mstack.append((lv, os, (am_,i+1)))
            case _:
                log("unsupported operation",b)
                return None


    def handle_if(self,b,log):
        (lv, os, (am_,i)) = self.mstack[-1]
        match b["condition"]:
            case "gt":
                if os[-2]>os[-1]:
                    self.mstack.pop()
                    self.mstack.append((lv, os, (am_,b["target"])))
                else:
                    self.mstack.pop()
                    self.mstack.append((lv, os, (am_,i + 1)))
            
            case _:
                log("unsupported operation",b)
                return None

    
    def handle_return(self,b,log):
        (lv, os, (am_,i)) = self.mstack[-1]
        match (b["type"]):
            case None:
                return None
            case "int":
                return os[-1]
            case _:
                log("unsupported operation",b)
                return None
    
    def handle_push(self,b,log):
        (lv, os, (am_,i)) = self.mstack[-1]
        v = b["value"]
        _ = self.mstack.pop()
        self.mstack.append((lv, os + [v["value"]], (am_,i + 1 )))
    
    def handle_load(self,b,log):
        (lv, os, (am_,i)) = self.mstack[-1]
        _ = self.mstack.pop()
        self.mstack.append((lv, os + [self.memory[b["index"]]], (am_,i + 1 )))

    def handle_binary(self,b,log):
        match b["operant"]:
            case "add":
                (lv, os, (am_,i)) = self.mstack[-1]
                a = os.pop()
                b = os.pop()
                _ = self.mstack.pop()
                self.mstack.append((lv, os + [a+b], (am_,i+1)))
            case _:
                log("unsupported operation",b)
                return None

    