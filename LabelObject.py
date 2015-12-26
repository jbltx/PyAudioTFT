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

class LabelObject():
    def __init__(self, surface, x, y, endX, speed, idleTime):
        self.surface = surface
        self.x = x
        self.y = y
        self.endX = endX
        self.speed = speed
        self.idleTime = idleTime
        self.alpha = 255
        self.timer_start = 0
        self.timer_end = 0
        self.pos = surface.get_rect().move(x,y)

    def move(self):
        self.timer_start = self.timer_start + 1
        if self.timer_start > self.idleTime:
            if (self.pos[0]+self.pos[2]) > self.endX:
                self.pos = self.pos.move(self.speed, 0)
            elif self.pos[0] < self.x:
                self.timer_end = self.timer_end + 1
                if self.timer_end > self.idleTime:
                    self.alpha = self.alpha - 25
                if self.timer_end > self.idleTime + 11:
                    self.pos = self.surface.get_rect().move(self.x, self.y)
                    self.timer_start = 0
                    self.timer_end = 0
                    self.alpha = 255
        self.surface.set_alpha(self.alpha)
