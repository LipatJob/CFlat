from pprint import pprint
import re
def parse(testcase: str):
    m = re.findall("\/\*TEST(.+?)\*\/", testcase, re.DOTALL)
    if not m: return

    vals = m[0].strip().split("\n")

    current = 1
    inputs = []
    while current < len(vals) and "output" not in vals[current].lower():
        inputs.append(vals[current])
        current+=1
        
    current += 1
    outputs = []
    while current < len(vals) and "description" not in vals[current].lower():
        outputs.append(vals[current])
        current+=1

    return inputs, outputs

