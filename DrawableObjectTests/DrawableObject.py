import pygame

class DrawableObject(pygame.sprite.Sprite):

    def __init__(self,images,textfileName,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):
        pygame.sprite.Sprite.__init__(self)
        cnt = 0
        
        self._originals = images
        self._images = images
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.animations = {}
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
        self._originals.extend(images)
        
    def goToAnim(self, animName):

        self._frame = self.animations[animName][0]
        self.image = self._images[self._frame]
    
    def move(self):

        self.xPos += self.xSpeed
        self.yPos += self.ySpeed
        
        self.image[0].get_rect().move(self.xPos,self.yPos)

    def scale(self, newXSize, newYSize):
        
        self.xSize = newXSize
        self.ySize = newYSize

        cnt = 0
        while  cnt < len(self._images):
            
            self._images[cnt][0] = pygame.transform.scale(self._originals[cnt][0], (newXSize, newYSize))
            cnt += 1

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
    
       if x != None:  self.xPos = x
       if y != None:  self.yPos = y
    
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
