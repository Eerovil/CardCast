import json
import subprocess
from reader import Reader

with open('config.json', 'r') as f:
    settings = json.load(f)

print(settings)

def call(*args):
    subprocess.call([settings['chromecastCliPath'], '-H', settings['chromecastIP']] + list(args))

call('status')

with Reader(1, 1) as reader:
    reader.read()
