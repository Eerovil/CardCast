# CardCast
Use a USB card reader to cast videos to your chromecast

Example config.json

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
            "name": "Cars",
            "code": "0004186222"
        },
    ],
    "chromecastCliPath": "node_modules/.bin/chromecast",
    "chromecastIP": "192.168.100.18"
}
```
