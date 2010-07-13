#! /usr/bin/env python
from AnimatedSprite import Spritesheet
from AnimatedSprite import AnimatedSprite
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

AnimPerLineArr=[ 
    [".bmp","AnimationPerLine/bmp16/"],
    [".bmp","AnimationPerLine/bmp24/"],
    [".gif","AnimationPerLine/gif/"]  ,
    [".gif","AnimationPerLine/gift/"] ,
    [".png","AnimationPerLine/png/"]  ,
    [".png","AnimationPerLine/pngt/"] ]

FixedWidthArr=[ 
    [".bmp","FixedWithSheets/bmp16/"],
    [".bmp","FixedWithSheets/bmp24/"],
    [".gif","FixedWithSheets/gif/"]  ,
    [".gif","FixedWithSheets/gift/"] ,
    [".png","FixedWithSheets/png/"]  ,
    [".png","FixedWidthSheets/pngt/"] ]

OneSheetArr=[ 
    [".bmp","OneSheetPerAnimation/bmp16/"],
    [".bmp","OneSheetPerAnimation/bmp24/"],
    [".gif","OneSheetPerAnimation/gif/"]  ,
    [".gif","OneSheetPerAnimation/gift/"] ,
    [".png","OneSheetPerAnimation/png/"]  ,
    [".png","OneSheetPerAnimation/pngt/"] ]

IndivFrameArr=[ 
    [".bmp","IndividualFrames/bmp16/"],
    [".bmp","IndividualFrames/bmp24/"],
    [".gif","IndividualFrames/gif/"]  ,
    [".gif","IndividualFrames/gift/"] ,
    [".png","IndividualFrames/png/"]  ,
    [".png","IndividualFrames/pngt/"] ]

screen = pygame.display.set_mode(SIZE) #Screen Set 600x400

screen.fill((BACKGROUNDR, BACKGROUNDG, BACKGROUNDB))

"""Reading Individual Frames
"""

def readIndivFrames(fileType, path):
 switch1 = [
  [pygame.image.load("%sa1/1%s"%(path,fileType))],
  [pygame.image.load("%sa1/2%s"%(path,fileType))],
  [pygame.image.load("%sa1/3%s"%(path,fileType))],
  [pygame.image.load("%sa1/4%s"%(path,fileType))],
  [pygame.image.load("%sa1/5%s"%(path,fileType))],
  [pygame.image.load("%sa1/6%s"%(path,fileType))],
  [pygame.image.load("%sa1/7%s"%(path,fileType))],
  [pygame.image.load("%sa1/8%s"%(path,fileType))],
  [pygame.image.load("%sa1/9%s"%(path,fileType))]
 ]

 switch2 = [
  [pygame.image.load("%sa2/1%s"%(path,fileType))],
  [pygame.image.load("%sa2/2%s"%(path,fileType))],
  [pygame.image.load("%sa2/3%s"%(path,fileType))],
  [pygame.image.load("%sa2/4%s"%(path,fileType))],
  [pygame.image.load("%sa2/5%s"%(path,fileType))],
  [pygame.image.load("%sa2/6%s"%(path,fileType))],
  [pygame.image.load("%sa2/7%s"%(path,fileType))],
  [pygame.image.load("%sa2/8%s"%(path,fileType))],
  [pygame.image.load("%sa2/9%s"%(path,fileType))]
 ]
 
 instances= []

 cnt = make
 
 while cnt > 0:
  animatedSprites = []
  animatedSprites.append([AnimatedSprite(switch1,'',10),[(40*cnt),0,2,2]])

  animatedSprites.append([AnimatedSprite(switch2,'',10),[(40*cnt),40,2,2]])

  instances.append(animatedSprites)

  cnt = cnt - 1

 trials = 0
 while trials < 5:

  groups = len(instances) - 1
  while groups >= 0:
   instances[groups][0][1][0] = 40 * groups
   instances[groups][0][1][1] = 0
   instances[groups][1][1][0] = 40 * groups
   instances[groups][1][1][1] = 40
   groups = groups - 1

  changes = 0
  start = time.time()
  while changes < 500:
   groups = len(instances) - 1
   while groups >= 0:
    instances[groups][0][0].nextFrame()
    instances[groups][1][0].nextFrame()

    if instances[groups][0][1][0] < 0 or instances[groups][0][1][0] > WIDTH - 40:
       instances[groups][0][1][2] = instances[groups][0][1][2] * -1
       
    if instances[groups][0][1][1] < 0 or instances[groups][0][1][1] > HEIGHT - 40:
       instances[groups][0][1][3] = instances[groups][0][1][3] * -1
       
    if instances[groups][1][1][0] < 0 or instances[groups][1][1][0] > WIDTH - 40:
       instances[groups][1][1][2] = instances[groups][1][1][2] * -1
       
    if instances[groups][1][1][1] < 0 or instances[groups][1][1][1] > HEIGHT - 40:
       instances[groups][1][1][3] = instances[groups][1][1][3] * -1
     

    instances[groups][0][1][0] += instances[groups][0][1][2]
    instances[groups][0][1][1] += instances[groups][0][1][3]

    instances[groups][1][1][0] += instances[groups][1][1][2]
    instances[groups][1][1][1] += instances[groups][1][1][3]

    screen.blit(instances[groups][0][0].image[0], (instances[groups][0][0].image[0].get_rect().move(instances[groups][0][1][0], instances[groups][0][1][1])))
    screen.blit(instances[groups][1][0].image[0], (instances[groups][1][0].image[0].get_rect().move(instances[groups][1][1][0], instances[groups][1][1][1])))

    groups = groups - 1
   pygame.display.flip()
   screen.fill((BACKGROUNDR,BACKGROUNDG,BACKGROUNDB))
   changes = changes + 1
  trials = trials + 1
  print(trials)
  print(1/((time.time() -start)/500))

