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

#GREEN = 0, 192, 0
screenWidth = 600
screenHeight = 400
maxGroup = 1
maxTrial = 1 # multiple trials, but hard coded in this test
maxFrame=500 #temperary
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
    
    ###NOTE: Convert to an encapsulated LOOP###
    
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

    """ Object 1 will be a static image that will not be animating NOTE: once 
        you pass the list of frames to the object, they and their encapsulated 
        metadata are no longer only surfaces but are considered instead to be 
        Sprite Objects
    """
    drawObject1 = DrawableObject(surfaceList, infoFilePath, None, 0 , 0 , 1 , 1)
    drawObject1.goToAnim("anim1")
    
    """ 2-4 are dynamic objects that will refresh at varying rates to illustrate
        the capabilities of our code to allow users to have varying refresh rate
    """
    drawObject2 = DynamicDrawableObject(
        surfaceList,infoFilePath,24,40,40,1,1)
    drawObject2.goToAnim("anim1")
    
    drawObject3 = DynamicDrawableObject(
        surfaceList,infoFilePath,24,80,80,1,1)
    drawObject3.goToAnim("anim1")
    
    drawObject4 = DynamicDrawableObject(
        surfaceList,infoFilePath,24,120,120,1,1)
    drawObject4.goToAnim("anim1")
    
    drawObject5 = DynamicDrawableObject(
        surfaceList,infoFilePath,24,160,160,1,1)
    drawObject5.goToAnim("anim1")

    group1 = Scene( drawObject1 )
    group1.addObjects( [drawObject2] )
    group1.addObjects( [drawObject3] )
    group1.addObjects( [drawObject4] )
    group1.addObjects( [drawObject5] )

    ### END: Convert to an encapsulated LOOP###

    """ We only need a single group for this example, but this format of an 
        ordered list of our scenes/groups will be echoed in our end 
        implementation.
        
        Revisit this and possibly simplify: this isn't a tutorial for suggested
        techniques, but a test to demonstrate that it can be applied and to 
        record the data to imply why it's a viable alternative
    """
    
#    groupsList=[group1] # < --- What the hell and why

    print (time()-start) ,
    print " -- Time to load and sort animations into groupsListList"

    clock = pygame.time.Clock()
    clock.tick() # <--Updates the clock variable in milliseconds
    
    start = time()
    for maxFrame in range(maxFrame):
        dirtyList=[]

        """ Move/collision detection, individually blit each image group, add to 
            dirtyList within the trial, this iterates through a list containing 
            sublists of surfaces that we want to update.  This list contains both 
        """
        for grp in range(maxGroup):
            groupsList[grp].update( clock.get_time() )
            clock.tick()
            dirtyList.extend( groupsList[grp].draw(screen) )
        print dirtyList
        pygame.display.update(dirtyList) # <-- is there a faster way to place?
        
        for grp in range(maxGroup):
            groupsList[grp].clear(screen, background)

    print "Trial's average framerate was " , str(1/((time()-start)/maxFrame))
    
