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
"""
try:
    f=preferences[0][9]
except:
    f=preferences[0][9]=open('./logs/Test Results - %s.csv' 
        %str(datetime.now()),'a')
f.write("\n\nSpeed Test - "+str(datetime.now()))
f.write(",Width (pixels)"+','+"Height (pixels)"+','+
    "Trial Runs"+','+"Image Objects Drawn")
f.write("\n,"+str(screenWidth)+','+str(screenHeight)+','+
    str(maxTrial)+','+str(numImages))
f.write("\nFile Type"+','+"Time taken to load images to memory"+
    ','+"Trials (frames per second)")
"""
print "width,height",
print screenWidth,
print ",",
print screenHeight

screen = pygame.display.set_mode( [int(screenWidth),
    int(screenHeight)] ) #Screen Set 600x400
pygame.display.set_caption("Sprite Speed Test Window")
GREEN = 0, 192, 0 # green
background = pygame.Surface( (screenWidth,screenHeight) )
background.fill(GREEN)
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

#make our groups
group1=pygame.sprite.RenderUpdates( BouncingBox(frameList,(0,0)) )
group2=pygame.sprite.RenderUpdates(BouncingBox(frameList,(40,40)) )
group3=pygame.sprite.RenderUpdates(BouncingBox(frameList,(80,80)) )
group4=pygame.sprite.RenderUpdates(BouncingBox(frameList,(120,120)) )
group5=pygame.sprite.RenderUpdates(BouncingBox(frameList,(160,160)) )

print (time()-start) ,
print " -- Time to load"

groups=[group1,group2,group3,group4,group5]

"""while 1:
    try:ft=ftArr[t]
    except: 
        print "\nTest Complete\n"
        break
    f.seek(0,2)
    f.write(str('\n'+ft[1]+' Speed Test'))
    f.seek(0,2)
    start=time.time()

    f.write(',')
    f.write(str(time.time()-start))
"""
print time()-start

for aTrial in range(maxTrial):
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
"""f.seek(0,2)
        f.write(','+str(1/((time.time()-start)/r)))


screen = pygame.display.set_mode([1200, 900])
boxesTwo.add(UpDownBox([pygame.image.load("goblin.png")], (0,300)))
background = pygame.image.load("Room.gif")
#background.fill(pygame.image.load("Room.gif"))
screen.blit(background, [0, 0])
pygame.display.flip()

boxesTwo.update(pygame.time.get_ticks(), 700)
rectlist = boxesTwo.draw(screen)
pygame.display.update(rectlist)
start = time()
for i in range(2000):
    boxes.update(pygame.time.get_ticks(), 700)
    boxesTwo.update(pygame.time.get_ticks(), 700)
    rectlist = boxesTwo.draw(screen)
    rectlist.extend(boxes.draw(screen))
    pygame.display.update(rectlist)
    boxesTwo.clear(screen, background)
    boxes.clear(screen, background)

print 2000/(time() - start)
"""