#-----------------------------------------------------------------

def readPerLine(fileType, path):

 spriteSheet1 = Spritesheet(("%sButtons.%s"%(path,fileType)))

 instances= []

 cnt = make
 while cnt > 0:
  animatedSprites = []
  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,2,40,40),("%stext.txt"%(path)),10),[(40*cnt),0,2,2]])

  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,2,40,40),("%stext.txt"%(path)),10),[(40*cnt),40,2,2]])

  instances.append(animatedSprites)

  cnt = cnt - 1

 trials = 0
 while trials < 5:

  groups = len(instances) - 1
  while groups >= 0:
   instances[groups][0][1][0] = 40 * groups
   instances[groups][0][1][1] = 0
   instances[groups][1][1][0] = 40 * groups
   instances[groups][1][1][1] = 40
   groups = groups - 1

  changes = 0
  start = time.time()
  while changes < 500:
   groups = len(instances) - 1
   while groups >= 0:
    instances[groups][0][0].nextAnimFrame("anim1")
    instances[groups][1][0].nextAnimFrame("anim2")

    if instances[groups][0][1][0] < 0 or instances[groups][0][1][0] > WIDTH - 40:
       instances[groups][0][1][2] = instances[groups][0][1][2] * -1
       
    if instances[groups][0][1][1] < 0 or instances[groups][0][1][1] > HEIGHT - 40:
       instances[groups][0][1][3] = instances[groups][0][1][3] * -1
       
    if instances[groups][1][1][0] < 0 or instances[groups][1][1][0] > WIDTH - 40:
       instances[groups][1][1][2] = instances[groups][1][1][2] * -1
       
    if instances[groups][1][1][1] < 0 or instances[groups][1][1][1] > HEIGHT - 40:
       instances[groups][1][1][3] = instances[groups][1][1][3] * -1
     

    instances[groups][0][1][0] += instances[groups][0][1][2]
    instances[groups][0][1][1] += instances[groups][0][1][3]

    instances[groups][1][1][0] += instances[groups][1][1][2]
    instances[groups][1][1][1] += instances[groups][1][1][3]

    screen.blit(instances[groups][0][0].image, (instances[groups][0][0].image.get_rect().move(instances[groups][0][1][0], instances[groups][0][1][1])))
    screen.blit(instances[groups][1][0].image, (instances[groups][1][0].image.get_rect().move(instances[groups][1][1][0], instances[groups][1][1][1])))

    groups = groups - 1
   pygame.display.flip()
   screen.fill((BACKGROUNDR,BACKGROUNDG,BACKGROUNDB))
   changes = changes + 1
  trials = trials + 1
  print(trials)
  print(1/((time.time() -start)/500))

