import pygame
from DrawableObject import DrawableObject

class DrawableFontObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,text,font,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):

        self.font = font
        self.textImage = font.render(text, 1, (255,255,255))

        DrawableObject.__init__(self, [self.textImage], '', fps, x, y, xVelocity, yVelocity)

    def changeText(self, newText):

        self._images[0] = self.font.render(newText, True, (111,22,45))
        self.image = self._images[0]
