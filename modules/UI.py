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

import sys, os, pygame, threading
from pydoc               import locate
from mpd                 import CommandError
from select              import select
from modules.MPControl   import MPControl

class UI:
    def __init__(self, mpdHost, mpdPort, themeName, fps):

        Theme = locate('themes.'+themeName+'.'+themeName+'.Theme')

        self.__last_played_artist__    = ""
        self.__last_played_album__     = ""
        self.__last_cover_image__      = 0
        self.mpdHost                   = mpdHost
        self.mpdPort                   = mpdPort
        self.themeName                 = themeName
        self.framerate                 = fps
        self.over                      = False
        self.clock                     = pygame.time.Clock()
        self.mpcontrol                 = MPControl(mpdHost,mpdPort)
        self.mpcontrol.update()
        pygame.display.init()
        pygame.mouse.set_visible(False)
        self.screen                    = pygame.display.set_mode((320,240), pygame.FULLSCREEN, 0)
        self.theme                     = Theme(self.screen)
        self.timeProgress              = 0

    def globalUpdate(self):
        self.mpcontrol.update()
        self.theme.updateUI(self.mpcontrol.infos,self.timeProgress)
        self.mpcontrol.client.send_idle()

    def loop(self):
        canRead = select([self.mpcontrol.client], [], [], 0)[0]
        if canRead:
            result = self.mpcontrol.client.fetch_idle()
            self.timeProgress = 0
            self.globalUpdate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.over = True
                else:
                    try:
                        self.mpcontrol.client.noidle()
                    except CommandError:
                        pass
                    self.mpcontrol.send(event.key)
                    self.mpcontrol.client.send_idle()

        if self.mpcontrol.infos["status"]["state"] == "play":
            self.timeProgress = self.timeProgress + (1/self.framerate)
            self.theme.updateUI(self.mpcontrol.infos,self.timeProgress)
        pygame.display.update()
        self.clock.tick(self.framerate)

    def load (self):
        self.globalUpdate()
        while not self.over:
            self.loop()
        try:
            self.mpcontrol.client.noidle()
        except CommandError:
            pass
        self.mpcontrol.client.close()
        self.mpcontrol.client.disconnect()
        pygame.quit()
        sys.exit(0)