#-----------------------------------------------------------------
def readIndivSheet(fileType, path):

 spriteSheet1 = Spritesheet(("%s1%s"%(path,fileType)))
 spriteSheet2 = Spritesheet(("%s2%s"%(path,fileType)))
 
 instances= []

 cnt = make
 while cnt > 0:
  animatedSprites = []
  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,1,40,40),("%stext.txt"%(path)),10),[(40*cnt),0,2,2]])
  animatedSprites[0][0].addImages(spriteSheet2.img_extract(9,1,40,40))

  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,1,40,40),("%stext.txt"%(path)),10),[(40*cnt),40,2,2]])
  animatedSprites[1][0].addImages(spriteSheet2.img_extract(9,1,40,40))

  instances.append(animatedSprites)

  cnt = cnt - 1

 trials = 0
 while trials < 5:

  groups = len(instances) - 1
  while groups >= 0:
   instances[groups][0][1][0] = 40 * groups
   instances[groups][0][1][1] = 0
   instances[groups][1][1][0] = 40 * groups
   instances[groups][1][1][1] = 40
   groups = groups - 1

  changes = 0
  start = time.time()
  while changes < 500:
   groups = len(instances) - 1
   while groups >= 0:
    instances[groups][0][0].nextAnimFrame("anim1")
    instances[groups][1][0].nextAnimFrame("anim2")

    if instances[groups][0][1][0] < 0 or instances[groups][0][1][0] > WIDTH - 40:
       instances[groups][0][1][2] = instances[groups][0][1][2] * -1
       
    if instances[groups][0][1][1] < 0 or instances[groups][0][1][1] > HEIGHT - 40:
       instances[groups][0][1][3] = instances[groups][0][1][3] * -1
       
    if instances[groups][1][1][0] < 0 or instances[groups][1][1][0] > WIDTH - 40:
       instances[groups][1][1][2] = instances[groups][1][1][2] * -1
       
    if instances[groups][1][1][1] < 0 or instances[groups][1][1][1] > HEIGHT - 40:
       instances[groups][1][1][3] = instances[groups][1][1][3] * -1
     

    instances[groups][0][1][0] += instances[groups][0][1][2]
    instances[groups][0][1][1] += instances[groups][0][1][3]

    instances[groups][1][1][0] += instances[groups][1][1][2]
    instances[groups][1][1][1] += instances[groups][1][1][3]

    screen.blit(instances[groups][0][0].image, (instances[groups][0][0].image.get_rect().move(instances[groups][0][1][0], instances[groups][0][1][1])))
    screen.blit(instances[groups][1][0].image, (instances[groups][1][0].image.get_rect().move(instances[groups][1][1][0], instances[groups][1][1][1])))

    groups = groups - 1
   pygame.display.flip()
   screen.fill((BACKGROUNDR,BACKGROUNDG,BACKGROUNDB))
   changes = changes + 1
  trials = trials + 1
  print(trials)
  print(1/((time.time() -start)/500))


#-----------------------------------------------------------------
# iterator = 0
# print "\nTesting One Sheet Per Animation"
# print "" 
# while iterator < len(AnimPerLineArr):
# 
#  print ""
#  print OneSheetArr[iterator][1]
#  readIndivSheet(OneSheetArr[iterator][0],OneSheetArr[iterator][1])
#  iterator += 1
# 
# iterator = 0
# print ""
# print "Testing One Animation Per Line"
# print ""
# while iterator < len(OneSheetArr):
# 
#  print ""
#  print AnimPerLineArr[iterator][1]
#  readPerLine(AnimPerLineArr[iterator][0],AnimPerLineArr[iterator][1])
#  iterator += 1
#  
# iterator = 0
# print ""
# print "Testing Individual Frames"
# print ""
# while iterator < len(IndivFrameArr):
# 
#  print ""
#  print IndivFrameArr[iterator][1]
#  readIndivFrames(IndivFrameArr[iterator][0],IndivFrameArr[iterator][1])
#  iterator += 1 

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
dynamicObj.rotate(10)
dynamicObj.rotate(10)
dynamicObj.setPosition(0,0)
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
dynamicObj.rotate(45)

while cnt < 100:
  
  dynamicObj.nextFrame()
  screen.blit(dynamicObj.image[0], (dynamicObj.getXPos(), dynamicObj.getYPos()))
  dynamicObj.move()
  pygame.display.flip()
  screen.fill((BACKGROUNDR,BACKGROUNDG,BACKGROUNDB))
  cnt += 1

