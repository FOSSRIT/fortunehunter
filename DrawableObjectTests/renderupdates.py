import pygame
from pygame.locals import *
from boxes import UpDownBox
from time import time

pygame.init()
boxes = pygame.sprite.RenderUpdates()

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

boxes.add(UpDownBox(switch1, location))

screen = pygame.display.set_mode([400, 400])
background = pygame.image.load("Room.gif")
#background.fill(pygame.image.load("Room.gif"))
screen.blit(background, [0, 0])
pygame.display.flip()
start = time()
for i in range(500):
    boxes.update(pygame.time.get_ticks(), 150)
    rectlist = boxes.draw(screen)
    pygame.display.update(rectlist)
    #pygame.time.delay(10)
    boxes.clear(screen, background)
    
print 500/(time() - start)
