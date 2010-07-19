import pygame

class DrawableObject(pygame.sprite.Sprite):

    def __init__(self,images,textfileName,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):
        pygame.sprite.Sprite.__init__(self)
        cnt = 0
        
        #self._originals = images
        #self._images = images
        self._images = []
        while cnt < len(images):
            self._images.append(images[cnt][0].convert())
            cnt += 1
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.animations = {}
        self._current_anim = ""
        self.xPos = x
        self.yPos = y
        self.xSpeed = xVelocity
        self.ySpeed = yVelocity
        #self.myAngle = 0
        self.xSize = 40
        self.ySize = 40
        
        if textfileName != '':

           f = open(textfileName, 'r')
           currentLine = f.readline()
           while currentLine != '':

             animValues = currentLine.split(",")
             self.animations[animValues[0]] =  [int(animValues[1]), int(animValues[2])]
             currentLine = f.readline()


    def addImages(self, images):

        self._images.extend(images)
        #self._originals.extend(images)
        
    def goToAnim(self, animName):

        cnt = 0
        while cnt < len(animations):
           
           if animations[cnt] == animName:
             self._current_anim = animName
             self._frame = self.animations[animName][0]
             self.image = self._images[self._frame]
             cnt = len(animations)
           cnt += 1
    
    def move(self):

        self.xPos += self.xSpeed
        self.yPos += self.ySpeed

        self.image[0].get_rect().move(self.xPos,self.yPos)

    def nudge(self, xNudge = 0, yNudge = 0):

        self.xPos += xNudge
        self.yPos += yNudge

        self.image[0].get_rect().move(self.xPos,self.yPos)

    def scale(self, newXSize = None, newYSize = None):

        if newXSize != None: self.xSize = newXSize
        if newYSize != None: self.ySize = newYSize

        cnt = 0
        while  cnt < len(self._images):
            
            self._images[cnt] = pygame.transform.scale(self._images[cnt], (newXSize, newYSize))
            cnt += 1
            
    def getXSize(self):
    
       return self.xSize

    def getYSize(self):

       return self.ySize

    #def rotate(self,angle):

        #self._images = copy.deepcopy(self._originals)

        #cnt = 0

        #self.myAngle += angle
        #while  cnt < len(self._images):

            #self._images[cnt][0] = pygame.transform.rotate(self._images[cnt][0], self.myAngle)
            #cnt += 1

        #self.scale(self.xSize, self.ySize)

    #def getRotation(self):
    
       #return self.myAngle
    
    def setPosition(self, x = None, y = None):
    
       if x != None and x >= 0:  self.xPos = x
       if y != None and y >= 0:  self.yPos = y

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
    
       myColorKey = images[0][0].get_at((0,0))
       setColorKey(myColorKey)

    def setColorKey(self, aColor):

       cnt = 0
       while cnt < len(self._images):
          self._images[cnt][0].set_colorkey(aColor)
          cnt += 1

    def update(self, t):
       pass

    def updateCurrnetAnimation(self, t):
       pass

    def nextFrame(self):
       pass

    def nextCurrentAnimFrame(self):
       pass
