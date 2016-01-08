#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Mickael Bonfill
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# By reading this code you agree not to ridicule the author =)

import os, io, json
from urllib.request import urlopen
from urllib.error import URLError

class Cover:
    def __init__(self, mpdMusicDir, defaultCover):
        self.localDir     = mpdMusicDir
        self.itunesUrl    = "https://itunes.apple.com/search?media=music&entity=album&limit=1&term="
        self.defaultCover = defaultCover

    def getData(self, artist, album, musicFile):

        if musicFile == "":
            return self.defaultCover

        # Search cover locally first
        pathObjs = musicFile.split("/")
        path = self.localDir
        for i in range(len(pathObjs)-1):
            path += "/%s" % (pathObjs[i])
        for f in os.listdir(path):
            if f.endswith("jpeg") or f.endswith("jpg") or f.endswith("png"):
                return "%s/%s" % (path, f)

        # Search cover online
        queryUrl  = self.itunesUrl+artist.replace(" ","+") + "+" + album.replace(" ","+")
        try:
            request = urlopen(queryUrl)
        except URLError:
            return self.defaultCover
        response = json.loads(request.read().decode("utf-8"))
        if response["resultCount"] == 1 and "artworkUrl100" in response["results"][0]:
            coverUrl = response["results"][0]["artworkUrl100"].replace("100x100", "300x300")
            image_request = urlopen(self.coverUrl)
            image_response = image_request.read()
            cover = io.BytesIO(image_response)
            return cover

        # Nothing found, return default theme cover
        return self.defaultCover
