class Abstraction:
    def handle_binary(b, state, log) -> []:
        pass

    def handle_if(b, state, log) -> []:
        pass

    def handle_incr(b, state, log) -> []:
        pass

    def handle_store(b, state, log) -> []:
        pass

    def handle_push(b, state, log) -> []:
        pass

    def handle_ifz(b, state, log) -> []:  # if zero
        pass

    def handle_arraystore(b, state, log) -> []:  # if zero
        pass

    def handle_arrayload(b, state, log) -> []:  # if zero
        pass

    def handle_arraylength(b, state, log) -> []:  # if zero
        pass

    def join_state(self, state, stateMap) -> ({}, []):
        pass


class SignAbstraction(Abstraction):
    values = ["-", "+", "0"]

    def join_state(self, state, state_map):
        lv, os, (am_, i) = state
        hasChanged = False
        if not i in state_map.keys():
            hasChanged = True
            state_map[i] = state
        old_lv, old_os, (old_am_, i) = state_map[i]

        for key in lv.keys():
            if lv[key] != old_lv[key]:
                hasChanged = True
                lv[key] = lv[key].union(old_lv[key])  # not sure
        for si, o in enumerate(os):  # si is stack index
            if si >= len(old_os):
                hasChanged = True
                old_os.append(o)
            elif os[si] != old_os[si]:
                hasChanged = True
                os[si] = o.union(old_os[si])
        state_map[i] = state
        add_work_queue = []
        if hasChanged:
            add_work_queue.append(i)
        return (state_map, add_work_queue)

    def handle_binary(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        val1 = os.pop()
        val2 = os.pop()

        match b["operant"]:
            case "add":
                ret_set = set()
                if "+" in val1 and "+" in val2:
                    ret_set = ret_set.union({"+"})
                if ("+" in val1 and not "-" in val2) or (
                    not "-" in val1 and "+" in val2
                ):
                    ret_set = ret_set.union({"+"})
                if ("-" in val1 and not "+" in val2) or (
                    not "+" in val1 and "-" in val2
                ):
                    ret_set = ret_set.union({"-"})
                if "0" in val1 and "0" in val2:
                    ret_set = ret_set.union({"0"})
                if ("+" in val1 and "-" in val2) or ("-" in val1 and "+" in val2):
                    ret_set = ret_set.union({"0", "-", "+"})
                return [(lv, os + [ret_set], (am_, i + 1))]

            case "mul":
                ret_set = set()
                if "0" in val1 or "0" in val2:
                    ret_set = ret_set.union({"0"})

                if ("-" in val1) ^ ("-" in val2):
                    ret_set = ret_set.union({"-"})
                else:
                    ret_set = ret_set.union({"+"})
                return [(lv, os + [ret_set], (am_, i + 1))]
            case "sub":
                if "+" in val2:
                    val2.union({"-"})
                    val2.remove("+")
                if "-" in val2:
                    val2.union({"+"})
                    val2.remove("-")

                ret_set = set()

                if "+" in val1 and "+" in val2:
                    ret_set = ret_set.union({"+"})
                if ("+" in val1 and not "-" in val2) or (
                    not "-" in val1 and "+" in val2
                ):
                    ret_set = ret_set.union({"+"})
                if ("-" in val1 and not "+" in val2) or (
                    not "+" in val1 and "-" in val2
                ):
                    ret_set = ret_set.union({"-"})
                if "0" in val1 and "0" in val2:
                    ret_set = ret_set.union({"0"})
                if ("+" in val1 and "-" in val2) or ("-" in val1 and "+" in val2):
                    ret_set = ret_set.union({"0", "-", "+"})
                return [(lv, os + [ret_set], (am_, i + 1))]

            case _:
                raise Exception("Unsupported", b)

    def handle_arrayload(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        index = os.pop()
        array = os.pop()
        if "-" in index:
            raise Exception("IndexOutOfBoundsException", b)
        if "+" in index:
            raise Exception("IndexOutOfBoundsException", b)
        else:
            new_array = array.copy()
            val = new_array[0]
            return [(lv, os + [val], (am_, i + 1))]

    def handle_arraylength(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        array = os.pop()
        if len(array) > 0:
            return [(lv, os + [{"0"}], (am_, i + 1))]
        else:
            return [(lv, os + [{"+"}], (am_, i + 1))]

    def handle_arraystore(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        val = os.pop()
        index = os.pop()
        array = os.pop()
        if "-" in index:
            raise Exception("IndexOutOfBoundsException", b)
        if "+" in index:
            raise Exception("IndexOutOfBoundsException", b)
        else:
            new_array = array.copy()
            new_array[0] = val
            return [(lv, os + [new_array], (am_, i + 1))]

    def handle_if(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        match b["condition"]:
            case "gt":
                # val2 > val1
                val1 = os.pop()
                val2 = os.pop()
                next = False
                target = False
                if "+" in val2:
                    if "+" in val1:
                        # Here we can return the states directly because it already allows for both target and next state to be taken
                        return [
                            (lv.copy(), os.copy(), (am_, i + 1)),
                            (lv.copy(), os.copy(), (am_, b["target"])),
                        ]

                    else:
                        next = True
                if "0" in val2:
                    if "+" in val1:
                        target = True
                    elif "-" in val1:
                        next = True
                    else:
                        target = True
                if "-" in val2:
                    if "-" in val1:
                        return [
                            (lv.copy(), os.copy(), (am_, i + 1)),
                            (lv.copy(), os.copy(), (am_, b["target"])),
                        ]

                    else:
                        target = True
                ret_states = []
                if next:
                    ret_states.append((lv.copy(), os.copy(), (am_, i + 1)))
                if target:
                    ret_states.append((lv.copy(), os.copy(), (am_, b["target"])))
                return ret_states

            case _:
                raise Exception("Unsupported", b)

    def handle_push(self, b, state, log):
        lv, os, (am_, i) = state
        v = b["value"]
        if isinstance(v["value"], int):
            if v["value"] > 0:
                return [(lv, os + [{"+"}], (am_, i + 1))]
            elif v["value"] == 0:
                return [(lv, os + [{"0"}], (am_, i + 1))]
            else:
                return [(lv, os + [{"-"}], (am_, i + 1))]
        return [(lv, os + [v["value"]], (am_, i + 1))]

    def handle_incr(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        var_sign = lv[b["index"]]
        ret_set = set()
        if b["amount"] > 0:
            if "+" in var_sign or "0" in var_sign:
                ret_set = ret_set.union({"+"})
            if "-" in var_sign:
                ret_set = ret_set.union({"+", "0", "-"})
            nlv = lv.copy()
            nlv[b["index"]] = ret_set
            return [(nlv, os, (am_, i + 1))]
        elif b["amount"] < 0:
            if "+" in var_sign:
                ret_set = ret_set.union({"+", "0", "-"})
            if "-" in var_sign or "0" in var_sign:
                ret_set = ret_set.union({"-"})
            nlv = lv.copy()
            nlv[b["index"]] = ret_set
            return [(nlv, os, (am_, i + 1))]
        else:
            return [(lv, os, (am_, i + 1))]

    def handle_ifz(self, b, state, log) -> []:
        lv, os, (am_, i) = state
        match b["condition"]:
            case "le":
                val1 = os[-1]
                return_states = []
                if "0" in val1:
                    return_states.append((lv, os, (am_, b["target"])))
                if "-" in val1:
                    return_states.append((lv, os, (am_, b["target"])))
                if "+" in val1:
                    return_states.append((lv, os, (am_, i + 1)))
                return return_states
            case "ne":
                val1 = os[-1]
                if val1 is None:
                    return [(lv, os, (am_, i + 1))]
                return_states = []
                if "0" in val1:
                    return_states.append((lv, os, (am_, i + 1)))
                if "-" in val1:
                    return_states.append((lv, os, (am_, b["target"])))
                if "+" in val1:
                    return_states.append((lv, os, (am_, b["target"])))
                return return_states
            case _:
                raise Exception("Unsupported", b)


# class RangeAbstraction(Abstraction):
#     def handle_binary(self, b, state, log) -> []:
#         lv, os, (am_, i) = state
#         (l1, h1) = os.pop()
#         (l2, h2) = os.pop()

#         match b["operant"]:
#             case "add":
#                 return ([((lv, os + [(l1 + l2, h1 + h2)], (am_, i + 1)), memory)], [])
#             case "mul":
#                 return ([((lv, os + [(l1 * l2, h1 * h2)], (am_, i + 1)), memory)], [])
#             case _:
#                 return ([], [("Unsupported", (lv, os, (am_, i)))])

#     def handle_if(self, b, state, log) -> []:
#         lv, os, (am_, i) = state
#         match b["condition"]:
#             case "gt":
#                 (l2, h2) = os[-2]
#                 (l1, h1) = os[-1]
#                 if l2 > h1:
#                     return ([((lv, os, (am_, b["target"])), memory)], [])
#                 elif not h2 > l1:
#                     return ([((lv, os, (am_, i + 1)), memory)], [])
#                 else:
#                     return (
#                         [
#                             ((lv, os.copy(), (am_, i + 1)), memory.copy()),
#                             ((lv, os.copy(), (am_, b["target"])), memory.copy()),
#                         ],
#                         [],
#                     )
#             case _:
#                 log("unsupported operation", b)
#                 return ([], [("Unsupported", (lv, os, (am_, i)))])

#     def handle_push(self, b, state, log):
#         lv, os, (am_, i) = state
#         v = b["value"]
#         if isinstance(v["value"], int):
#             os.append((v["value"], v["value"]))
#             return [((lv, os, (am_, i + 1)), memory)], []
#         return [((lv, os + [v["value"]], (am_, i + 1)), memory)], []

#     def handle_incr(self, b, state, log) -> []:
#         lv, os, (am_, i) = state
#         (l1, h1) = memory[b["index"]]
#         memory[b["index"]] = (l1 + b["amount"], h1 + b["amount"])
#         return [((lv, os, (am_, i + 1)), memory)], []

#     def handle_ifz(self, b, state, log) -> []:
#         lv, os, (am_, i) = state
#         match b["condition"]:
#             case "le":
#                 (l1, h1) = os[-1]
#                 if l1 > 0:
#                     return ([((lv, os, (am_, i + 1)), memory)], [])
#                 elif h1 < 0:
#                     return ([((lv, os, (am_, b["target"])), memory)], [])
#                 else:
#                     return (
#                         [
#                             ((lv, os.copy(), (am_, i + 1)), memory.copy()),
#                             ((lv, os.copy(), (am_, b["target"])), memory.copy()),
#                         ],
#                         [],
#                     )

#             case _:
#                 log("unsupported operation", b)
#                 return ([], [("Unsupported", (lv, os, (am_, i)))])
