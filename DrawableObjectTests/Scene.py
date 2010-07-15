import pygame

class Scene:

    def __init__(self, drawableObjects):
    
       self._my_Objects = []

       cnt = 0
       while cnt < len(drawableObjects):
           self._my_Objects.append([drawableObjects[cnt],drawableObjects[cnt].getXPos(),drawableObjects[cnt].getYPos()])
           cnt += 1
           
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
       while cnt < len(self._my_Objects):
           if self._my_Objects[cnt][0].getXPos() < lowestX: lowestX = self._my_Objects[cnt][0].getXPos()
           if self._my_Objects[cnt][0].getYPos() < lowestY: lowestY = self._my_Objects[cnt][0].getYPos()
           cnt += 1

       self.xPos = lowestX
       self.yPos = lowestY

    def calcSize(self):
    
       highestX = 0
       highestY = 0
       
       cnt = 0
       while cnt < len(self._my_Objects):
           if self._my_Objects[cnt][0].getXPos() + self._my_Objects[cnt][0].getXSize() > highestX: highestX = self._my_Objects[cnt][0].getXPos() + self._my_Objects[cnt][0].getXSize()
           if self._my_Objects[cnt][0].getYPos() + self._my_Objects[cnt][0].getYSize() > highestY: highestY = self._my_Objects[cnt][0].getYPos() + self._my_Objects[cnt][0].getYSize()
           cnt += 1

       self.xSize = highestX - self.xPos
       self.ySize = highestY - self.yPos
    
    def addObjects(self, newDrawableObjects):

       cnt = 0
       while cnt < len(newDrawableObjects):
           self._my_Objects.append([newDrawableObjects[cnt],newDrawableObjects[cnt].getXPos(),newDrawableObjects[cnt].getYPos()])
           cnt += 1
       
       self.calcPosition()
       self.calcSize()
       self.setRelativePositions()

    def setRelativePositions(self):

       cnt = 0
       while cnt < len(self._my_Objects):
           self._my_Objects[cnt][1] = self._my_Objects[cnt][1] - self.xPos
           self._my_Objects[cnt][2] = self._my_Objects[cnt][2] - self.yPos
           cnt += 1

    def removeObject(self, index):

       if index < len(self._my_Objects): del self._my_Objects[index]

    def getObject(self, index):

       if index < len(self._my_Objects):
          return  self._my_Objects[index]
          
    def getlistSize(self):
       return len(self._my_Objects)

    def moveObjects(self):

       cnt = 0
       while cnt < len(self._my_Objects):

          self._my_Objects[cnt][0].move()
          cnt += 1

       self.calcPosition()
       self.calcSize()
       self.setRelativePositions()

    def moveScene(self, xNudge = 0, yNudge = 0):

       cnt = 0
       while cnt < len(self._my_Objects):

          self._my_Objects[cnt][0].nudge(xNudge, yNudge)
          cnt += 1

       self.calcPosition()

    def setPosition(self, newXPos = None, newYPos = None):

       if newXPos != None: self.xPos = newXPos
       if newYPos != None: self.yPos = newYPos

       cnt = 0
       while cnt < len(self._my_Objects):

          self._my_Objects[cnt][0].setPosition(self.xPos + self._my_Objects[cnt][1], self.yPos + self._my_Objects[cnt][2])
          cnt += 1

    def getXPos(self):
       return xPos

    def getYPos(self):
       return yPos

    def getXSize(self):
       return xSize

    def getYSize(self):
       return ySize

    def scaleObjects(self, newXSize = None, newYSize = None):

       cnt = 0
       while cnt < len(self._my_Objects):
           self._my_Objects[cnt][0].scale(newXSize, newYSize)
           cnt += 1

    def scaleScene(self, newXSize = None, newYSize = None):

       xScale = 1
       yScale = 1

       if newXSize != None: xScale = newXSize/xSize
       if newYSize != None: yScale = newYSize/ySize

       cnt = 0
       while cnt < len(self._my_Objects):
           self._my_Objects[cnt][0].scale(xScale * self._my_Objects[cnt][0].getXSize(), yScale * self._my_Objects[cnt][0].getYSize())
           self._my_Objects[cnt][1] = xScale * self._my_Objects[cnt][1]
           self._my_Objects[cnt][2] = yScale * self._my_Objects[cnt][2]
           cnt += 1

       self.setPosition()

    def updateAnimations(self, t):

       cnt = 0
       while cnt < len(self._my_Objects):

          self._my_Objects[cnt][0].updateCurrentAnimation(t)
          cnt += 1
    
    def nextFrame(self):

       cnt = 0
       while cnt < len(self._my_Objects):

          self._my_Objects[cnt][0].nextFrame()
          pygame.display.blit(self._my_Objects[cnt][0], (self._my_Objects[cnt][0].xPos(), self._my_Objects[cnt][0].yPos()))
          cnt += 1
