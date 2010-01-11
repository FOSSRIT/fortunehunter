import pippy, pygame, sys, math
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

######################################################################
#Tutorial Class: stores image list, traverses through list
######################################################################
class Tutorial:
    def __init__(self,imageList,sX,sY):
        self.currentIndex = 0
        self.images=[]

        for image in imageList:
          spt=pygame.sprite.Sprite()
          spt.image=pygame.image.load(image)
          spt.rect=pygame.Rect(sX,sY,1290,700)
	  self.images.append(spt)

       	self.size=len(imageList)

    def next(self):
    	if  self.currentIndex < self.size - 1:
       	  self.currentIndex+=1

    	else:
          self.currentIndex=0
	  player.mainMenu = True
	  player.inTutorial = False

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
