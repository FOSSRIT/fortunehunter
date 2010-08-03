#! /usr/bin/env python
import pygame
from pygame.locals import *
from time import time
from Scene import Scene
from DrawableObject import DrawableObject
from DynamicDrawableObject import DynamicDrawableObject
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

#Creating my list of images to use later
surfaceList = [
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/1.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/2.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/3.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/4.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/5.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/6.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/7.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/8.bmp").convert(),
    pygame.image.load(
        "./Animation Styles/IndividualFrames/bmp16/a2/9.bmp").convert()
    ]

for aTrial in range(maxTrial):
    start = time()#starting timer

    d = DynamicDrawableObject(surfaceList,'', 100) #creating my DynamicDrawableObject object using my previously made images list

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
        for image in range(numImages):
            groups[image].update(clock.get_time())#calls the update function for my DDO
            clock.tick()#ticks clock
            dirtyList.extend(groups[image].draw(screen))#adding stuff that has been updated to my dirty list

        pygame.display.update(dirtyList)#updates the screen with the dirty list
        for image in range(numImages):
            groups[image].clear(screen, background)#clears stuff behind images based on given background image.
