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

from modules.UI import UI
import sys

__version__="1.0"
__author__="Mickael Bonfill <mickael.bonfill@gmail.com>"
__repository__="https://github.com/jbltx/PyAudioTFT"
__doc__="""PyAudioTFT v%s (c) 2015 %s

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

Github repo: %s""" % (__version__,__author__,__repository__)

#
# BEGIN CONFIGURATION
#

# MPD server host name
__mpd_host__                = "localhost"

# MPD server port number
__mpd_port__                = 6600

# MPD Music directory
__mpd_music_dir__          = "/path/to/your/mpd/music/dir"

# Choose a theme
__theme__                   = "default"

# Display Framerate
__fps__                     = 12

#
# END OF CONFIGURATION
#

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "help" or sys.argv[1] == "-h":
            print(__doc__)
        else:
            print("No valid arg(s), exiting...")
    else:
        application = UI(__mpd_host__, __mpd_port__, __mpd_music_dir__, __theme__, __fps__)
        application.load()

if __name__ == "__main__":
    main()
