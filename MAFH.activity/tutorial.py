#Tutorial Class: stores image list, traverses through list
######################################################################
import pippy, pygame, sys, math
from player import *
from hero import *
from enemy import *
from battleEngine import *
from menu import *
from dungeon import *
from map import *
from room import *
from item import *
from pygame.locals import *
from random import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

class Tutorial:
    def __init__(self,imageList):
        self.currentIndex = 0
        self.images=[]

        for image in imageList:
            spt=pygame.sprite.Sprite()
            spt.image=pygame.image.load(image)
            spt.rect=pygame.Rect(0,0,1290,700)
          
            self.images.append(spt)

       	self.size=len(imageList)

    def next(self):
    	if  self.currentIndex < self.size - 1:
       	  self.currentIndex+=1

    	else:
          self.currentIndex=0
	  #player.mainMenu = True
	  #player.inTutorial = False

    def previous(self):
      if self.currentIndex > 0:
        self.currentIndex-=1

      else:
        self.currentIndex=0

    def draw(self,group,screen):
        group.empty()
        group.add(self.images[self.currentIndex])
        group.draw(screen)
        pygame.display.flip()

