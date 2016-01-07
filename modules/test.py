import pygame, os, sys

pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode((320,240), pygame.FULLSCREEN, 0)
clock = pygame.time.Clock()
sh = screen.get_height()
sw = screen.get_width()
padding = int(sh*0.05)
over = False
color = (255,255,255)
latoLight = os.path.join(sys.path[0],"resources","Lato-Light.ttf")
latoRegular = os.path.join(sys.path[0],"resources","Lato-Regular.ttf")


#CREATE AREA ELEMENTS
coverArea = pygame.Surface((sh*0.5, sh*0.5))
artistArea = pygame.Surface((sw-sh*0.5-padding*3, sh*0.07),pygame.SRCALPHA)
artistFont = pygame.font.Font(latoLight,int(artistArea.get_height()*0.9))
titleArea = pygame.Surface((sw-sh*0.5-padding*3, sh*0.1),pygame.SRCALPHA)
titleFont = pygame.font.Font(latoRegular,int(titleArea.get_height()*0.9))
albumArea = pygame.Surface((sw-sh*0.5-padding*3, sh*0.07),pygame.SRCALPHA)
albumFont = pygame.font.Font(latoLight,int(albumArea.get_height()*0.9))
bitrateArea = pygame.Surface((sw-padding*4-sh*0.72,sh*0.07),pygame.SRCALPHA)
bitrateFont = pygame.font.Font(latoLight,int(bitrateArea.get_height()*0.9))
metaArea = pygame.Surface((sw-padding*4-sh*0.72,sh*0.07),pygame.SRCALPHA)
metaFont = pygame.font.Font(latoLight,int(metaArea.get_height()*0.9))
logoArea = pygame.Surface((sh*0.23,sh*0.23),pygame.SRCALPHA)
repeatArea = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
singleArea = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
randomArea = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
consumeArea = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
stateArea = pygame.Surface((sh*0.18, sh*0.18),pygame.SRCALPHA)
currentTimeArea = pygame.Surface((sw*0.2,sh*0.075),pygame.SRCALPHA)
timeFont = pygame.font.Font(latoLight,int(currentTimeArea.get_height()*0.8))
playlistArea = pygame.Surface((sw*0.15,sh*0.075),pygame.SRCALPHA)
volumeArea = pygame.Surface((sw*0.13,sh*0.075),pygame.SRCALPHA)
totalTimeArea = pygame.Surface((sw*0.2,sh*0.075),pygame.SRCALPHA)
timingArea = pygame.Surface((sw-padding*2-sh*0.2, sh*0.06),pygame.SRCALPHA)

bg = pygame.transform.scale(pygame.image.load(
    os.path.join(sys.path[0],"resources","background.png")
).convert(), (sw, sh))
screen.blit(bg, (0,0))

# UPDATE ELEMENTS
coverFile = os.path.join(sys.path[0],"resources","cover.png")
cover = pygame.image.load(coverFile).convert()
cover = pygame.transform.scale(cover, (int(sh*0.5), int(sh*0.5)))
coverArea.blit(cover, (0,0))

artist = artistFont.render("Test Artist", 0, color)
artistArea.blit(artist, (0,-2))

title = titleFont.render("The song title", 0, color)
titleArea.blit(title, (0,-2))

album = albumFont.render("ALbum Name - 1999", 0, color)
albumArea.blit(album, (0,-2))

bitrate = bitrateFont.render("320 kbps", 0, color)
bitrateArea.blit(bitrate, (0,-2))

meta = metaFont.render("2ch/24bits/192000Hz", 0, color)
metaArea.blit(meta, (0,-2))

logoFile = os.path.join(sys.path[0],"resources","format-mp3.png")
logo = pygame.image.load(logoFile).convert_alpha()
logo = pygame.transform.scale(logo,(logoArea.get_width(),logoArea.get_height()))
logoArea.blit(logo, (0,0))

