import pygame

class Scene(pygame.sprite.RenderUpdates):

    def __init__(self, *sprites):

       self._spritelist = []
       RenderUpdates.__init__(self, *sprites)

    #def calcPosition(self):

    #def calcSize(self):

    def addObjects(self, newDrawableObjects):
        for sprite in newDrawableObjects:
           RenderUpdates.add_internal(self, sprite)
           self._spritelist.append(sprite)

    #def setRelativePositions(self):

    def removeObject(self, sprite):
       RenderUpdates.remove_internal(self, sprite)
       self._spritelist.remove(sprite)

    #def getObject(self, index):

    def getListSize(self):

       return len(self._spritelist)

    def getList(self):

       return list(self._spritelist)

    #def moveObjects(self):

    #def moveScene(self, xNudge = 0, yNudge = 0):

    #def setPosition(self, newXPos = None, newYPos = None):

    #def getXPos(self):

    #def getYPos(self):

    #def getXSize(self):

    #def getYSize(self):

    #@def scaleObjects(self, newXSize = None, newYSize = None):

    #def scaleScene(self, newXSize = None, newYSize = None):

    #def updateAnimations(self, t):

    #def nextFrame(self):
