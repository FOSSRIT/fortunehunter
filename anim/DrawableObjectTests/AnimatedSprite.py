import pygame

class Spritesheet:
    """
    Class from http://www.scriptedfun.com/transcript-2-using-sprite-sheets-and-drawing-the-background/

    """
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename)#.convert()

    def imgat(self, rect):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size)#.convert()
        image.blit(self.sheet, (0, 0), rect)
        return image

    def imgsat(self, rects):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect))
        return imgs

    def img_extract( self, cols, rows, width, height ):
        rect_list = []
        for y in range(0, rows):
            for x in range(0, cols):
                rect_list.append( (width*x, height*y, width, height) )
        return self.imgsat( rect_list)


class AnimatedSprite(pygame.sprite.Sprite):
    """
    http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/
    """

    def __init__(self,images,textfileName,fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self._images = images

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.animations = {}
        
        if textfileName != '':
           f = open(textfileName, 'r')
           currentLine = f.readline()
           while currentLine != '':
             animValues = currentLine.split(",")
             #This is a list called animations that at each position contains a list of two values. the first value is the start position
             #of the given animation and the second is the end position of the given animation
             self.animations[animValues[0]] =  [int(animValues[1]), int(animValues[2])]
             currentLine = f.readline()

        # Call update to set our first image.
        #self.update(pygame.time.get_ticks())

    def addImages(self, images):

        self._images.extend(images)

    def update(self, t):
        # This method updates the animation in a situation where there is only one animation contained within the object.

        #calculates the amount of time that has passed since the last update
        timePassed = t - self._last_update
        #checks if enough time has passed that it would need to update the frame of the animation
        if timePassed > self._delay:
            #since enough time has passed, it will determine how many times the frame was supposed to change since the last update
            frameChanges = int(timePassed/self._delay)
            #goes to the frame that it should be at right now and skips any frames that would have already been over and done with
            self._frame += frameChanges
            #checks if the current frame is past the final frame and continues to check over and over until it is not
            while self._frame >= len(self._images):
              #since we are past the final frame it is now figuring out how many frames past the final frame we have actually gone
              framesPast = self._frame - len(self._images)
              #sets the current frame to the frame it should be at
              self._frame = framesPast - 1
            #sets the current image to the image associated with the current frame
            self.image = self._images[self._frame]
            #sets the last update value to the current time so that at the next update the time change is accurate
            self._last_update = t

    def updateAnimation(self, t, animName):
        # This method updates the animation based on the start and end frame of the specific animation you are on.
        #This means that if your object contains multiple animations, you can use this method to reference the exact
        #animation that you are using.

        #calculates the amount of time that has passed since the last update
        timePassed = t - self._last_update
        #checks if enough time has passed that it would need to update the frame of the animation
        if timePassed > self._delay:
            #Checks to make sure that the current frame is actually set to a position within the animation
            if self._frame < self.animations.get(animName)[0] or self._frame > self.animations.get(animName)[1]:
              #corrects the position of the current frame
              self._frame = self.animations.get(animName)[0]
            #since enough time has passed, it will determine how many times the frame was supposed to change since the last update
            frameChanges = int(timePassed/self._delay)
            #goes to the frame that it should be at right now and skips any frames that would have already been over and done with
            self._frame += frameChanges
            #checks if the current frame is past the final frame of the current animation and continues to check over and over
            #until it is not
            while self._frame >= self.animations.get(animName)[1]:
              #Determines how many frames past the final frame of the animation it is
              framesPast = self._frame - self.animations.get(animName)[1]
              #Sets the current frame to the frame it should be at
              self._frame = framesPast - 1 + self.animations.get(animName)[0]
            #sets the current image to the image associated with the current frame
            self.image = self._images[self._frame]
            #sets the last update value to the current time so that at the next update the time change is accurate
            self._last_update = t

    def nextFrame(self):
        # This definition is designed to simply move to the next frame.
        # All of the other definitions only move to the nex frame if
        # enough time has passed based on the framerate. With this
        # definition I can go right to the next frame allowing me to
        # see how fast a framerate I can get to and not be limited by 
        # what I define.

        self._frame += 1
        if self._frame >= len(self._images):
            framesPast = self._frame - len(self._images)
            self._frame = framesPast
        self.image = self._images[self._frame]
        
    def nextAnimFrame(self, animName):
        # This definition is designed to simply move to the next frame of the specified animation.
        if self._frame < self.animations[animName][0]:
            self._frame = self.animations[animName][0]

        self._frame += 1
        if self._frame > self.animations[animName][1]:
            framesPast = self._frame - self.animations[animName][1]
            self._frame = framesPast - 1 + self.animations[animName][0]
        self.image = self._images[self._frame]
        
