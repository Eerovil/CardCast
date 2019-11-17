import json
import subprocess
from random import randrange

from keyboard import Reader
from areena import Areena

with open('config.json', 'r') as f:
    settings = json.load(f)


print(settings)

currentmapping = ""

def call(*args):
    print("Calling chromecast: %s" % " ".join(args))
    subprocess.call([settings['chromecastCliPath'], '-H', settings['chromecastIP']] + list(args))

def handle_mapping(mapping):
    global currentmapping
    if 'url' in mapping and mapping['url'] == 'STOP':
        print("Stopping")
        currentmapping = ""
        call('stop')
        return

    if mapping['code'] == currentmapping and mapping.get('series_type', '') != 'random':
        print("Not restarting same file")
        return

    currentmapping = mapping['code']

    if 'url' in mapping:
        print("Playing %s" % mapping['name'])
        call('play', mapping['url'])
        return
    
    if 'series_urls' in mapping and mapping.get('series_type', '') == 'random':
        print("Playing %s (random)" % mapping['name'])
        index = randrange(len(mapping['series_urls']) - 1)
        call('play', mapping['series_urls'][index])
        return

    # Stop here for better UX, since areena stuff has some delay with URL fetching
    call('stop')
    if 'areena_series' in mapping:
        if mapping['series_type'] == 'latest':
            call('play', areena.get_series_url_latest(mapping['areena_series']))
        elif mapping['series_type'] == 'random':
            call('play', areena.get_series_url_random(mapping['areena_series']))
    elif 'areena_program' in mapping:
        call('play', areena.get_program_url(mapping['areena_program']))

areena = Areena(settings['areena_key'])

while True:
    try:
        with Reader('/dev/input/event0') as reader:
            line = reader.read()
            found = False
            for mapping in settings['cardMappings']:
                if mapping['code'] == line:
                    found = True
                    handle_mapping(mapping)

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
