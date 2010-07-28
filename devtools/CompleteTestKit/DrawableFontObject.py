import pygame
from DrawableObject import DrawableObject

class DrawableFontObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,text,font,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):

        self.font = font
        self.textImage = font.render(text, True, (0,0,0))
        DrawableObject.__init__(self, [self.textImage], '', fps, x, y, xVelocity, yVelocity)

    def changeText(self, newtext):

        self._images[0] = font.render(newText, True, (0,0,0))
        
    def update(self, t): # just updates the frame / object

        print "last update     ", self._last_update
        timePassed = t + self._last_update
        print "time passed    ", timePassed
        if (timePassed) > self._delay:
            if self._frame < self.animations.get(self._current_anim)[0] or self._frame > self.animations.get(self._current_anim)[1]:
              self._frame = self.animations.get(self._current_anim)[0]

            self._frame += timePassed/self._delay
            print "frame   ", self._frame

            while self._frame >= self.animations.get(self._current_anim)[1]:
              framesPast = self._frame - self.animations.get(self._current_anim)[1]
              self._frame = framesPast - 1 + self.animations.get(self._current_anim)[0]

            self.image = self._images[self._frame]
            self._last_update = timePassed%self._delay
        else:
           
           self._last_update = timePassed
