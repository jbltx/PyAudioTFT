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

from UI import UI

__version__="0.1"
__author__="Mickael Bonfill <mickael.bonfill@gmail.com>"
__repository__="https://github.com/jbltx/PyAudioTFT"
__doc__="""PyAudioTFT v%s (c) 2015 Mickael Bonfill

PyAudioTFT is a program that shows infos from MPD server.

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307, USA.

Please send issues on github repo: %s""" % (__version__, __repository__)

# Choose your resolution here :
# -> "240p" for 320x240
# -> "480p" for 640x480
# -> "720p" for 1280x720
# -> "768p" for 1024x768
# -> "1080p" for 1920x1080
__resolution__              = "240p"

# The main color for all labels (r,g,b)
__main_color__              = (255,255,255)

# The main color for all inactive labels (r,g,b)
__inactive_color__          = (10,10,10)

# Font used for the song title
__title_font__              = "Lato-Regular.ttf"

# Font used for other elements
__main_font__               = "Lato-Light.ttf"

# Name of the directory where all resources used by the scripts are located
__resources_dir__           = "resources"

# MPD server host name
__mpd_host__                = "localhost"

# MPD server port number
__mpd_port__                = 6600

# Cover API URL
__c__ = "https://itunes.apple.com/search?media=music&entity=album&limit=1&term="


#
# END OF CONFIGURATION
#

def main():
    application = UI(
        __resolution__, __main_color__, __inactive_color__, __title_font__,
        __main_font__, __resources_dir__, __mpd_host__, __mpd_port__, __c__
    )
    application.load()

if __name__ == "__main__":
    main()
