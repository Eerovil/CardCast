import json
import subprocess
from keyboard import Reader

with open('config.json', 'r') as f:
    settings = json.load(f)

print(settings)

def call(*args):
    print("Calling chromecast: %s" % " ".join(args))
    subprocess.call([settings['chromecastCliPath'], '-H', settings['chromecastIP']] + list(args))

call('status')

while True:
    try:
        with Reader('/dev/input/event0') as reader:
            line = reader.read()
            found = False
            for mapping in settings['cardMappings']:
                if mapping['code'] == line:
                    found = True
                    if mapping['url'] == 'STOP':
                        print("Stopping")
                        call('stop', mapping['url'])
                    else:
                        print("Playing %s" % mapping['name'])
                        call('play', mapping['url'])

            if not found:
                print("No mapping found for code %s" % line)
                for i in range(len(settings['cardMappings'])):
                    print("%i: %s" % (i, settings['cardMappings'][i]))
                new = int(input("Select new mapping"))
                settings['cardMappings'][new]['code'] = line
                with open('config.json', 'w') as f:
                    json.dump(settings, f)

                print(settings['cardMappings'][new])
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        continue
