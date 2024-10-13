import json
import re

# with open("./alpaca_en_demo.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
#
# print(data)
#
# with open("./RED.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
#
# print(len(data))

with open("./DocRED/rel_info.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data.values())
