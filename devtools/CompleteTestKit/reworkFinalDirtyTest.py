#! /usr/bin/env python
import pygame
from pygame.locals import *
from boxes import BouncingBox
from time import time
from Scene import Scene
from DrawableObject import DrawableObject
from DynamicDrawableObject import DynamicDrawableObject
pygame.init()

#2345678911234567892123456789312345678941234567895123456789612345678971234567898
#2345678911234567892123456789312345678941234567895123456789612345678971234567898

screenWidth = 600
screenHeight = 400
maxImage = 5
maxGroup = 1 # not implemented for the first step
        # groups are scenes within our code - our Scene inherits Group and ergo
        # functions as such
maxTrial = 1 # multiple trials, but hard coded in this test
maxFrame=500 # temperary
infoFilePath = 'animInfo.txt'

screen = pygame.display.set_mode(( screenWidth,screenHeight) )
pygame.display.set_caption("Testing Custom Objects - FinalDirtyTest.py")
background = pygame.image.load("Room.gif")

start = time()

for trial in range(maxTrial):
    print "New trial"
    screen.blit( background , [0,0] )
    pygame.display.flip()
    
    start = time()   
    surfaceList = []
    drawObject = []
    scenesList = []
    
    drawObject = [ DrawableObject(
        surfaceList, infoFilePath, None, 0 , 0 , 1 , 1) ]
    drawObject[0].goToAnim("anim1")
    
    for img in range(maxImage)[1:]:
        surfaceList.append(pygame.image.load(
            "./Animation Styles/IndividualFrames/bmp16/a2/",img,
            "1.bmp").convert()))
        drawObject[img] = DynamicDrawableObject(
            surfaceList,infoFilePath,24,img*40,img*40,1,1)
        drawObject[img].goToAnim("anim1")
        if img==1:
            scene1[] = Scene( drawObject[img] )
            scenesList.append(scene1)
        else:
            scene1.addObjects( [ drawObject[img] ] )
            scenesList.append(scene1)

# 'scenesList' is a list filled with Scene objects (those inherit/extend Group)

    print (time()-start) ,
    print " -- Time to load and sort animations into scenesList"

    clock = pygame.time.Clock()
    clock.tick() # <--Updates the clock variable in milliseconds
    
    start = time()
    for maxFrame in range(maxFrame):
        dirtyList=[]
        
        scenesList[1].update( clock.get_time() ) ## hard coded for now
        clock.tick()
        dirtyList.extend( scenesList[grp].draw(screen) )
        print dirtyList
        pygame.display.update(dirtyList) # <-- is there a faster way to place?

        scenesList[grp].clear(screen, background)

    print "Trial's average framerate was " , str(1/((time()-start)/maxFrame))
