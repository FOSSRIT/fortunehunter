#! /usr/bin/env python
import pygame
from pygame.locals import *
from boxes import BouncingBox
from time import time
from Scene import Scene
from DrawableObject import DrawableObject
from DrawableFontObject import DrawableFontObject
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

for aTrial in range(maxTrial):
    start = time()

    font = pygame.font.SysFont("cmr10", 24)
    d = DrawableFontObject("hello world", font)
    d.goToAnim("anim1")

    group1=Scene(d)
    groups=[group1]
    print (time()-start) ,
    print " -- Time to load"


    clock = pygame.time.Clock()
    clock.tick()
    start = time()
    for frame in range(FRAME):
        dirtyList=[]
        for image in range(numImages):
            #move / collision detection
            groups[image].update(clock.get_time())
            clock.tick()
            #individually blit each image group - add to list for update
            dirtyList.extend(groups[image].draw(screen))

        #draw the images flip/update
        pygame.display.update(dirtyList)
        for image in range(numImages):
            groups[image].clear(screen, background)

    #print 1/((time()-start)/FRAME)
    pygame.display.flip()
