import pygame

class Scene:

    def __init__(self, drawableObjects):
    
       self._my_Objects = []

       cnt = 0
       while cnt < len(drawableObjects):
           self._my_objects.append(drawableObjects[cnt],[drawableObjects[cnt].getXPos(),drawableObjects[cnt].getYPos()])
    
    def calcPosition(self):
    
    def calcSize(self):
    
    def addObjects(self):
    
    def setRelativePositions(self):
    
    def removeObject(self):
    
    def getObject(self):
    
    def moveObjects(self):
    
    def nudgeScene(self):
    
    def setPosition(self):
    
    def getPosition(self):
    
    def scaleObjects(self):
    
    def scaleScene(self):
    
    def updateAnimations(self):
