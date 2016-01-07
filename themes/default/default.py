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
        latoLight            = os.path.join(self.resourcesDir,self.mainFont)
        latoRegular          = os.path.join(self.resourcesDir,self.titleFont)
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
        self.currentTimeArea = pygame.Surface((sw*0.2, sh*0.075),pygame.SRCALPHA)
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

    def updateUI(self,infos,idleTime):

        if "time" in infos["status"]:
            currentTimeData = self.convertTime(int(infos["status"]["time"].split(":")[0])+int(idleTime))
            totalTimeData = self.convertTime(int(infos["status"]["time"].split(":")[1]))
            ratioTimeData = (int(infos["status"]["time"].split(":")[0])+int(idleTime))/int(infos["status"]["time"].split(":")[1])
        else:
            currentTimeData = "00:00:00"
            totalTimeData = "00:00:00"
            ratioTimeData = 1
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
            extensionData = "wav"
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

        # CLEAN ALL ELEMENTS
        self.coverArea.fill((0,0,0,0))
        self.artistArea.fill((0,0,0,0))
        self.titleArea.fill((0,0,0,0))
        self.albumArea.fill((0,0,0,0))
        self.bitrateArea.fill((0,0,0,0))
        self.metaArea.fill((0,0,0,0))
        self.logoArea.fill((0,0,0,0))
        self.repeatArea.fill((0,0,0,0))
        self.singleArea.fill((0,0,0,0))
        self.randomArea.fill((0,0,0,0))
        self.consumeArea.fill((0,0,0,0))
        self.stateArea.fill((0,0,0,0))
        self.currentTimeArea.fill((0,0,0,0))
        self.playlistArea.fill((0,0,0,0))
        self.volumeArea.fill((0,0,0,0))
        self.totalTimeArea.fill((0,0,0,0))
        self.timingArea.fill((0,0,0,0))

        # Update Background Image
        bg = pygame.transform.scale(pygame.image.load(os.path.join(self.resourcesDir,"background.png")).convert(), (self.sw, self.sh))

        # Update Cover Image
        coverFile = Cover(artistData,albumData)
        cover = pygame.image.load(coverFile.getData()).convert()
        cover = pygame.transform.scale(cover, (int(self.sh*0.5), int(self.sh*0.5)))
        self.coverArea.blit(cover, (0,0))

        # Update Artist Text
        artist = self.artistFont.render(artistData, 0, self.mainColor)
        self.artistArea.blit(artist, (0,-2))

        # Update Title Text
        title = self.titleFont.render(titleData, 0, self.mainColor)
        self.titleArea.blit(title, (0,-2))

        # Update Album Text
        album = self.albumFont.render(albumData, 0, self.mainColor)
        self.albumArea.blit(album, (0,-2))

        # Update Format Logo Image
        logoFile = self.getFormatLogo(extensionData)
        logo = pygame.image.load(logoFile).convert_alpha()
        logo = pygame.transform.scale(logo,(self.logoArea.get_width(),self.logoArea.get_height()))
        self.logoArea.blit(logo, (0,0))

        # Update Bitrate Text
        bitrate = self.bitrateFont.render(bitrateData + " kbps", 0, self.mainColor)
        self.bitrateArea.blit(bitrate, (0,-2))

        # Update Meta Text
        meta = self.metaFont.render("%sch/%sbits/%sHz" % (channelsData, bitsData, samplingData), 0, self.mainColor)
        self.metaArea.blit(meta, (0,-2))

        # Update Icons Image
        repeatFile = self.getIconByState("repeat", repeatData)
        repeat = pygame.image.load(repeatFile).convert_alpha()
        repeat = pygame.transform.scale(repeat,(int(self.sh*0.18),int(self.sh*0.18)))
        self.repeatArea.blit(repeat, (0,0))

        singleFile = self.getIconByState("single", singleData)
        single = pygame.image.load(singleFile).convert_alpha()
        single = pygame.transform.scale(single,(int(self.sh*0.18),int(self.sh*0.18)))
        self.singleArea.blit(single, (0,0))

        randomFile = self.getIconByState("random", randomData)
        random = pygame.image.load(randomFile).convert_alpha()
        random = pygame.transform.scale(random,(int(self.sh*0.18),int(self.sh*0.18)))
        self.randomArea.blit(random, (0,0))

        consumeFile = self.getIconByState("consume", consumeData)
        consume = pygame.image.load(consumeFile).convert_alpha()
        consume = pygame.transform.scale(consume,(int(self.sh*0.18),int(self.sh*0.18)))
        self.consumeArea.blit(consume, (0,0))

        # Update Playback Icon Image
        stateFile = self.getStateIcon(stateData)
        state = pygame.image.load(stateFile).convert_alpha()
        state = pygame.transform.scale(state,(int(self.sh*0.18),int(self.sh*0.18)))
        self.stateArea.blit(state, (0,0))

        # Update Current Time Text
        currentTime = self.timeFont.render(currentTimeData,0, self.mainColor)
        self.currentTimeArea.blit(currentTime, (0,-2))

        # Update Playlist Text
        playlist = self.timeFont.render("%s/%s" % (positionData, countData),0, self.mainColor)
        self.playlistArea.blit(playlist, (0,-2))

        # Update Volume Text
        volume = self.timeFont.render(volumeData,0,self.mainColor)
        self.volumeArea.blit(volume, (0,-2))

        # Update Total Time Text
        totalTime = self.timeFont.render(totalTimeData,0,self.mainColor)
        self.totalTimeArea.blit(totalTime, (self.totalTimeArea.get_width()-totalTime.get_width(),-2))

        # Update Time Bar
        timingOutline = pygame.Rect(0,0,self.timingArea.get_width(),self.timingArea.get_height())
        pygame.draw.rect(self.timingArea, self.mainColor, timingOutline, 2)
        timeScale = (self.timingArea.get_width()-12)*ratioTimeData
        timing = pygame.Rect(0,0,timeScale,self.timingArea.get_height())
        pygame.draw.rect(self.timingArea, self.mainColor, timing)


        # BLIT ELEMENTS
        self.screen.blit(bg, (0,0))
        self.screen.blit(self.coverArea, (self.padding,self.padding))
        self.screen.blit(self.artistArea, (self.padding*2+self.sh*0.5, self.padding))
        self.screen.blit(self.titleArea, (self.padding*2+self.sh*0.5, self.padding+self.sh*0.08))
        self.screen.blit(self.albumArea, (self.padding*2+self.sh*0.5, self.padding+self.sh*0.19))
        self.screen.blit(self.logoArea, (self.sw-self.padding-self.logoArea.get_width(), self.sh*0.32))
        self.screen.blit(self.bitrateArea, (self.padding*2+self.sh*0.5, self.sh*0.40))
        self.screen.blit(self.metaArea, (self.padding*2+self.sh*0.5, self.sh*0.48))
        self.screen.blit(self.repeatArea, (self.padding,self.padding*1.5+self.sh*0.5))
        self.screen.blit(self.singleArea, (self.sw*0.3, self.padding*1.5+self.sh*0.5))
        self.screen.blit(self.randomArea, (self.sw*0.7-self.sh*0.18, self.padding*1.5+self.sh*0.5))
        self.screen.blit(self.consumeArea, (self.sw-self.padding-self.sh*0.18,self.padding*1.5+self.sh*0.5))
        self.screen.blit(self.stateArea, (self.padding, self.sh-self.padding-self.sh*0.18))
        self.screen.blit(self.currentTimeArea, (self.padding+self.sh*0.2, self.sh-self.padding-self.sh*0.17))
        self.screen.blit(self.playlistArea, (self.padding+self.sw*0.15+self.sh*0.3, self.sh-self.padding-self.sh*0.17))
        self.screen.blit(self.volumeArea, (self.padding+self.sw*0.33+self.sh*0.3, self.sh-self.padding-self.sh*0.17))
        self.screen.blit(self.totalTimeArea, (self.sw-self.padding-self.sw*0.2, self.sh-self.padding-self.sh*0.17))
        self.screen.blit(self.timingArea, (self.padding+self.sh*0.2,self.sh-self.padding-self.sh*0.08))

    def getFormatLogo(self, extension):
        return os.path.join(self.resourcesDir,"format-%s.png" % (extension))

    def getIconByState(self,iconName,isActive):
        if isActive == 1:
            state = "active"
        else:
            state = "inactive"
        return os.path.join(self.resourcesDir,"%s-%s.png" % (iconName,state))

    def getStateIcon(self,state):
        return os.path.join(self.resourcesDir,"%s.png" % (state))

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
