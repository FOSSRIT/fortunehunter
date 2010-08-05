import pygame
from DrawableObject import DrawableObject

class TestObject:

    def __init__(self, drawableObject):
    
        self.myDrawableObject = drawableObject
        
    def changeSize(self, x, y):
    
        self.myDrawableObject.scale(x,y)
        
    def getDrawable(self):
    
        return self.myDrawableObject