repeatOffFile = os.path.join(sys.path[0],"resources","repeat-inactive.png")
repeatOnFile = os.path.join(sys.path[0],"resources","repeat-active.png")
repeat = pygame.image.load(repeatOnFile).convert_alpha()
repeat = pygame.transform.scale(repeat,(int(sh*0.18),int(sh*0.18)))
repeatArea.blit(repeat, (0,0))

singleOffFile = os.path.join(sys.path[0],"resources","single-inactive.png")
singleOnFile = os.path.join(sys.path[0],"resources","single-active.png")
single = pygame.image.load(singleOnFile).convert_alpha()
single = pygame.transform.scale(single,(int(sh*0.18),int(sh*0.18)))
singleArea.blit(single, (0,0))

randomOffFile = os.path.join(sys.path[0],"resources","random-inactive.png")
randomOnFile = os.path.join(sys.path[0],"resources","random-active.png")
random = pygame.image.load(randomOnFile).convert_alpha()
random = pygame.transform.scale(random,(int(sh*0.18),int(sh*0.18)))
randomArea.blit(random, (0,0))

consumeOffFile = os.path.join(sys.path[0],"resources","consume-inactive.png")
consumeOnFile = os.path.join(sys.path[0],"resources","consume-active.png")
consume = pygame.image.load(consumeOnFile).convert_alpha()
consume = pygame.transform.scale(consume,(int(sh*0.18),int(sh*0.18)))
consumeArea.blit(consume, (0,0))

statePlayFile = os.path.join(sys.path[0],"resources","play.png")
state = pygame.image.load(statePlayFile).convert_alpha()
state = pygame.transform.scale(state,(int(sh*0.18),int(sh*0.18)))
stateArea.blit(state, (0,0))

currentTime = timeFont.render("00:00:00",0,color)
currentTimeArea.blit(currentTime, (0,-2))

playlist = timeFont.render("99/99",0,color)
playlistArea.blit(playlist, (0,-2))

volume = timeFont.render("100%",0,color)
volumeArea.blit(volume, (0,-2))

totalTime = timeFont.render("00:00:00",0,color)
totalTimeArea.blit(totalTime, (totalTimeArea.get_width()-totalTime.get_width(),-2))

timingOutline = pygame.Rect(0,0,timingArea.get_width(),timingArea.get_height())
pygame.draw.rect(timingArea, color, timingOutline, 2)
timeScale = (timingArea.get_width()-12)*1
timing = pygame.Rect(0,0,timeScale,timingArea.get_height())
pygame.draw.rect(timingArea, color, timing)


# DISPLAY ELEMENTS
screen.blit(coverArea, (padding,padding))
screen.blit(artistArea, (padding*2+sh*0.5, padding))
screen.blit(titleArea, (padding*2+sh*0.5, padding+sh*0.08))
screen.blit(albumArea, (padding*2+sh*0.5, padding+sh*0.19))
screen.blit(bitrateArea, (padding*2+sh*0.5, sh*0.40))
screen.blit(metaArea, (padding*2+sh*0.5, sh*0.48))
screen.blit(logoArea, (sw-padding-logoArea.get_width(), sh*0.32))
screen.blit(repeatArea, (padding,padding*1.5+sh*0.5))
screen.blit(singleArea, (sw*0.3, padding*1.5+sh*0.5))
screen.blit(randomArea, (sw*0.7-sh*0.18, padding*1.5+sh*0.5))
screen.blit(consumeArea, (sw-padding-sh*0.18,padding*1.5+sh*0.5))
screen.blit(stateArea, (padding, sh-padding-sh*0.18))
screen.blit(currentTimeArea, (padding+sh*0.2, sh-padding-sh*0.17))
screen.blit(playlistArea, (padding+sw*0.15+sh*0.3, sh-padding-sh*0.17))
screen.blit(volumeArea, (padding+sw*0.33+sh*0.3, sh-padding-sh*0.17))
screen.blit(totalTimeArea, (sw-padding-sw*0.2, sh-padding-sh*0.17))
screen.blit(timingArea, (padding+sh*0.2,sh-padding-sh*0.08))

while not over:

    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            over = True

    # REFRESH THE SCREEN
    pygame.display.update()
    clock.tick(30)
pygame.quit()
