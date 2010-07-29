import pygame

class DrawableObject(pygame.sprite.Sprite):

    def __init__(self,images, textfileName, x = 0, y = 0,):
        pygame.sprite.Sprite.__init__(self)

        self._images = []
        self._origImages = []

        for i in range(len(images)):
            self._images.append(images[i].convert())
            self._origImages.append(images[i].convert())

        self.image = self._images[0]
        self.rect = self.image.get_rect()
        self.xPos = x
        self.yPos = y
        self.myAngle = 0
        self.xSize = images[0].get_width()
        self.ySize = images[0].get_width()
        self.rect.topleft = (x,y)
        
        if textfileName != '':

           f = open(textfileName, 'r')
           currentLine = f.readline()
           while currentLine != '':

             animValues = currentLine.split(",")
             self.animations[animValues[0]] =  [int(animValues[1]), int(animValues[2])]
             currentLine = f.readline()

    def addImages(self, images):
        for i in range(len(images)):
            self._images.append(images[i].convert())
            self._origImages.append(images[i].convert())

    def goToAnim(self, animName):
      if self.animations.get(animName, 0) != 0:
         self._current_anim = animName
         self._frame = self.animations[animName][0]
         self.image = self._images[self._frame]
         
#
#   Again I took out default values because I don't want the primary function
#   of the method to be effectively overridable and have a method that can
#   do nothing without raising flags
#   I also conformed the parameter naming convention so that it conforms with the
#   other methods' naming convention in this object
#   JT Jul 28 2010
    def nudge(self, x, y):
        self.xPos += x
        self.yPos += y
        self.rect.right += x
        self.rect.top += y

#
#   reworked the loop for efficiency and the if statement logic
#   JT Jul 28 2010
    def scale(self, x=None, y=None):
        if type(x).__name__=='int': self.xSize = x
        if type(y).__name__=='int': self.ySize = y
            
        for i in range(len(self._images)):
            self._origImages[i] = pygame.transform.scale(self._origImages[i], (self.xSize, self.ySize))
            self._images[i] = self._origImages[i]

    def getXSize(self):
       return self.xSize

    def getYSize(self):
       return self.ySize

#
#   I changed rotate to utilize a for instead of a counter/while loop for speed
#   JT - Jul 28 2010
    def rotate(self,angle):
        self.myAngle += angle
        for i in range(len(self._images)):
            self._images[i] = pygame.transform.rotate(self._origImages[i], self.myAngle)

    def getRotation(self):
       return self.myAngle

#
#   I don't recommend forcing people to keep images within the screen
#   a common trick in bullet hells is to temporarily move image objects off-
#   screen when they die so the game isn't constantly loading a new instance of
#   a common enemy
#   JT - Jul 28 2010
    def setPosition(self, x = None, y = None):
        if type(x).__name__=='int': self.xPos = x
        if type(y).__name__=='int': self.yPos = y
        self.rect.topleft = (self.xPos, self.yPos)

    def getXPos(self):
       return self.xPos

    def getYPos(self):
       return self.yPos

#
#   Added defaul values in case someone wants their color key to be taken from bot.right corner, eg
#   JT Jul 28 2010
    def calcColorKey(self, x=0, y=0):
       myColorKey = images[0].get_at((x,y))
       setColorKey(myColorKey)

    def setColorKey(self, aColor):
       for i in range(len(self._images)):
          self._images[i].set_colorkey(aColor)
#
#   Set default value to allow the method to be called empty (since t does nothing atm)
#   JT Jul 28 2010
    def update(self, t=None):
       pass
       
    def nextFrame(self):
       pass

    def nextCurrentAnimFrame(self):
       pass