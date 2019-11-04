import json
import subprocess
from keyboard import Reader
from areena import Areena

with open('config.json', 'r') as f:
    settings = json.load(f)

print(settings)

def call(*args):
    print("Calling chromecast: %s" % " ".join(args))
    subprocess.call([settings['chromecastCliPath'], '-H', settings['chromecastIP']] + list(args))

call('status')

areena = Areena(settings['areena_key'])

while True:
    try:
        with Reader('/dev/input/event0') as reader:
            line = reader.read()
            found = False
            for mapping in settings['cardMappings']:
                if mapping['code'] == line:
                    found = True
                    call('stop')
                    if 'url' in mapping:
                        if mapping['url'] == 'STOP':
                            print("Stopping")
                        else:
                            print("Playing %s" % mapping['name'])
                            call('play', mapping['url'])
                    elif 'areena_series' in mapping:
                        if mapping['areena_series_type'] == 'latest':
                            call('play', areena.get_series_url_latest(mapping['areena_series']))
                        elif mapping['areena_series_type'] == 'random':
                            call('play', areena.get_series_url_random(mapping['areena_series']))
                    elif 'areena_program' in mapping:
                        call('play', areena.get_program_url(mapping['areena_program']))

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
