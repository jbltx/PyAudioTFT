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

import io
import json
from urllib.request import urlopen

class ItunesCover:
    def __init__(self, artist, album, url):
        self.queryUrl = url+artist.replace(" ","+") + "+" + album.replace(" ","+")
        self.coverUrl = ""
        self.cover = 0

    def get_cover(self):
        request = urlopen(self.queryUrl)
        response = json.loads(request.read().decode("utf-8"))
        if response["resultCount"] == 1 and "artworkUrl100" in response["results"][0]:
            self.coverUrl = response["results"][0]["artworkUrl100"].replace("100x100", "300x300")
            image_request = urlopen(self.coverUrl)
            image_response = image_request.read()
            self.cover = io.BytesIO(image_response)
        return self.cover
