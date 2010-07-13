import pygame
from DrawableObject import DrawableObject 

class DynamicDrawableObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,images,textfileName,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):

        DrawableObject.__init__(self, images, textfileName, fps, x, y, xVelocity, yVelocity)

    def addImages(self, images):

        self._images.extend(images)

    def update(self, t):

        timePassed = t - self._last_update
        if timePassed > self._delay:

            frameChanges = int(timePassed/self._delay)
            self._frame += frameChanges
            while self._frame >= len(self._images):

              framesPast = self._frame - len(self._images)
              self._frame = framesPast - 1

            self.image = self._images[self._frame]
            self._last_update = t

    def updateAnimation(self, t, animName):

        timePassed = t - self._last_update
        if timePassed > self._delay:

            if self._frame < self.animations.get(animName)[0] or self._frame > self.animations.get(animName)[1]:

              self._frame = self.animations.get(animName)[0]

            frameChanges = int(timePassed/self._delay)
            self._frame += frameChanges
            while self._frame >= self.animations.get(animName)[1]:

              framesPast = self._frame - self.animations.get(animName)[1]
              self._frame = framesPast - 1 + self.animations.get(animName)[0]

            self.image = self._images[self._frame]
            self._last_update = t

    def nextFrame(self):

        self._frame += 1
        if self._frame >= len(self._images):

            framesPast = self._frame - len(self._images)
            self._frame = framesPast

        self.image = self._images[self._frame]

    def nextAnimFrame(self, animName):

        if self._frame < self.animations[animName][0] or self._frame > self.animations[animName][1]:
            
            self._frame = self.animations[animName][0]

        self._frame += 1
        if self._frame > self.animations[animName][1]:

            framesPast = self._frame - self.animations[animName][1]
            self._frame = framesPast - 1 + self.animations[animName][0]
            
        self.image = self._images[self._frame]
