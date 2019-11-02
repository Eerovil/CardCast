import json

with open('config.json', 'r') as f:
    settings = json.load(f)

print(settings)
