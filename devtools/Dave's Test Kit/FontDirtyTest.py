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

for aTrial in range(maxTrial):
    start = time()#starting timer

    font = pygame.font.SysFont("cmr10", 100) #creating my font object
    d = DrawableFontObject("hello world", font) #creating my DrawableFontObject object using my previously made font object

    group1=Scene(d) #creating my scene
    groups=[group1] #creating my array of scenes
    #printing time to load images and stuff
    print (time()-start) ,
    print " -- Time to load"

    #setting up timer stuff
    clock = pygame.time.Clock()
    clock.tick()
    start = time()
    #loop that goes through and upodates my objects
    for frame in range(FRAME):
        dirtyList=[]
        d.changeText(str(frame))#updates my text for my DFO
        for image in range(numImages):
            groups[image].update(clock.get_time())#calls the update function for my DFO
            clock.tick()#ticks clock
            dirtyList.extend(groups[image].draw(screen))#adding stuff that has been updated to my dirty list

        pygame.display.update(dirtyList)#updates the screen with the dirty list
        for image in range(numImages):
            groups[image].clear(screen, background)#clears stuff behind images based on given background image.
