import pygame
from DrawableObject import DrawableObject

class DynamicDrawableObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,images,textfileName,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):

        DrawableObject.__init__(self, images, textfileName, fps, x, y, xVelocity, yVelocity)

    def addImages(self, images):

        self._images.extend(images)

    # def update(self, t):
# 
#         timePassed = t + self._last_update
#         if timePassed > self._delay:
# 
#             self._frame += timePassed/self._delay
#             while self._frame >= len(self._images):
# 
#               framesPast = self._frame - len(self._images)
#               self._frame = framesPast - 1
# 
#             self.image = self._images[self._frame]
#             self._last_update = timePassed%self._delay
#         self._last_update = timePassed

    def updateWithMovement(self, right, bottom): # causes objects to move and collide with walls

         # If we're at the top or bottom of the screen, switch directions.
        if (self.yPos + self.ySize) >= bottom or self.yPos < 0: self.ySpeed = self.ySpeed * -1
        if (self.yPos + self.ySize) >= bottom and self.ySpeed > 0: self.ySpeed = self.ySpeed * -1
        if self.yPos < 0 and self.ySpeed < 0: self.ySpeed = self.ySpeed * -1

        # If we're at the right or left of the screen, switch directions.
        if (self.xPos + self.xSize) >= right or self.xPos < 0: self.xSpeed = self.xSpeed * -1
        if (self.xPos + self.xSize) >= right and self.xSpeed > 0: self.xSpeed = self.xSpeed * -1
        if self.xPos < 0 and self.xSpeed < 0: self.xSpeed = self.xSpeed * -1
 
        self.move()

        if self._frame < len(self._images) - 1:
           self._frame += 1
        else:
           self._frame = 0
           
        self.image = self._images[self._frame]

    def update(self, t): # just updates the frame / object

        print "last update     ", self._last_update
        timePassed = t + self._last_update#getting the time since the last time I updated my frame and adding it to the time that I last updated my frame
        print "time passed    ", timePassed
        if (timePassed) > self._delay:
            if self._frame < self.animations.get(self._current_anim)[0] or self._frame > self.animations.get(self._current_anim)[1]: #checking if I am in the animation and putting me there if I am not
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

    def nextFrame(self): # push to next frame

        self._frame += 1
        if self._frame >= len(self._images):

            framesPast = self._frame - len(self._images)
            self._frame = framesPast

        self.image = self._images[self._frame]

    def nextCurrentAnimFrame(self): # push to the next frame of curr animation

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
