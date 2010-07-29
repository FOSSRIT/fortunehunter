import pygame
from pygame.sprite import RenderUpdates

class Scene(pygame.sprite.RenderUpdates):

    def __init__(self, sprites):

       self._spritelist = []
       self._spritelist.append([sprites, sprites.getXPos(), sprites.getYPos()])
       RenderUpdates.__init__(self, sprites)

       self.xPos = 0
       self.yPos = 0
       self.xSize = 0
       self.ySize = 0

       self.calcPosition()
       self.calcSize()
       self.setRelativePositions()

    def calcPosition(self):
    
       lowestX = 9000
       lowestY = 9000
       
       cnt = 0
       while cnt < len(self._spritelist):
           if self._spritelist[cnt][0].getXPos() < lowestX: lowestX = self._spritelist[cnt][0].getXPos()
           if self._spritelist[cnt][0].getYPos() < lowestY: lowestY = self._spritelist[cnt][0].getYPos()
           cnt += 1

       self.xPos = lowestX
       self.yPos = lowestY

    def calcSize(self):
    
       highestX = 0
       highestY = 0
       
       cnt = 0
       while cnt < len(self._spritelist):
           if (self._spritelist[cnt][0].getXPos() + self._spritelist[cnt][0].getXSize()) > highestX: highestX = self._spritelist[cnt][0].getXPos() + self._spritelist[cnt][0].getXSize()
           if (self._spritelist[cnt][0].getYPos() + self._spritelist[cnt][0].getYSize()) > highestY: highestY = self._spritelist[cnt][0].getYPos() + self._spritelist[cnt][0].getYSize()
           cnt += 1

       self.xSize = highestX - self.xPos
       self.ySize = highestY - self.yPos

    def addObject(self, newDrawableObject):

           RenderUpdates.add_internal(self, newDrawableObject)
           self._spritelist.append([newDrawableObject, newDrawableObject.getXPos(), newDrawableObject.getYPos()])
           
    def addObjects(self, newDrawableObjects):
        for sprite in newDrawableObjects:
           RenderUpdates.add_internal(self, sprite)
           self._spritelist.append([sprite, sprite.getXPos(), sprite.getYPos()])

    def setRelativePositions(self):

       cnt = 0
       while cnt < len(self._spritelist):
           self._spritelist[cnt][1] = self._spritelist[cnt][0].getXPos() - self.xPos
           self._spritelist[cnt][2] = self._spritelist[cnt][0].getYPos() - self.yPos
           cnt += 1

    def removeObject(self, sprite):
       RenderUpdates.remove_internal(self, sprite)
       #self._spritelist.remove(sprite)


    def getObject(self, index):

       if index < len(self._spritelist):
          return  self._spritelist[index][0]

    def getListSize(self):

       return len(self._spritelist)

    def getList(self):

       return list(self._spritelist)

    def moveObjects(self):

       cnt = 0
       while cnt < len(self._spritelist):

          self._spritelist[cnt][0].move()
          cnt += 1

       self.calcPosition()
       self.calcSize()
       self.setRelativePositions()

    def moveScene(self, xNudge = 0, yNudge = 0):

       cnt = 0
       while cnt < len(self._spritelist):

          self._spritelist[cnt][0].nudge(xNudge, yNudge)
          cnt += 1

       self.calcPosition()

    def setPosition(self, newXPos = None, newYPos = None):

       if newXPos != None: self.xPos = newXPos
       if newYPos != None: self.yPos = newYPos

       cnt = 0
       while cnt < len(self._spritelist):

          self._spritelist[cnt][0].setPosition(self.xPos + self._spritelist[cnt][1], self.yPos + self._spritelist[cnt][2])
          cnt += 1

    def getXPos(self):
       return self.xPos

    def getYPos(self):
       return self.yPos

    def getXSize(self):
       return self.xSize

    def getYSize(self):
       return self.ySize

    def scaleObjects(self, newXSize = None, newYSize = None):

       cnt = 0
       while cnt < len(self._spritelist):
           self._spritelist[cnt][0].scale(newXSize, newYSize)
           cnt += 1

    def scaleScene(self, newXSize = None, newYSize = None):

       self.calcPosition()
       self.calcSize()

       xScale = 1
       yScale = 1

       if newXSize != None: xScale = (newXSize * 1.0)/self.xSize
       if newYSize != None: yScale = (newYSize * 1.0)/self.ySize

       cnt = 0
       while cnt < len(self._spritelist):
           self._spritelist[cnt][0].scale(xScale * self._spritelist[cnt][0].getXSize(), yScale * self._spritelist[cnt][0].getYSize())
           self._spritelist[cnt][1] = xScale * self._spritelist[cnt][1]
           self._spritelist[cnt][2] = yScale * self._spritelist[cnt][2]
           cnt += 1

       self.calcPosition()
       self.calcSize()
       self.setPosition()

    def updateAnimations(self, t):

       cnt = 0
       while cnt < len(self._spritelist):

          self._spritelist[cnt][0].updateCurrentAnimation(t)
          cnt += 1

    def nextFrame(self):

       cnt = 0
       while cnt < len(self._spritelist):

          self._spritelist[cnt][0].nextFrame()
          cnt += 1
