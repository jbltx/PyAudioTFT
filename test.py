import sys, os

resourcesDir = "resources"
titleFont = "Lato-Regular.ttf"

if not os.path.isfile(os.path.join(sys.path[0],resourcesDir,titleFont)):
	print "Error : Font file for title doesn't exist, exiting..."
	sys.exit(1)
else:
	print "lol"
