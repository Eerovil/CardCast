# CardCast

![](https://i.imgur.com/M6py7pS.png?1)

Use a USB card reader to cast videos to your chromecast

Currently three ways of casting are supported:

1. Casting media urls
   - Supported
     - Anything with a straight url to the file.
     - YLE Areena media IDs
     - DLNA Server series/movie titles for auto-updating URLs
2. Casting via native chromcast applications using the pychromecast library
   - Supported:
     - Youtube
3. Casting via an extra android device using remote control
   - Supported:
     - Netflix

Example config.json

- `code` is the code your card reader will input (It should be detected as a keyboard input device)
- `dlna_title` is used to update any changed urls using a upnp-client on restart
- `inputDevice` is usually `/dev/input/event0`. Check it by disconnecting your reader, running `ls -l /dev/input`, then connecting it and running `ls -l /dev/input` again. This way you can see which device is your reader.,
- `dlnaServer` The DLNA server ip:port. Only one is currently supported.
- Others should be more or less self-explainatory

```
{
    "cardMappings": [
        {
            "url": "STOP",
            "name": "STOP",
            "code": ""
        },
        {
            "url": "http://192.168.100.20:32469/object/009adf40388ace12afbb/file.mp4",
            "dlna_title": "Cars",
            "name": "Cars",
            "code": "0004186222"
        },
        {
            "code": "0004244721",
            "name": "Skibidi",
            "youtube_id": "mDFBTdToRmw"
        },
        {
            "areena_series": "1-3371178",
            "code": "0004189213",
            "name": "Pikku Kakkonen",
            "series_type": "latest"
        },
        {
            "code": "0004119880",
            "dlna_series": "Muumilaakson tarinoita*",
            "name": "Muumilaakson Tarinoita",
            "series_type": "random",
            "series_urls": [
                "http://192.168.100.20:8200/MediaItems/254.mp4",
                "http://192.168.100.20:8200/MediaItems/207.mp4",
                "http://192.168.100.20:8200/MediaItems/240.mp4"
            ]
        }
    ],
    "chromecastIP": "192.168.100.18",
    "chromecastName": "Living Room Chromecast",
    "inputDevice": "/dev/input/event0",
    "dlnaServer": "127.0.0.1:8200"
}
```
