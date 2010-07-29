import pygame
from DrawableObject import DrawableObject

class DrawableFontObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,text,font,fps = 1, x = 0, y = 0, xVelocity = 0, yVelocity = 0):

        self.font = font
        self.textImage = font.render(text, 1, (255,255,255))
        #self._image = self.textImage
        DrawableObject.__init__(self, [self.textImage], '', fps, x, y, xVelocity, yVelocity)

    def changeText(self, newText, color = (0,0,0)):
        self._images[0] = self.font.render(newText, True, color)
        self.image = self._images[0]
