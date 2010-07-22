#! /usr/bin/env python
import pygame
from pygame.locals import *
from boxes import BouncingBox
from time import time
pygame.init()

FRAME=500
screenWidth = 600
screenHeight = 400
numImages = 5
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

for aTrial in range(maxTrial):
    start = time()
    group1=pygame.sprite.RenderUpdates(BouncingBox(frameList,(0,0)) )
    group2=pygame.sprite.RenderUpdates(BouncingBox(frameList,(40,40)) )
    group3=pygame.sprite.RenderUpdates(BouncingBox(frameList,(80,80)) )
    group4=pygame.sprite.RenderUpdates(BouncingBox(frameList,(120,120)) )
    group5=pygame.sprite.RenderUpdates(BouncingBox(frameList,(160,160)) )
    groups=[group1,group2,group3,group4,group5]
    print (time()-start) ,
    print " -- Time to load"

    start = time()
    for frame in range(FRAME):
        dirtyList=[]
        for image in range(numImages):
            #move / collision detection
            groups[image].update( screenWidth,screenHeight )
            
            #individually blit each image group - add to list for update
            dirtyList.extend(groups[image].draw(screen))
            
        #draw the images flip/update
        pygame.display.update(dirtyList)
        for image in range(numImages):
            groups[image].clear(screen, background)


    print 1/((time()-start)/FRAME)
    pygame.display.flip()    
