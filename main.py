import json

with open(r"C:\Users\banks\OneDrive\Documents\nell_file.json", "r") as read_file:
    data = json.load(read_file)

result = [json.dumps(record) for record in data]
with open(r"C:\Users\banks\OneDrive\Documents\nell_file.json", 'w') as obj:
    for i in result:
        obj.write(i + '\n')
