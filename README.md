# PyAudioTFT
Show Music Player Daemon informations on your TFT screen


![PyAudioTFT Demo Show](http://i.imgur.com/zGYXt6k.png)

---
### What you need
- Python 3 (3.5.1 used)
- PyGame with extended Image module (1.9.2 used)
- Mpd2 Python library
- MPD running on one of your machine (locally or not)
- An Internet connection (to get album artworks via iTunes)

### What is customizable
- Interface resolution
- Font file/size/color
- All icons and background (just overwrite present files in resources directory)

### How it works
You just need to set the host name or IP address where your MPD is located, and its port in `main.py` file:
```
__mpd_host__ = "localhost"
__mpd_port__ = 6600
```
Then you can launch the script:
```
$ python3 main.py
```

### Contribute
Don't hesitate to fork this project and send back some pull requests !
