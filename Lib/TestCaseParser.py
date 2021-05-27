from pprint import pprint

def parse(values: str):
    files = []
    inputs = []
    outputs = []
    values = values.split(">>end")[:-1]
    for test_case in values:
        vals = list(test_case.strip().split("\n"))

        file_name = vals[1].replace(">>","")

        current = 3

        current_inputs = []
        while current < len(vals) and ">>output" not in vals[current]:
            current_inputs.append(vals[current])
            current+=1
            
        current+=1
        current_ouputs = []
        while current < len(vals) and ">>end" not in vals[current]:
            current_ouputs.append(vals[current]+"\n")
            current+=1

        files.append(file_name)
        inputs.append(current_inputs)
        outputs.append("".join(current_ouputs))


    return files, inputs, outputs
