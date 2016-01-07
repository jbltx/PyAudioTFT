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

import sys, os, pygame, math
from modules.Cover import Cover

class Theme:
    def __init__(self, screen):
        self.themeName      = "default"
        self.mainColor      = (255,255,255)
        self.inactiveColor  = (10,10,10)
        self.titleFont      = "Lato-Regular.ttf"
        self.mainFont       = "Lato-Light.ttf"
        self.screen         = screen
        self.sw             = screen.get_width()
        self.sh             = screen.get_height()
        self.padding        = int(self.sh*0.05)
        self.themeDir       = os.path.join(sys.path[0],"themes",self.themeName)
        self.resourcesDir   = os.path.join(self.themeDir,"resources")

        self.checkTheme()

        pygame.font.init()
        sh                   = self.sh
        sw                   = self.sw
        padding              = self.padding
        self.coverArea       = pygame.Surface((sh*0.5, sh*0.5))
        self.artistArea      = pygame.Surface((sw-sh*0.5-padding*3, sh*0.07),pygame.SRCALPHA)
        self.artistFont      = pygame.font.Font(latoLight,int(self.artistArea.get_height()*0.9))
        self.titleArea       = pygame.Surface((sw-sh*0.5-padding*3, sh*0.1),pygame.SRCALPHA)
        self.titleFont       = pygame.font.Font(latoRegular,int(self.titleArea.get_height()*0.9))
        self.albumArea       = pygame.Surface((sw-sh*0.5-padding*3, sh*0.07),pygame.SRCALPHA)
        self.albumFont       = pygame.font.Font(latoLight,int(self.albumArea.get_height()*0.9))
        self.bitrateArea     = pygame.Surface((sw-padding*4-sh*0.72,sh*0.07),pygame.SRCALPHA)
        self.bitrateFont     = pygame.font.Font(latoLight,int(self.bitrateArea.get_height()*0.9))
        self.metaArea        = pygame.Surface((sw-padding*4-sh*0.72,sh*0.07),pygame.SRCALPHA)
        self.metaFont        = pygame.font.Font(latoLight,int(self.metaArea.get_height()*0.9))
        self.logoArea        = pygame.Surface((sh*0.23,sh*0.23),pygame.SRCALPHA)
        self.repeatArea      = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
        self.singleArea      = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
        self.randomArea      = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
        self.consumeArea     = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
        self.stateArea       = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
        self.currentTimeArea = pygame.Surface((sw*0.2,sh*0.075),pygame.SRCALPHA)
        self.timeFont        = pygame.font.Font(latoLight,int(self.currentTimeArea.get_height()*0.8))
        self.playlistArea    = pygame.Surface((sw*0.15,sh*0.075),pygame.SRCALPHA)
        self.volumeArea      = pygame.Surface((sw*0.13,sh*0.075),pygame.SRCALPHA)
        self.totalTimeArea   = pygame.Surface((sw*0.2,sh*0.075),pygame.SRCALPHA)
        self.timingArea      = pygame.Surface((sw-padding*2-sh*0.2, sh*0.06),pygame.SRCALPHA)

    def convertTime(self, _seconds):
        hourMod = divmod(_seconds, 3600)
        minMod = divmod(hourMod[1], 60)
        hours = hourMod[0]
        minutes = minMod[0]
        seconds = minMod[1]
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def updateUI(self,infos):
        self.timeProgress = 0

        if "time" in infos["status"]:
            totalTimeData = self.convertTime(int(infos["status"]["time"].split(":")[1]))
        else:
            totalTimeData = "00:00:00"
        stateData         = str(infos["status"]["state"])
        countData         = str(infos["status"]["playlistlength"])
        if "pos" in infos["currentsong"]:
            positionData  = str(int(infos["currentsong"]["pos"])+1)
        else:
            positionData  = "0"
        if "title" in infos["currentsong"]:
            titleData     = str(infos["currentsong"]["title"])
            artistData    = str(infos["currentsong"]["artist"])
            albumData     = str(infos["currentsong"]["album"])
            yearData      = str(infos["currentsong"]["date"])[0:4]
            extensionData = infos["currentsong"]["file"].split(".")[-1]
        else:
            titleData     = ""
            artistData    = ""
            albumData     = ""
            yearData      = ""
        if "audio" in infos["status"]:
            samplingData  = str(infos["status"]["audio"].split(":")[0])
            bitsData      = str(infos["status"]["audio"].split(":")[1])
            channelsData  = str(infos["status"]["audio"].split(":")[2])
            bitrateData   = str(infos["status"]["bitrate"])
        else:
            samplingData  = "0"
            bitsData      = "0"
            channelsData  = "0"
            bitrateData   = "0"
        repeatData        = int(infos["status"]["repeat"])
        singleData        = int(infos["status"]["single"])
        consumeData       = int(infos["status"]["consume"])
        randomData        = int(infos["status"]["random"])
        volumeData        = str(infos["status"]["volume"])+"%"

        # Update Background Image
        bg = pygame.transform.scale(pygame.image.load(os.path.join(self.resourcesDir,"background.png")).convert(), (self.sw, self.sh))
        self.screen.blit(bg, (0,0))

        # Update Cover Image
        coverFile = Cover(artistData,albumData)
        cover = pygame.image.load(coverFile).convert()
        cover = pygame.transform.scale(cover, (int(self.sh*0.5), int(self.sh*0.5)))
        self.coverArea.blit(cover, (0,0))

        # Update Artist Text
        

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



    def checkTheme(self):
        if len(self.mainColor) != 3:
            print("Error : Wrong main color list length, exiting...")
            sys.exit(1)
        else:
            for c in self.mainColor:
                if c < 0 or c > 255:
                    print("Error : Wrong main color value(s), exiting...")
                    sys.exit(1)

        if len(self.inactiveColor) != 3:
            print("Error : Wrong inactive color list length, exiting...")
            sys.exit(1)
        else:
            for c in self.inactiveColor:
                if c < 0 or c > 255:
                    print("Error : Wrong inactive color value(s), exiting...")
                    sys.exit(1)

        if not os.path.isdir(self.resourcesDir):
            print("Error : The resources directory doesn't exist, exiting...")
            sys.exit(1)

        if not os.path.isfile(os.path.join(self.resourcesDir,self.titleFont)):
            print("Error : Font file for title doesn't exist, exiting...")
            sys.exit(1)

        if not os.path.isfile(os.path.join(self.resourcesDir,self.mainFont)):
            print("Error : Main font file doesn't exist, exiting...")
            sys.exit(1)

        if pygame.image.get_extended() == 0:
            print("Error : Can't use Image module from PyGame, exiting...")
            sys.exit(1)
