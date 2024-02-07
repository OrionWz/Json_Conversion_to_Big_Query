import requests
import json


def fetch_api_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def create_json(data):
    return json.dumps(data, indent=2)


def write_json_to_file(json_data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_data)


api_url = 'https://api.sampleapis.com/switch/games'
data = fetch_api_data(api_url)

if data:
    json_data = create_json(data)
    write_json_to_file(json_data, 'output.json')
else:
    print("Failed to fetch data from the API")

print(data)
