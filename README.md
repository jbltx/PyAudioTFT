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
- You can develop your own interface by creating a new theme in the `themes` directory
- All default icons and background can be overwritten in the `resources` directory

### How it works
You just need to set the host name or IP address where your MPD is located, its port and your mpd music directory path in `main.py` file:
```python
__mpd_host__ = "localhost"
__mpd_port__ = 6600
__mpd_music_dir__ = "/path/to/your/mpd/music/dir"
__theme__    = "default"
__fps__      = 12
```
Then you can launch the script:
```bash
$ python3 main.py
```

### Available shortcuts
- Play/Pause : <kbd>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</kbd>
- Stop : <kbd>s</kbd>
- Next Song : <kbd>→</kbd>
- Previous Song : <kbd>←</kbd>
- Volume Up : <kbd>↑</kbd>
- Volume Down : <kbd>↓</kbd>
- Toggle Repeat : <kbd>l</kbd>
- Toggle Single : <kbd>o</kbd>
- Toggle Random : <kbd>r</kbd>
- Toggle Consume : <kbd>c</kbd>
- Close Application : <kbd>Esc</kbd>

### Contribute
Don't hesitate to fork this project and send back some pull requests !
