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

import sys
import socket
import pygame
import math
from mpd import MPDClient

class MPControl:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = MPDClient()
        if not self.tryConnection():
            print("Unable to connect to MPD, exiting...")
            sys.exit(1)
        self.infos = {'status':{}, 'currentsong': {} }

    def send(self, key):
        if key == pygame.K_SPACE:
            if self.infos["status"]["state"] == "play":
                self.client.pause()
            else:
                self.client.play()
        if key == pygame.K_r:
            if (self.client.status()["random"] == "1"):
                self.client.random(0)
            else:
                self.client.random(1)
        if key == pygame.K_s:
            self.client.stop()
        if key == pygame.K_l:
            if (self.client.status()["repeat"] == "1"):
                self.client.repeat(0)
            else:
                self.client.repeat(1)
        if key == pygame.K_c:
            if (self.client.status()["consume"] == "1"):
                self.client.consume(0)
            else:
                self.client.consume(1)
        if key == pygame.K_o:
            if (self.client.status()["single"] == "1"):
                self.client.single(0)
            else:
                self.client.single(1)
        if key == pygame.K_RIGHT:
            self.client.next()
        if key == pygame.K_LEFT:
            self.client.previous()
        if key == pygame.K_UP and int(self.infos["status"]["volume"]) < 100:
            self.client.setvol(int(self.infos["status"]["volume"]) + 5)
        if key == pygame.K_DOWN and int(self.infos["status"]["volume"]) > 0:
            self.client.setvol(int(self.infos["status"]["volume"]) - 5)

    def convertTime(self, _seconds):
        hourMod = divmod(_seconds, 3600)
        minMod = divmod(hourMod[1], 60)
        hours = hourMod[0]
        minutes = minMod[0]
        seconds = minMod[1]
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def tryConnection(self):
        try:
            self.client.connect(self.host, self.port)
        except socket.error:
            return False
        return True

    def update(self):
        self.infos["status"] = self.client.status()
        self.infos["currentsong"] = self.client.currentsong()
