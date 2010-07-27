import pygame

class Spritesheet:
    """
    Class from http://www.scriptedfun.com/transcript-2-using-sprite-sheets-and-drawing-the-background/

    This class is used to seperate sprite sheets into the individual frames contained on them and put them into an array of images.
    """

    def __init__(self, filename):
    #This is the constructor. You pass in a file that contains your frames and it sets it to the sheet property.

        self.sheet = pygame.image.load(filename)#.convert()

    def imgat(self, rect):
    #This definition is called by imgsat and takes an individual frame and creates a seperate image out of it

        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size)#.convert()
        image.blit(self.sheet, (0, 0), rect)
        return image

    def imgsat(self, rects):
    #This definition is called by img_extract. It takes the array of frames and passes them into imgat so they can be turned into usable images.
    #It then takes the returned images and adds them to the final array of frames.

        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect))
        return imgs

    def img_extract( self, cols, rows, width, height ):
    #This definition begins the chain rection of calling all of the other definitions by sending the list of rectangles that are the images
    #into imgsat.

        rect_list = []
        for y in range(0, rows):
            for x in range(0, cols):
                rect_list.append( (width*x, height*y, width, height) )
        return self.imgsat( rect_list)


class AnimatedSprite(pygame.sprite.Sprite):
    """
    http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/
    
    This class is meant to hold the array of images/frames for animation so they can be used to animate.
    """

    def __init__(self,images,textfileName,fps = 10):
    #This is the consrtuctor for the class. It takes in the array of imnages/frames, a text file that explains what frames belong
    #to each animation, and a frame rateat which the animations should run.

        pygame.sprite.Sprite.__init__(self)
        self._images = images

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.animations = {}
        
        #This tests to see if the text file is being used. In a situation where something only has one animation you have
        #no need for the text file and can pass in an empty string to signify this.
        if textfileName != '':
           f = open(textfileName, 'r')
           currentLine = f.readline()
           #This while loop goes through and as long as you have not reached an empty line it continues to read the formatted lines
           while currentLine != '':
             #The lines of text are formatted to contain the name, start frame, and end frame, of each animation
             animValues = currentLine.split(",")
             #animations is a dictionary that uses the name of each animation as the reference and then has a two item list at each 
             #position containing the start and end frame of the corresponding animation
             self.animations[animValues[0]] =  [int(animValues[1]), int(animValues[2])]
             currentLine = f.readline()#Moving on to the next line.

    def addImages(self, images):
        #This definition simply allows you to add more images to your array of images.

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
        # All of the other definitions only move to the next frame if
        # enough time has passed based on the framerate. With this
        # definition I can go right to the next frame allowing me to
        # see how fast a framerate I can get to and not be limited by 
        # what I define.

        #Iterates to the next frame in the animation
        self._frame += 1
        #Checks to make sure it has not gone past the final frame of the animation
        if self._frame >= len(self._images):
            #Since it has gone pastr the final frame it figures out how far past it has gone and corrects it.
            framesPast = self._frame - len(self._images)
            self._frame = framesPast
        #Finally sets the image to the current frame
        self.image = self._images[self._frame]
        
    def nextAnimFrame(self, animName):
        # This definition is designed to simply move to the next frame of the specified animation.
        
        #Checks to make sure that it is actually in the range of the animation's frames
        if self._frame < self.animations[animName][0] or self.frame > self.animations[animName][1]:
            self._frame = self.animations[animName][0]

        #Iterates to the next frame in the animation
        self._frame += 1
        #Checks to make sure it has not gone past the final frame of the animation
        if self._frame > self.animations[animName][1]:
            #Since it has gone pastr the final frame it figures out how far past it has gone and corrects it.
            framesPast = self._frame - self.animations[animName][1]
            self._frame = framesPast - 1 + self.animations[animName][0]
        #Finally sets the image to the current frame
        self.image = self._images[self._frame]
        
