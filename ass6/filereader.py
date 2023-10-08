from pathlib import Path
import json

dc = Path(
    "/Users/paulnelsonbecker/Documents/Uni/Masters/se1/program-analysis/course-02242-examples"
)
# dc = Path("/Users/enricotuda/Desktop/course-02242-examples")

classes = {}
# Here I create a json file
for f in dc.glob("**/*.json"):  # Open every json file
    with open(f) as p:
        doc = json.load(p)  # doc = text of the json
        classes[doc["name"]] = doc  # {NAMEjson1:....,NAMEjson2:..... ecc}
        # classes[method] -->


methods = (
    {}
)  # dictionary that will use a tuple (of dictionaries) as key and values method.json
# Here i create the map methods and through a for cicle i collect al the methods in that map
for cls in classes.values():
    for m in cls["methods"]:
        methods[(cls["name"], m["name"])] = m  # className, methodName


def find_method(am):
    return methods[(am)]  # I give the (fileName,methodName) and it gives me the metohod


def print_bytecode(am):
    m = find_method(am)
    assert m is not None
    print(m["code"]["bytecode"])


print_bytecode(("dtu/compute/exec/Simple", "noop"))
