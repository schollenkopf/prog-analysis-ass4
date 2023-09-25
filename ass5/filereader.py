from pathlib import Path
import json

dc = Path("/Users/paulnelsonbecker/Documents/Uni/Masters/se1/program-analysis/course-02242-examples")

classes = {}
for f in dc.glob("**/*.json"):
    with open(f) as p:
        doc = json.load(p)
        classes[doc["name"]] = doc

methods = {}
for cls in classes.values():
    for m in cls["methods"]:        
        methods[(cls["name"],m["name"])] = m

def find_method(am):
    return methods[(am)]
        
def print_bytecode(am):
    m = find_method(am)
    assert m is not None
    print(m["code"]["bytecode"])

print_bytecode(("dtu/compute/exec/Simple","noop"))