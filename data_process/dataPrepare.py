import json
import re
from itertools import chain

root_pth = "./DocRED/"
train_annotated_pth = root_pth + "train_annotated.json"
valid_annotated_pth = root_pth + "dev.json"
train_distant_pth = root_pth + "train_distant.json"
rel_info_pth = root_pth + "rel_info.json"


def import_json(file_pth):
    with open(file_pth, "r") as f:
        data = f.read()
    return json.loads(data)

def process(ss):
    s = " ".join(ss)
    s = s.replace("\"", "")
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s+([.,!?;):])', r'\1', s)
    s = re.sub(r'(")\s+', r'\1', s)
    s = re.sub(r'([.,!?;])(?=\S)', r'\1 ', s)
    s = re.sub(r'(\()(\s+)', r'\1', s)
    s = re.sub(r'\s+(-)\s+', r'\1', s)
    s = re.sub(r'\s+\'', '\'', s)
    return s


instruction = (
    "You are a specialized expert in document-level relation extraction. I need you to comprehend the article I provide, "
    "considering the contextual nuances, to extract the entities and relationships within the text. Please output all "
    "extracted triples in the format 'Entity > Relation > Entity'.")

print(len(instruction.split()))
train_annotated_json = import_json(train_annotated_pth)
valid_annotated_json = import_json(valid_annotated_pth)
rel_info_json = import_json(rel_info_pth)

json_data = []
for contents in valid_annotated_json:
    input = ""
    triplets = "triplets: \n"
    sents = contents.get("sents")
    labels = contents.get("labels")
    vertexSet = contents.get("vertexSet")
    vertexSet = list(chain(*vertexSet))
    name_list = [vts.get("name") for vts in vertexSet]
    entities = "entities: " + ", ".join(name_list) + "\n"
    for sent in sents:
        s = process(sent)
        input += s + " "
    for label in labels:
        relation = rel_info_json.get(label.get("r"))
        head = name_list[label.get("h")]
        tail = name_list[label.get("t")]
        triplets += " > ".join([head, relation, tail]) + "\n"
    triplets = triplets[:-1] + "."
    row_data = {"instruction": instruction, "input": input, "output": triplets}
    json_data.append(row_data)
print(len(json_data))
with open("./RED_VALID.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4, sort_keys=True, ensure_ascii=False)