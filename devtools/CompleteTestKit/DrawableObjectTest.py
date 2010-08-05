#2345678911234567892123456789312345678941234567895123456789612345678971234567898
#! /usr/bin/env python
import pygame
from pygame.locals import *
import time
from Scene import Scene
from DrawableObject import DrawableObject
from DynamicDrawableObject import DynamicDrawableObject

pygame.init()

screenWidth = 600   # screen width
screenHeight= 400   # screen height

maxFrame    = 10000 # Number of frame refreshes per trial run
maxImage    = 5     # " Animated images to create
maxScene    = 1     # " Scenes to load simultaneously
maxTrial    = 5     # " Trials to loop through

# 'Constants' that would otherwise be passed in declared ^^ 
# Begin creating test variables

screen = pygame.display.set_mode( (screenWidth,screenHeight) )
background = pygame.image.load("./art/GIF/Room.gif").convert()
clock=pygame.time.Clock()

#2345678911234567892123456789312345678941234567895123456789612345678971234567898
surfaceList = [
        pygame.image.load("./art/GIF/1.gif").convert(),
        pygame.image.load("./art/GIF/2.gif").convert(),
        pygame.image.load("./art/GIF/3.gif").convert(),
        pygame.image.load("./art/GIF/4.gif").convert(),
        pygame.image.load("./art/GIF/5.gif").convert(),
        pygame.image.load("./art/GIF/6.gif").convert(),
        pygame.image.load("./art/GIF/7.gif").convert(),
        pygame.image.load("./art/GIF/8.gif").convert(),
        pygame.image.load("./art/GIF/9.gif").convert()]

#2345678911234567892123456789312345678941234567895123456789612345678971234567898
# Make the screen and the background image
pygame.display.set_caption("Sprite Speed Test Window")
screen.blit( background,(0,0) )
pygame.display.flip()

# Make the DDO's to use in the screen
aDDO = DynamicDrawableObject( surfaceList,'', 1,  0,  0,2,2 )
bDDO = DynamicDrawableObject( surfaceList,'', 8, 40, 40,2,2 )
cDDO = DynamicDrawableObject( surfaceList,'',12, 80, 80,2,2 )
dDDO = DynamicDrawableObject( surfaceList,'',24,120,120,2,2 )
eDDO = DynamicDrawableObject( surfaceList,'',72,160,160,2,2 )

myScene = Scene(aDDO) # creating my scenes
myScene.addObjects( [ bDDO , cDDO , dDDO , eDDO ] )

for trial in range(maxTrial):
    clock.tick()
    for frame in range(maxFrame):
        dirtyList = []
        
        myscene.moveObjects()
        myScene.update( clock.get_time() )
        pygame.display.update( myScene.draw(screen) )
        
        clock.tick()

#2345678911234567892123456789312345678941234567895123456789612345678971234567898
