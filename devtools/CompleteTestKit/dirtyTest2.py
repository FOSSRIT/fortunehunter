#! /usr/bin/env python
import pygame
from pygame.locals import *
from boxes import BouncingBox
from time import time
from NewScene import Scene
from DrawableObject import DrawableObject
from DynamicDrawableObject import DynamicDrawableObject
pygame.init()

FRAME=500
screenWidth = 600
screenHeight = 400
numImages = 1
maxTrial = 5 # multiple trials, but hard coded in this test
dirtyList=[]

print "width,height",
print screenWidth,
print ",",
print screenHeight

screen = pygame.display.set_mode( [int(screenWidth),
    int(screenHeight)] ) #Screen Set 600x400
pygame.display.set_caption("Sprite Speed Test Window")
GREEN = 0, 192, 0 # green
background = pygame.image.load("Room.gif")
screen.blit(background,[0,0])
pygame.display.flip()
start = time()
frameList = [
    pygame.image.load("./art/BMP24/1.bmp").convert(),
    pygame.image.load("./art/BMP24/2.bmp").convert(),
    pygame.image.load("./art/BMP24/3.bmp").convert(),
    pygame.image.load("./art/BMP24/4.bmp").convert(),
    pygame.image.load("./art/BMP24/5.bmp").convert(),
    pygame.image.load("./art/BMP24/6.bmp").convert(),
    pygame.image.load("./art/BMP24/7.bmp").convert(),
    pygame.image.load("./art/BMP24/8.bmp").convert(),
    pygame.image.load("./art/BMP24/9.bmp").convert(),
]
frameList2 = [
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/1.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/2.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/3.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/4.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/5.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/6.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/7.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/8.bmp").convert(),
    pygame.image.load("./Animation Styles/IndividualFrames/bmp16/a2/9.bmp").convert(),
]

for aTrial in range(maxTrial):
    start = time()
    group1=Scene(DynamicDrawableObject(frameList,"",1,0,0,2,2))
    group1.addObjects([DynamicDrawableObject(frameList2,"",1,40,40,2,2)])
    group1.addObjects([DynamicDrawableObject(frameList,"",1,80,80,2,2)])
    group1.addObjects([DynamicDrawableObject(frameList2,"",1,120,120,2,2)])
    group1.addObjects([DynamicDrawableObject(frameList,"",1,160,160,2,2)])
    groups=[group1]
    print (time()-start) ,
    print " -- Time to load"


    start = time()
    for frame in range(FRAME):
        dirtyList=[]
        #if frame == 250: groups[0][4].scale(200,200)
        for image in range(numImages):
            #move / collision detection
            groups[image].update( screenWidth,screenHeight )

            #individually blit each image group - add to list for update
            dirtyList.extend(groups[image].draw(screen))

        #draw the images flip/update
        pygame.display.update(dirtyList)
        for image in range(numImages):
            groups[image].clear(screen, background)

    group1.calcPosition()
    print group1.getXPos()
    print group1.getYPos()
    print 1/((time()-start)/FRAME)
    pygame.display.flip()
