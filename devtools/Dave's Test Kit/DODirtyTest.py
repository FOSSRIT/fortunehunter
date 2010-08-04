#! /usr/bin/env python
import pygame
from pygame.locals import *
import time
from Scene import Scene
from DrawableObject import DrawableObject
from DynamicDrawableObject import DynamicDrawableObject
pygame.init()

FRAME=2500 #setting number of frames per trial
screenWidth = 600 #screen width
screenHeight = 400 #screen height
numImages = 4 #number of copies of images
numGroups = 1
maxTrial = 5 # multiple trials, but hard coded in this test

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
    start = time.time()#starting timer

#creating my DynamicDrawableObject object using my previously made images list
    a = DynamicDrawableObject(surfaceList,'', 72, 40, 40 , 2,2)
    b = DynamicDrawableObject(surfaceList,'', 24, 80, 80 , 2,2)
    c = DynamicDrawableObject(surfaceList,'', 12,120, 120, 2,2)
    d = DynamicDrawableObject(surfaceList,'', 1, 160, 160, 2,2)

    sceneList=[Scene(a),] #creating my array of scenes
    sceneList[0].addObjects([b,c,d])
    
    for sc in range(numGroups):
        for img in range(sceneList[sc].getListSize()):
            sceneList[sc].getObject(img).setSpeed(2,2)
    
    #printing time to load images and stuff
    print (time.time()-start) ,
    print " -- Time to load"
    
    #setting up timer stuff
    clock = pygame.time.Clock()
    clock.tick()
    start = time.time()
    
    #loop that goes through and upodates my objects
    for frame in range(FRAME):
        time.sleep(.25)
        dirtyList=[]
        for sc in range(numGroups):

            for img in range(sceneList[sc].getListSize()):
                thisrect = sceneList[sc].getObject(img).getRectangle()
                if thisrect.right>screenWidth or thisrect.left<0:
                    sceneList[sc].setSpeed( sceneList[sc].getXSpeed()*-1, None )
                if thisrect.bottom>screenHeight or thisrect.top<0:
                    sceneList[sc].setSpeed( None , sceneList[sc].getYSpeed()*-1 )
            
            sceneList[sc].update(clock.get_time()) #calls the update function for my DDO
            
            clock.tick() #ticks clock
            
            dirtyList.extend( sceneList[sc].draw(screen) )#adding stuff that has been updated to my dirty list

        pygame.display.update(dirtyList) #updates the screen with the dirty list
        for sc in range(numGroups):
            sceneList[sc].clear(screen, background) #clears stuff behind images based on given background image.
