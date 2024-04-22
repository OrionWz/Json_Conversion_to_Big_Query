import json
from prefect import task, Flow

@task
def read_json_file(file_path):
    """ Reads data from a JSON file """
    with open(file_path, "r") as read_file:
        return json.load(read_file)

@task
def process_data(data):
    """ Processes the data (in this case, just converts it to JSON strings) """
    return [json.dumps(record) for record in data]

@task
def write_json_file(data, file_path):
    """ Writes data to a JSON file """
    with open(file_path, 'w') as write_file:
        for record in data:
            write_file.write(record + '\n')

with Flow("Process JSON File") as flow:
    file_path_in = r"C:\Users\orion\OneDrive\Documents\orion_file.json"
    file_path_out = r"C:\Users\banks\OneDrive\Documents\orion_file.json"

    data = read_json_file(file_path_in)
    processed_data = process_data(data)
    write_json_file(processed_data, file_path_out)

flow.run()


import json

with open(r"C:\Users\banks\OneDrive\Documents\nell_file.json", "r") as read_file:
    data = json.load(read_file)

result = [json.dumps(record) for record in data]
with open(r"C:\Users\banks\OneDrive\Documents\nell_file.json", 'w') as obj:
    for i in result:
        obj.write(i + '\n')

import json 
with open(r"C:\
