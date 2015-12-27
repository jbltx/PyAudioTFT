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
import os.path
import pygame
import threading
from mpd import CommandError
from select import select
from MPControl import MPControl
from ItunesCover import ItunesCover
from LabelObject import LabelObject

class UI:
    def __init__(self, resolution, mainColor, inactiveColor, titleFont, mainFont, resourcesDir, mpdHost, mpdPort, coverApiUrl):

        self.__last_played_artist__ = ""
        self.__last_played_album__   = ""
        self.__last_cover_image__ = 0

        r = resolution
        if r != "240p" and r != "480p" and r != "720p" and r != "768p" and r != "1080p":
            print("Error : Wrong resolution configuration, exiting...")
            sys.exit(1)

        if len(mainColor) != 3:
            print("Error : Wrong main color list length, exiting...")
            sys.exit(1)
        else:
            for c in mainColor:
                if c < 0 or c > 255:
                    print("Error : Wrong main color value(s), exiting...")
                    sys.exit(1)

        if len(inactiveColor) != 3:
            print("Error : Wrong inactive color list length, exiting...")
            sys.exit(1)
        else:
            for c in inactiveColor:
                if c < 0 or c > 255:
                    print("Error : Wrong inactive color value(s), exiting...")
                    sys.exit(1)

        if not os.path.isdir(os.path.join(sys.path[0], resourcesDir)):
            print("Error : The resources directory doesn't exist, exiting...")
            sys.exit(1)

        if not os.path.isfile(os.path.join(sys.path[0],resourcesDir,titleFont)):
            print("Error : Font file for title doesn't exist, exiting...")
            sys.exit(1)

        if not os.path.isfile(os.path.join(sys.path[0],resourcesDir,mainFont)):
            print("Error : Main font file doesn't exist, exiting...")
            sys.exit(1)

        if pygame.image.get_extended() == 0:
            print("Error : Can't use extended Image module from PyGame, exiting...")
            sys.exit(1)

        # MPControl initialization
        self.mpcontrol = MPControl(mpdHost,mpdPort)
        self.mpcontrol.update()

        if r == "240p":
            self.factor       = 1
            self.screenWidth  = 320
            self.screenHeight = 240
        if r == "480p":
            self.factor       = 2
            self.screenWidth  = 640
            self.screenHeight = 480
        if r == "720p":
            self.factor       = 3
            self.screenWidth  = 1280
            self.screenHeight = 720
        if r == "768p":
            self.factor       = 3
            self.screenWidth  = 1024
            self.screenHeight = 768
        if r == "1080p":
            self.factor       = 4
            self.screenWidth  = 1920
            self.screenHeight = 1080

        # PyGame initialization
        pygame.display.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(
            (self.screenWidth,self.screenHeight), pygame.FULLSCREEN, 0
        )

        self.mainColor      = mainColor
        self.inactiveColor  = inactiveColor
        self.framerate      = 20
        self.padding        = (16 * self.factor)
        self.titleFontSize  = (25 * self.factor)
        self.artistFontSize = (20 * self.factor)
        self.albumFontSize  = (15 * self.factor)
        self.mainFontSize   = (12 * self.factor)
        self.over           = False
        self.clock          = pygame.time.Clock()
        self.timeProgress   = 0
        self.coverApiUrl    = coverApiUrl

        pygame.font.init()
        self.titleFontSurface = pygame.font.Font(
            os.path.join(sys.path[0],resourcesDir,titleFont), self.titleFontSize
        )
        self.artistFontSurface = pygame.font.Font(
            os.path.join(sys.path[0],resourcesDir,mainFont), self.artistFontSize
        )
        self.albumFontSurface = pygame.font.Font(
            os.path.join(sys.path[0],resourcesDir,mainFont), self.albumFontSize
        )
        self.mainFontSurface = pygame.font.Font(
            os.path.join(sys.path[0],resourcesDir,mainFont), self.mainFontSize
        )

        self.background      = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"background.png")
        ).convert(), (self.screenWidth, self.screenHeight))
        self.defaultCover    = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"cover.png")
        ).convert(), (120 * self.factor,120 * self.factor))
        self.activeRepeat    = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"repeat-active.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.inactiveRepeat  = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"repeat-inactive.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.activeSingle    = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"single-active.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.inactiveSingle  = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"single-inactive.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.activeConsume   = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"consume-active.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.inactiveConsume = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"consume-inactive.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.activeRandom    = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"random-active.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.inactiveRandom  = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"random-inactive.png")
        ).convert_alpha(), (28 * self.factor,28 * self.factor))
        self.playIcon        = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"play.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.pauseIcon       = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"pause.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.stopIcon        = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"stop.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.aacLogo         = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"format-aac.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.wavLogo         = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"format-wav.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.dsdLogo         = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"format-dsd.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.flacLogo        = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"format-flac.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.mp3Logo         = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"format-mp3.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))
        self.oggLogo         = pygame.transform.scale(pygame.image.load(
            os.path.join(sys.path[0],resourcesDir,"format-ogg.png")
        ).convert_alpha(), (45 * self.factor,45 * self.factor))

    def updateUI(self):
        self.timeProgress = 0
        self.label_objects = []
        # Get data from MPControl
        if "time" in self.mpcontrol.infos["status"]:
            totalTimeData = self.mpcontrol.convertTime(
                int(self.mpcontrol.infos["status"]["time"].split(":")[1])
            )
        else:
            totalTimeData = "00:00:00"

        stateData = str(self.mpcontrol.infos["status"]["state"])
        countData = str(self.mpcontrol.infos["status"]["playlistlength"])
        if "pos" in self.mpcontrol.infos["currentsong"]:
            positionData = str(int(self.mpcontrol.infos["currentsong"]["pos"])+1)
        else:
            positionData = "0"
        if "title" in self.mpcontrol.infos["currentsong"]:
            titleData = str(self.mpcontrol.infos["currentsong"]["title"])
            artistData = str(self.mpcontrol.infos["currentsong"]["artist"])
            albumData = str(self.mpcontrol.infos["currentsong"]["album"])
            yearData = str(self.mpcontrol.infos["currentsong"]["date"])[0:4]
            extensionData = self.mpcontrol.infos["currentsong"]["file"].split(".")[-1]
        else:
            titleData = ""
            artistData = ""
            albumData = ""
            yearData = ""
        if "audio" in self.mpcontrol.infos["status"]:
            samplingData = str(self.mpcontrol.infos["status"]["audio"].split(":")[0])
            bitsData = str(self.mpcontrol.infos["status"]["audio"].split(":")[1])
            channelsData = str(self.mpcontrol.infos["status"]["audio"].split(":")[2])
            bitrateData = str(self.mpcontrol.infos["status"]["bitrate"])
        else:
            samplingData = "0"
            bitsData = "0"
            channelsData = "0"
            bitrateData = "0"
        repeatData = int(self.mpcontrol.infos["status"]["repeat"])
        singleData = int(self.mpcontrol.infos["status"]["single"])
        consumeData = int(self.mpcontrol.infos["status"]["consume"])
        randomData = int(self.mpcontrol.infos["status"]["random"])
        volumeData = int(self.mpcontrol.infos["status"]["volume"])

        # Surface creation for each data
        if titleData == "":
            self.cover = self.defaultCover
            self.itunesCover = False
            self.coverThread = False
            self.logo = self.wavLogo
        else:
            if extensionData == "aac":
                self.logo = self.aacLogo
            elif extensionData == "dsd" or extensionData == "dxf":
                self.logo = self.dsdLogo
            elif extensionData == "flac":
                self.logo = self.flacLogo
            elif extensionData == "mp3":
                self.logo = self.mp3Logo
            elif extensionData == "ogg":
                self.logo = self.oggLogo
            else:
                self.logo = self.wavLogo
            if artistData != self.__last_played_artist__ or albumData != self.__last_played_album__:
                self.__last_played_album__ = albumData
                self.__last_played_artist__ = artistData
                self.itunesCover = ItunesCover(artistData, albumData, self.coverApiUrl)
                self.coverThread = threading.Thread(target=self.itunesCover.get_cover, args=(), kwargs={})
                self.coverThread.start()
            else:
                self.cover = self.__last_cover_image__
        self.title = self.titleFontSurface.render(titleData, 0, self.mainColor)
        self.artist = self.artistFontSurface.render(artistData, 0, self.mainColor)
        self.album = self.albumFontSurface.render(
            albumData + " - " + yearData, 0, self.mainColor
        )
        self.bitrate = self.mainFontSurface.render(
            bitrateData + " kbps", 0, self.mainColor
        )
        self.meta = self.mainFontSurface.render(
            channelsData + "ch/" + bitsData + "bits/" + samplingData + "Hz", 0, self.mainColor
        )
        #volume HERE
        if repeatData == 1:
            self.repeat = self.activeRepeat
        else:
            self.repeat = self.inactiveRepeat
        if singleData == 1:
            self.single = self.activeSingle
        else:
            self.single = self.inactiveSingle
        if consumeData == 1:
            self.consume = self.activeConsume
        else:
            self.consume = self.inactiveConsume
        if randomData == 1:
            self.random = self.activeRandom
        else:
            self.random = self.inactiveRandom
        self.playlist = self.mainFontSurface.render(positionData + "/" + countData, 0, self.mainColor)
        self.totalTime = self.mainFontSurface.render(totalTimeData, 0, self.mainColor)
        if stateData == "play":
            self.state = self.playIcon
        elif stateData == "pause":
            self.state = self.pauseIcon
        else:
            self.state = self.stopIcon



        self.label_objects.append(
            LabelObject(
                self.artist,
                self.padding*2+self.factor*120,
                self.padding,
                self.screen.get_width()-self.padding,
                self.framerate*-0.05,
                self.framerate*3
            )
        )
        self.label_objects.append(
            LabelObject(
                self.title,
                self.padding*2+self.factor*120,
                self.padding+self.artist.get_height()-self.factor*2,
                self.screen.get_width()-self.padding,
                self.framerate*-0.05,
                self.framerate*3
            )
        )
        self.label_objects.append(
            LabelObject(
                self.album,
                self.padding*2+self.factor*120,
                self.padding+self.artist.get_height()+self.title.get_height()-self.factor*4,
                self.screen.get_width()-self.padding,
                self.framerate*-0.05,
                self.framerate*3
            )
        )

    def globalUpdate(self):
        self.mpcontrol.update()
        self.updateUI()
        self.mpcontrol.client.send_idle()

    def loop(self):
        canRead = select([self.mpcontrol.client], [], [], 0)[0]
        if canRead:
            result = self.mpcontrol.client.fetch_idle()
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

        self.screen.fill((0,0,0))

        if "time" in self.mpcontrol.infos["status"]:
            currentTimeData = self.mpcontrol.convertTime(
                int(self.mpcontrol.infos["status"]["time"].split(":")[0])+self.timeProgress
            )
            self.ratioTimer = (int(self.mpcontrol.infos["status"]["time"].split(":")[0])+self.timeProgress) / int(self.mpcontrol.infos["status"]["time"].split(":")[1])
        else:
            currentTimeData = "00:00:00"
            self.ratioTimer = 1

        self.currentTime = self.mainFontSurface.render(currentTimeData, 0, self.mainColor)

        if self.mpcontrol.infos["status"]["state"] == "play":
            self.timeProgress = self.timeProgress + (1/self.framerate)

        if not hasattr(self, "cover") or self.cover == 0:
            self.cover = self.defaultCover

        self.screen.blit(self.background, (0,0))

        if self.itunesCover and not self.coverThread.is_alive():
            if self.itunesCover.cover != 0:
                self.cover = pygame.transform.scale(pygame.image.load(self.itunesCover.cover), (120 * self.factor,120 * self.factor))
            else:
                self.cover = self.defaultCover
            self.__last_cover_image__ = self.cover
            self.itunesCover = False
            self.coverThread = False

        self.screen.blit(self.bitrate, (self.cover.get_width()+self.padding*2, 108*self.factor))
        self.screen.blit(self.meta, (self.cover.get_width()+self.padding*2, 122*self.factor))
        self.screen.blit(self.logo, (self.screenWidth-self.padding-self.logo.get_width(), 128*self.factor-self.logo.get_height()))
        self.screen.blit(self.state, (self.padding, ( self.padding+self.cover.get_height()+int((self.screenHeight-self.padding-self.cover.get_height())*0.5)-int(self.state.get_height()*0.5) )))
        self.screen.blit(self.consume, ( self.screenWidth-self.padding-self.consume.get_height(), self.padding*2+self.cover.get_height() ))
        self.screen.blit(self.random, ( self.padding*7+self.state.get_width()+self.repeat.get_width()+self.single.get_width(), self.padding*2+self.cover.get_height() ))
        self.screen.blit(self.single, ( self.padding*4.5+self.state.get_width()+self.repeat.get_width(), self.padding*2+self.cover.get_height() ))
        self.screen.blit(self.repeat, ( self.padding*2+self.state.get_width(), self.padding*2+self.cover.get_height() ))
        self.screen.blit(self.currentTime, ( self.padding*2+self.state.get_width(), self.screenHeight-self.padding*2.5 ))
        self.screen.blit(self.playlist, ( self.padding*2+self.state.get_width()+int((self.screenWidth-(self.padding*2+self.state.get_width()))*0.5)-int(self.playlist.get_width()*0.5), self.screenHeight-self.padding*2.5 ))
        self.screen.blit(self.totalTime, ( self.screenWidth-self.padding-self.totalTime.get_width(), self.screenHeight-self.padding*2.5 ))
        pygame.draw.rect(self.screen, self.mainColor, pygame.Rect(self.padding*2+self.state.get_width(), self.padding*2+self.cover.get_height()+self.repeat.get_height()+self.factor*5, self.screenWidth-(self.padding*3+self.state.get_width()), self.factor*11), 1*self.factor)
        pygame.draw.rect(self.screen, self.mainColor, pygame.Rect(self.padding*2+self.state.get_width(), self.padding*2+self.cover.get_height()+self.repeat.get_height()+self.factor*5, (self.screenWidth-(self.padding*3+self.state.get_width()))*self.ratioTimer, self.factor*11))

        for lo in self.label_objects:
            lo.move()
            labelArea = pygame.Rect(lo.x-lo.pos.x, 0, lo.endX-lo.x, lo.surface.get_height())
            self.screen.blit(lo.surface, (lo.x,lo.y) , area=labelArea )

        self.screen.blit(self.cover, (self.padding,self.padding))

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
