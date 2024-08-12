import json

with open('data/settings.json', 'r') as f:
    text_data = f.read()
    settings = json.loads(text_data)


