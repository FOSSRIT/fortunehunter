#! /usr/bin/env python
import pygame
from pygame.locals import *
from time import time
from Scene import Scene
from DrawableObject import DrawableObject
from DrawableFontObject import DrawableFontObject
pygame.init()

FRAME=500 #setting number of frames per trial
screenWidth = 600 #screen width
screenHeight = 400 #screen height
numImages = 1 #number of copies of images
maxTrial = 5 # multiple trials, but hard coded in this test
dirtyList=[] #list for objects to be updated

#print the height and width
print "width,height",
print screenWidth,
print ",",
print screenHeight

screen = pygame.display.set_mode( [int(screenWidth),
    int(screenHeight)] ) #Setting the screen size to the given size
pygame.display.set_caption("Sprite Speed Test Window")
background = pygame.image.load("Room.gif")#Loading my background image
screen.blit(background,[0,0])#blitting my background to screen
pygame.display.flip()#flipping screen
start = time()

for aTrial in range(maxTrial):
    start = time()

    font = pygame.font.SysFont("cmr10", 100)
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
        d.changeText(str(frame))
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
    #pygame.display.flip()
