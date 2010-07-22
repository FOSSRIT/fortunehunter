import pygame
from pygame.locals import *
from boxes import UpDownBox
from time import time

pygame.init()
boxes = pygame.sprite.RenderUpdates()
boxesTwo = pygame.sprite.RenderUpdates()
boxesThree = pygame.sprite.RenderUpdates()

switch1 = [
  pygame.image.load("%sa1/1%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/2%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/3%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/4%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/5%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/6%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/7%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/8%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/9%s"%("IndividualFrames/bmp16/",".bmp"))
]

switch2 = [
  pygame.image.load("%sa1/1%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/2%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/3%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/4%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/5%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/6%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/7%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/8%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/9%s"%("IndividualFrames/bmp16/",".bmp"))
]

switch3 = [
  pygame.image.load("%sa1/1%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/2%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/3%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/4%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/5%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/6%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/7%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/8%s"%("IndividualFrames/bmp16/",".bmp")),
  pygame.image.load("%sa1/9%s"%("IndividualFrames/bmp16/",".bmp"))
]

boxes.add(UpDownBox(switch1, (0, 0)))
boxes.add(UpDownBox(switch1, (100, 100)))
boxes.add(UpDownBox(switch1, (200, 200)))


screen = pygame.display.set_mode([1200, 900])
boxesTwo.add(UpDownBox([pygame.image.load("goblin.png")], (300,0)))
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
