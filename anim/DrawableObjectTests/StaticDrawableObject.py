import pygame
from DrawableObject import DrawableObject

class StaticDrawableObject(pygame.sprite.Sprite):

    def __init __(self,images,textfileName,fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self._images = images

        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.animations = {}
        
        if textfileName != '':

           f = open(textfileName, 'r')
           currentLine = f.readline()
           while currentLine != '':

             animValues = currentLine.split(",")
             self.animations[animValues[0]] =  [int(animValues[1]), int(animValues[2])]
             currentLine = f.readline()


    def addImages(self, images):

        self._images.extend(images)



