#! /usr/bin/env python
from Spritesheet import Spritesheet
from DynamicDrawableObject import DynamicDrawableObject
import pygame
import time
pygame.init()

make=input("How many images would you like to load? ")
img={}
ft="" #filetype
r=0 #frame refreshes
i=1 #cycles images
SIZE = WIDTH, HEIGHT = 600,400 #screen sizes
t=0 #trial number

BACKGROUNDR=152
BACKGROUNDG=0
BACKGROUNDB=152

screen = pygame.display.set_mode(SIZE) #Screen Set 600x400

screen.fill((BACKGROUNDR, BACKGROUNDG, BACKGROUNDB))

switch1 = [
  [pygame.image.load("%sa1/1%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/2%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/3%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/4%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/5%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/6%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/7%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/8%s"%("IndividualFrames/bmp16/",".bmp"))],
  [pygame.image.load("%sa1/9%s"%("IndividualFrames/bmp16/",".bmp"))]
]

dynamicObj = DynamicDrawableObject(switch1,'',1,0,0, 2, 2)

cnt = 0

while cnt < 100:

  dynamicObj.nextFrame()
  screen.blit(dynamicObj.image[0], (dynamicObj.getXPos(), dynamicObj.getYPos()))
  dynamicObj.move()
  pygame.display.flip()
  screen.fill((BACKGROUNDR,BACKGROUNDG,BACKGROUNDB))
  cnt += 1
  
cnt = 0
dynamicObj.setPosition(0,0)
dynamicObj.scale(160, 160)

while cnt < 100:
  
  dynamicObj.nextFrame()
  screen.blit(dynamicObj.image[0], (dynamicObj.getXPos(), dynamicObj.getYPos()))
  dynamicObj.move()
  pygame.display.flip()
  screen.fill((BACKGROUNDR,BACKGROUNDG,BACKGROUNDB))
  cnt += 1

