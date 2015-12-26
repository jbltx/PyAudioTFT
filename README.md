# PyAudioTFT
Show Music Player Daemon informations on your TFT screen


![PyAudioTFT Demo Show](http://i.imgur.com/zGYXt6k.png)

---
### What you need
- [Python 3](https://www.python.org/downloads/) (3.5.1 used)
- [PyGame](http://www.pygame.org/download.shtml) with extended Image module (1.9.2 used)
- [Mpd2](https://pypi.python.org/pypi/python-mpd2) Python library
- [MPD](http://www.musicpd.org/download.html) running on one of your machine (locally or not)
- [An Internet connection](https://www.youtube.com/watch?v=dQw4w9WgXcQ) (to get album artworks via iTunes)

### What is customizable
- Interface resolution (in `main.py`)
- Font file/size/color (same...)
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
