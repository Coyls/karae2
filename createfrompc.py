import json


f = open("./db/plants.json")
data = json.load(f)
print(data)