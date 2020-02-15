import json
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

from random import randrange

from keyboard import Reader
from areena import Areena
from dlna import parse_dlna

with open('config.json', 'r') as f:
    settings = json.load(f)

cleaned = []

for title, url in parse_dlna().items():
    for mapping in settings['cardMappings']:
        if mapping.get('dlna_title', '') == title:
            print("Found new url for %s: %s" % (title, url))
            mapping['url'] = url
        elif title in mapping.get('dlna_titles', []):
            if mapping['name'] not in cleaned:
                cleaned.append(mapping['name'])
                mapping['series_urls'] = []
            print("Found new url for %s: %s" % (title, url))
            mapping['series_urls'].append(url)
        elif title.startswith(mapping.get('dlna_series', '1234576').split('*')[0]):
            if mapping['name'] not in cleaned:
                cleaned.append(mapping['name'])
                mapping['series_urls'] = []
            print("Found new url for %s: %s" % (title, url))
            mapping['series_urls'].append(url)

print(settings)

currentmapping = ""


chromecasts = pychromecast.get_chromecasts()
cast = pychromecast.Chromecast(settings['chromecastIP'])
cast.wait()


def handle_mapping(mapping):
    global currentmapping
    if 'url' in mapping and mapping['url'] == 'STOP':
        print("Stopping")
        currentmapping = ""
        cast.media_controller.stop()
        return

    if (mapping['code'] == currentmapping and mapping.get('series_type', '') != 'random' and
            'youtube_id' not in mapping):
        print("Not restarting same file")
        return

    currentmapping = mapping['code']

    if 'url' in mapping:
        print("Playing %s" % mapping['name'])
        cast.play_media(mapping['url'], 'video/mp4')
        return
    
    if 'series_urls' in mapping and mapping.get('series_type', '') == 'random':
        print("Playing %s (random)" % mapping['name'])
        index = randrange(len(mapping['series_urls']) - 1)
        cast.play_media(mapping['series_urls'][index], 'video/mp4')
        return

    if 'youtube_id' in mapping:
        print('Playing youtube id %s' % mapping['youtube_id'])
        yt = YouTubeController()
        cast.register_handler(yt)
        yt.play_video(mapping['youtube_id'])
        return

    # Stop here for better UX, since areena stuff has some delay with URL fetching
    cast.media_controller.stop()
    if 'areena_series' in mapping:
        if mapping['series_type'] == 'latest':
            cast.play_media(areena.get_series_url_latest(mapping['areena_series']), 'video/mp4')
        elif mapping['series_type'] == 'random':
            cast.play_media(areena.get_series_url_random(mapping['areena_series']), 'video/mp4')
    elif 'areena_program' in mapping:
        cast.play_media(areena.get_program_url(mapping['areena_program']), 'video/mp4')


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
                    json.dump(settings, f, indent=4, sort_keys=True)

                print(settings['cardMappings'][new])
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        continue
