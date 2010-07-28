import pygame

class DrawableObject(pygame.sprite.Sprite):

    def __init__(self,images,textfileName,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):
        pygame.sprite.Sprite.__init__(self)
        cnt = 0
        
        #self._originals = images
        #self._images = images
        self._images = []
        self._origImages = []
        while cnt < len(images):
            self._images.append(images[cnt].convert_to_alpha())
            self._origImages.append(images[cnt].convert_to_alpha())
            cnt += 1
        self._start = pygame.time.get_ticks()
        self.image = self._images[0]
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.animations = {}
        self._current_anim = ""
        self.rect = self.image.get_rect()
        self.xPos = x
        self.yPos = y
        self.xSpeed = xVelocity
        self.ySpeed = yVelocity
        self.myAngle = 0
        self.xSize = 40
        self.ySize = 40
        self.rect.topleft = (x,y)

        if textfileName != '':

           f = open(textfileName, 'r')
           currentLine = f.readline()
           while currentLine != '':

             animValues = currentLine.split(",")
             self.animations[animValues[0]] =  [int(animValues[1]), int(animValues[2])]
             currentLine = f.readline()

           self.goToAnim("anim1")

        else:
        
            self.animations["anim1"] = [0, len(self._images) - 1]
            self.goToAnim("anim1")

    def addImages(self, images):

        self._images.extend(images)
        #self._originals.extend(images)

    def goToAnim(self, animName):

      if self.animations.get(animName, 0) != 0:
         self._current_anim = animName
         self._frame = self.animations[animName][0]
         self.image = self._images[self._frame]

    def move(self):

        self.xPos += self.xSpeed
        self.yPos += self.ySpeed

        self.rect.right += self.xSpeed
        self.rect.top += self.ySpeed

    def nudge(self, xNudge = 0, yNudge = 0):

        self.xPos += xNudge
        self.yPos += yNudge

        self.rect.right += xNudge
        self.rect.top += yNudge

    def scale(self, newXSize = None, newYSize = None):

        if newXSize != None: self.xSize = newXSize
        if newYSize != None: self.ySize = newYSize

        cnt = 0
        while  cnt < len(self._images):
            self._origImages[cnt] = pygame.transform.scale(self._origImages[cnt], (self.xSize, self.ySize))
            self._images[cnt] = self._origImages[cnt]
            cnt += 1

    def getXSize(self):

       return self.xSize

    def getYSize(self):

       return self.ySize

    def rotate(self,angle):

        cnt = 0

        self.myAngle += angle
        while  cnt < len(self._images):

            self._images[cnt] = pygame.transform.rotate(self._origImages[cnt], self.myAngle)
            cnt += 1

    def getRotation(self):

       return self.myAngle

    def setPosition(self, x = None, y = None):

       if x != None and x >= 0:  self.xPos = x
       if y != None and y >= 0:  self.yPos = y
       
       self.rect.topleft = (self.xPos, self.yPos)

    def getXPos(self):

       return self.xPos

    def getYPos(self):

       return self.yPos

    def setSpeed(self, xVelocity = None, yVelocity = None):

       if xVelocity != None:  self.xSpeed = xVelocity
       if yVelocity != None:  self.ySpeed = yVelocity

    def getXSpeed(self):

       return self.xSpeed

    def getYSpeed(self):

       return self.ySpeed

    def calcColorKey(self):

       myColorKey = images[0].get_at((0,0))
       setColorKey(myColorKey)

    def setColorKey(self, aColor):

       cnt = 0
       while cnt < len(self._images):
          self._images[cnt].set_colorkey(aColor)
          cnt += 1

    def update(self, t):
       pass

    def updateCurrnetAnimation(self, t):
       pass

    def nextFrame(self):
       pass

    def nextCurrentAnimFrame(self):
       pass
