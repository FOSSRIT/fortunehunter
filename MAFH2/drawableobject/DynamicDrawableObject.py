import pygame
from DrawableObject import DrawableObject

class DynamicDrawableObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,images,textfileName,fps = 2, x = 0, y = 0, xVelocity = 0, yVelocity = 0):

        DrawableObject.__init__(self, images, textfileName, fps, x, y, xVelocity, yVelocity)

    def addImages(self, images):

        self._images.extend(images)

    def updateAnim(self, t):

        timePassed = t + self._last_update
        if timePassed > self._delay:

            self._frame += timePassed/self._delay
            while self._frame >= len(self._images):

              framesPast = self._frame - len(self._images)
              self._frame = framesPast - 1

            self.image = self._images[self._frame]
            self._last_update = timePassed%self._delay
        self._last_update = timePassed

    def updateCurrentAnimation(self, t):

        cnt = 0
        while cnt < len(animations):
           
           if animations[cnt] == self._current_anim:
        
              timePassed = t + self._last_update
              if timePassed > self._delay:

                  if self._frame < self.animations.get(self._current_anim)[0] or self._frame > self.animations.get(self._current_anim)[1]: #checking if I am in the animation and putting me there if I am not
      
                    self._frame = self.animations.get(self._current_anim)[0]

                  self._frame += timePassed/self._delay
                  while self._frame >= self.animations.get(self._current_anim)[1]:
      
                    framesPast = self._frame - self.animations.get(self._current_anim)[1]
                    self._frame = framesPast - 1 + self.animations.get(self._current_anim)[0]
      
                  self.image = self._images[self._frame]
                  self._last_update = timePassed%self._delay
              self._last_update = timePassed
                  
              cnt = len(animations)

           cnt += 1

    def nextFrame(self):

        self._frame += 1
        if self._frame >= len(self._images):

            framesPast = self._frame - len(self._images)
            self._frame = framesPast

        self.image = self._images[self._frame]

    def nextCurrentAnimFrame(self):

        cnt = 0
        while cnt < len(animations):
           
           if animations[cnt] == self._current_anim:
              
              if self._frame < self.animations[self._current_anim][0] or self._frame > self.animations[self._current_anim][1]:
                  
                  self._frame = self.animations[self._current_anim][0]
              else:
                  self._frame += 1

              if self._frame > self.animations[self._current_anim][1]:
      
                  framesPast = self._frame - self.animations[self._current_anim][1]
                  self._frame = framesPast - 1 + self.animations[self._current_anim][0]
                  
              self.image = self._images[self._frame]
              
              cnt = len(anmiations)

           cnt += 1
