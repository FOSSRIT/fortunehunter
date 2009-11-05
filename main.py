import pippy, pygame, sys, math
from pygame.locals import *
from random import *
################################################################################
#Start of external classes and functions
###############################################################################


  ########################################################################
  #Dungeon class:  stores a 2d array of rooms representing the dungeon
  #                reads/parses a text file containing the data for a dungeon
  #######################################################################3
class Dungeon:
  def __init__(self,sizeX=5,sizeY=5,fileName="dungeon2.txt"):
    self.sizeX=sizeX
    self.sizeY=sizeY
    self.fileName=fileName
    ###INITALIZE DICTIONARY, TUPLE:ROOM PAIRINGS
    self.rooms={}
  def fill(self):
    #####open text file######
    dgnFile=open(self.fileName,'r')
    currentX=0
    currentY=0
    for line in dgnFile:
      ###print line for testing###

      ###initialize room variables###
      doorN=False
      doorS=False
      doorE=False
      doorW=False
      shop=False
      en1=0
      en2=0
      en3=0
      en4=0
      ###check characters in current line, set variables accordingly###
      ###KEY:1st character=door to north
      ###    2nd=door to south
      ###    3rd=door to east
      ###    4th=door to west
      ###    5th=if the room is a shop
      ###    6-9=enemy number in each slot (0 for no enemy)
      if line[0]=='N':
        doorN=True
      if line[1]=='S':
        doorS=True
      if line[2]=='E':
        doorE=True
      if line[3]=='W':
        doorW=True
      if line[4]=='S':
        shop=True
      rm=Room(doorN,doorS,doorE,doorW,shop,line[5],line[6],line[7],line[8])
      #print(rm.getData())
      #print(repr(currentX)+", "+repr(currentY))
      self.rooms[(currentX,currentY)]=rm
      ###update position in array###
      currentX+=1
      if currentX==self.sizeX:
        currentY+=1
        currentX=0
      if currentY>self.sizeY:
        break
      
      
##################################################################################
#Room class: stores data about a room in the dungeon.  IE doors, enemies, mood etc
####################################################################################
class Room:
  def __init__(self,doorN=False,doorS=False,doorE=False,doorW=False,shop=False,en1=0,en2=0,en3=0,en4=0):
    self.doorN=doorN
    self.doorS=doorS
    self.doorE=doorE
    self.doorW=doorW
    self.shop=shop
    self.en1=en1
    self.en2=en2
    self.en3=en3
    self.en4=en4
    self.image=0
  #######To string method########
  def getData(self):
    string=""
    string+=repr(self.doorN)+repr(self.doorS)+repr(self.doorE)+repr(self.doorW)
    string+=self.en1+self.en2+self.en3+self.en4
    return(string)
  def setImage(self,imagePath):
    self.image=pygame.image.load(imagePath)


#################################################################################
  #Map class: stores information about the layout of the dungeon for easy display
###############################################################################
class Map:
  def __init__(self,dgn=Dungeon(0,0,'')):
    self.sizeX=dgn.sizeX
    self.sizeY=dgn.sizeY
    self.rectSizeX=38
    self.rectSizeY=38
    self.rects={}
    self.fullRooms={}
    self.totalSurface=pygame.Surface((self.sizeX*40,self.sizeY*40))
    for y in range(self.sizeY):
      for x in range(self.sizeX):
        curRect=pygame.Rect(x*40,y*40,self.rectSizeX,self.rectSizeX)
        self.rects[(x,y)]=curRect
        if dgn.rooms.get((x,y)).doorN:
          self.fullRooms[(x,y)]=True
          print(repr(x)+", "+repr(y)+" True")
          self.totalSurface.fill((255,255,255),curRect,0)
        elif dgn.rooms.get((x,y)).doorS:
          self.fullRooms[(x,y)]=True
          print(repr(x)+", "+repr(y)+" True")
          self.totalSurface.fill((255,255,255),curRect,0)
        elif dgn.rooms.get((x,y)).doorE:
          self.fullRooms[(x,y)]=True
          print(repr(x)+", "+repr(y)+" True")
          self.totalSurface.fill((255,255,255),curRect,0)
        elif dgn.rooms.get((x,y)).doorW:
          self.fullRooms[(x,y)]=True
          print(repr(x)+", "+repr(y)+" True")
          self.totalSurface.fill((255,255,255),curRect,0)
  def display(self,player,screen):
    
    mapView=pygame.transform.chop(self.totalSurface,(0,0,0,0))
    mapView.fill((255,0,0),(player.currentX*40,player.currentY*40,38,38))
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    angle=0

    if player.playerFacing==NORTH:
      angle=0
      mapView=pygame.transform.rotate(mapView,angle)
      angle=90
    elif player.playerFacing==SOUTH:
      angle=180
      mapView=pygame.transform.rotate(mapView,angle)
      angle=270
    elif player.playerFacing==EAST:
      angle=90
      mapView=pygame.transform.rotate(mapView,angle)
      angle=0
    elif player.playerFacing==WEST:
      angle=270
      mapView=pygame.transform.rotate(mapView,angle)
      angle=180
    angle=angle*(math.pi/180)
    

    curSect=pygame.Rect(0,700,200,200)

    curSect.top+=((player.currentX*40-81)*math.cos(angle))-((player.currentY*40-81)*math.sin(angle))

    curSect.left-=((player.currentX*40-81)*math.sin(angle))+((player.currentY*40-81)*math.cos(angle))

    screen.fill(0,(0,700,200,300),0)
    screen.blit(mapView,curSect)
    screen.fill(0,(200,700,1200,300),0)
        

###########################################################################
#  Menu class:  contains a list of options (which can be other menus)
#               has a background image as well as images for each option
###########################################################################
class Menu:
    def __init__(self,options,player,bgImageFile,optionImageFiles,name):
        self.options=options
        self.currentOption=0
        self.background=pygame.sprite.Sprite()
        self.background.image=pygame.image.load(bgImageFile)
        self.background.rect=pygame.Rect(0,0,1290,900)
        self.optionsImages=[]
        i=0
        for name in optionImageFiles:
            sprite=pygame.sprite.Sprite()
            sprite.image=pygame.image.load(name)
            sprite.rectangle=pygame.Rect(430,(i+5)*40,1290,40)
            self.optionsImages.append(sprite)
            i+=1
        self.size=i
    def draw(self,group,screen):
        group.empty()
        i=0
        for image in self.optionsImages:
            if i==self.currentOption:
                image.rect=pygame.Rect(460,(i+5)*40,1290,40)
            else:
                image.rect=pygame.Rect(430,(i+5)*40,1290,40)
            group.add(image)
            i+=1
        bgGroup=pygame.sprite.Group(self.background)
        bgGroup.draw(screen)
        group.draw(screen)
        pygame.display.flip()
    def select(self,direction):
        if direction=="up":
            if self.currentOption>0:
                self.currentOption-=1
            else:
                self.currentOption=0
        else:
            if self.currentOption<self.size:
                self.currentOption+=1
            else:
                self.currentOption=self.size
    def progress(self,player,screen):
        if type(self.options[self.currentOption])==type(self):
            player.currentMenu=self.options[self.currentOption]
            player.previousMenu=self
        else:
            self.updateByName(self.options[self.currentOption],player,screen)
    def regress(self,player):
        temp=player.currentMenu
        player.currentMenu=player.previousMenu
        player.previousMenu=temp
    def updateByName(self,name,player,screen):
        if name=="New Game":
            player.traversal=True
            player.mainMenu=False
            setImage(player)
            player.currentRoomGroup.draw(screen)
            pygame.display.flip()
        elif name=="Close":
            sys.exit()
        elif name=="Tutorial":
            player.tutorial=True
        #WILL ADD MORE OPTIONS LATER
######################################################################
#Tutorial Class: stores image list, traverses through list
######################################################################
class Tutorial:
    def __init__(self,imageList):
        self.currentIndex = 0
        self.images=[]
        i=0
	
        for image in imageList:
            spt=pygame.sprite.Sprite()
            spt.image=pygame.image.load(image)
            spt.rect=pygame.Rect(0,0,1290,700)
	    
	    self.images.append(spt)
            #self.images[i]=spt
           # i+=1
       	    self.size=len(imageList)
    def next(self):
	
    	if  self.currentIndex >= (self.size - 1):
       	 	self.currentIndex+=1
    	else:
		player.mainmenu = true
		player.intutorial = false

    def previous(self):
        self.currentIndex-=1
    def draw(self,group,screen):
        group.empty()
        group.add(self.images[self.currentIndex])
        group.draw(screen)
        screen.flip()
            
################################################################################
# Player Class: stores info about the player ie. current position in dungeon etc
#########################################################################
class Player:
  ####LOADS EVERYTHING FOR THE GAME####
  def __init__(self,x=0,y=0):
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2

    self.initializeMenu()
    self.loadTutorial()
    self.loadImages()
    #state variables
    self.inTutorial=False
    self.mainMenu=True
    self.traversal=False
    self.waiting=False
    self.battle=False
    self.statMenu=False
    
    #traversal variables
    self.currentX=x
    self.currentY=y
    self.dgn=Dungeon(5,5,"/home/olpc/images/dungeon2.txt")
    self.dgn.fill()
    #self.currentRoom=Room(False,False,False,False,False,0,0,0,0)
    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))
    self.dgnMap=Map(self.dgn)

    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))
    self.playerFacing=SOUTH

    #sound
    self.doorEffect=pygame.mixer.Sound("/home/olpc/images/door.wav")
  def initializeMenu(self):
    mainMenuImages=["/home/olpc/images/tutorial.gif","/home/olpc/images/new.gif","/home/olpc/images/close.gif"]
    self.MainMenu=Menu(["Tutorial","New Game","Close"],self,"/home/olpc/images/mainBG.gif",mainMenuImages,"Main Menu")
    self.currentMenu=self.MainMenu
  def loadTutorial(self):
    tutorialImages=["/home/olpc/images/t1.gif","/home/olpc/images/t2.gif","/home/olpc/images/t3.gif"]
    self.tutorial=Tutorial(tutorialImages)
  def loadImages(self):
    self.currentRoomSprite=pygame.sprite.Sprite()
    self.currentRoomSprite.image=pygame.image.load("/home/olpc/images/beyond_zork.jpg")
    self.currentRoomSprite.rect=pygame.Rect(0,0,1200,700)

    self.Black=pygame.sprite.Sprite()
    self.Black.image=pygame.image.load("/home/olpc/images/Black.gif")
    self.Black.rect=pygame.Rect(0,0,1200,700)

    self.FLRSprite=pygame.sprite.Sprite()
    self.FLRSprite.image=pygame.image.load("/home/olpc/images/flr.gif")
    self.FLRSprite.rect=self.currentRoomSprite.rect

    self.FRSprite=pygame.sprite.Sprite()
    self.FRSprite.image=pygame.image.load("/home/olpc/images/fr.gif")
    self.FRSprite.rect=self.currentRoomSprite.rect

    self.FSprite=pygame.sprite.Sprite()
    self.FSprite.image=pygame.image.load("/home/olpc/images/f.gif")
    self.FSprite.rect=self.currentRoomSprite.rect

    self.FLSprite=pygame.sprite.Sprite()
    self.FLSprite.image=pygame.image.load("/home/olpc/images/fl.gif")
    self.FLSprite.rect=self.currentRoomSprite.rect

    self.LRSprite=pygame.sprite.Sprite()
    self.LRSprite.image=pygame.image.load("/home/olpc/images/lr.gif")
    self.LRSprite.rect=self.currentRoomSprite.rect

    self.LSprite=pygame.sprite.Sprite()
    self.LSprite.image=pygame.image.load("/home/olpc/images/l.gif")
    self.LSprite.rect=self.currentRoomSprite.rect

    self.NoSprite=pygame.sprite.Sprite()
    self.NoSprite.image=pygame.image.load("/home/olpc/images/_.gif")
    self.NoSprite.rect=self.currentRoomSprite.rect

    self.RSprite=pygame.sprite.Sprite()
    self.RSprite.image=pygame.image.load("/home/olpc/images/r.gif")
    self.RSprite.rect=self.currentRoomSprite.rect

    self.currentRoomGroup=pygame.sprite.Group(self.currentRoomSprite)

    
# always need to init first thing
pygame.init()


# turn off cursor
pygame.mouse.set_visible(False)

# XO screen is 1200x900
size = width, height = 1200, 900

# we'll use 36 pixel high text
fsize = 36


# create the window and keep track of the surface
# for drawing into
screen = pygame.display.set_mode(size)

# create a Font object from a file, or use the default
# font if the file name is None. size param is height
# in pixels

font = pygame.font.Font(None, fsize)
msg = "Hello!"
msg1=""
msg2=""
msg3=""
msg4=""
msg5=""

# Font.render draws text onto a new surface.
#
# usage: Font.render(text, antialias, color, bg=None)
text = font.render(msg, True, (255,255,255))
tl1=font.render(msg1,True,(255,255,255))
tl2=font.render(msg2,True,(255,255,255))
tl3=font.render(msg3,True,(255,255,255))
tl4=font.render(msg4,True,(255,255,255))
tl5=font.render(msg5,True,(255,255,255))

# the Rect object is used for positioning
bigRect = text.get_rect()
textRect=text.get_rect()
line1=pygame.Rect(300,700,800,36)
line2=pygame.Rect(300,736,800,36)
line3=pygame.Rect(300,772,800,36)
line4=pygame.Rect(300,808,800,36)
line5=pygame.Rect(300,844,800,36)

# start at the top left
bigRect.left = 300
bigRect.top = 700
bigRect.width=1000
bigRect.height=300

#####Functions for main class######
def enterRoom(direction,player,screen):
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    
    if direction=='north':
        player.currentY-=1
        player.playerFacing=NORTH
    elif direction=='south':
        player.currentY+=1
        player.playerFacing=SOUTH
    elif direction=='east':
        player.currentX+=1
        player.playerFacing=EAST
    elif direction=='west':
        player.currentX-=1
        player.playerFacing=WEST
    else:
        print(direction)
    player.currentRoom=player.dgn.rooms.get((player.currentX,player.currentY))

    player.doorEffect.play()

    player.currentRoomGroup.remove(player.currentRoomSprite)
    player.currentRoomSprite=player.Black
    player.currentRoomGroup.add(player.currentRoomSprite)
    player.currentRoomGroup.draw(screen)
    player.waiting=True
    #player.traversal=False
    
    #setImage(player)
    return("You enter room at "+repr(player.currentX)+", "+repr(player.currentY))

def setImage(player):
    fileName=""
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    ###Set up string for testing
    if player.playerFacing==NORTH:
        if player.currentRoom.doorN:
            fileName+="F"
        if player.currentRoom.doorW:
            fileName+="L"
        if player.currentRoom.doorE:
            fileName+="R"
    elif player.playerFacing==SOUTH:
        if player.currentRoom.doorS:
            fileName+="F"
        if player.currentRoom.doorE:
            fileName+="L"
        if player.currentRoom.doorW:
            fileName+="R"
    elif player.playerFacing==EAST:
        if player.currentRoom.doorE:
            fileName+="F"
        if player.currentRoom.doorN:
            fileName+="L"
        if player.currentRoom.doorS:
            fileName+="R"
        
    elif player.playerFacing==WEST:
        if player.currentRoom.doorW:
            fileName+="F"
        if player.currentRoom.doorS:
            fileName+="L"
        if player.currentRoom.doorN:
            fileName+="R"
    ###set sprite depending on string
    player.currentRoomGroup.empty()
    if fileName=="F":
        player.currentRoomSprite=player.FSprite
    elif fileName=="FL":
        player.currentRoomSprite=player.FLSprite
    elif fileName=="FR":
        player.currentRoomSprite=player.FRSprite
    elif fileName=="FLR":
        player.currentRoomSprite=player.FLRSprite
    elif fileName=="LR":
        player.currentRoomSprite=player.LRSprite
    elif fileName=="L":
        player.currentRoomSprite=player.LSprite
    elif fileName=="R":
        player.currentRoomSprite=player.RSprite
    else:
        player.currentRoomSprite=player.NoSprite
    player.currentRoomGroup.add(player.currentRoomSprite)

    
def checkDoor(direction,player,screen):
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    currentX=player.currentX
    currentY=player.currentY
    playerFacing=player.playerFacing
    currentRoom=player.currentRoom
    if direction=='down': 
         print("down pressed")
    elif direction=='up':
         if playerFacing==NORTH:
            if currentRoom.doorN:
                return(enterRoom('north',player,screen))
            else:
                return("There is no door in front of you")
         elif playerFacing==SOUTH:
            if currentRoom.doorS:
                return(enterRoom('south',player,screen))
            else:
                return("There is no door in front of you")
         elif playerFacing==EAST:
            if currentRoom.doorE:
                return(enterRoom('east',player,screen))
            else:
                return("There is no door in front of you")
         elif playerFacing==WEST:
            if currentRoom.doorW:
                return(enterRoom('west',player,screen))
            else:
                return("There is no door in front of you")
                
    elif direction=='left':
        if playerFacing==NORTH:
            player.playerFacing=WEST
            #setImage(player)
            return('You are now facing West')
        elif playerFacing==SOUTH:
            player.playerFacing=EAST
            #setImage(player)
            return('You are now facing East')
        elif playerFacing==EAST:
            player.playerFacing=NORTH
            #setImage(player)
            return('You are now facing North')
        elif playerFacing==WEST:
            player.playerFacing=SOUTH
            #setImage(player)
            return('You are now facing South')
    elif direction=='right':
        if playerFacing==NORTH:
            player.playerFacing=EAST
            #setImage(player)
            return('You are now facing East')
        elif playerFacing==SOUTH:

            player.playerFacing=WEST
            #setImage(player)
            return('You are now facing West')
        elif playerFacing==EAST:
            player.playerFacing=SOUTH
            setImage(player)
            return('You are now facing South')
        elif playerFacing==WEST:
            player.playerFacing=NORTH
            #setImage(player)
            return('You are now facing North')
    else:
        print(direction)

###Update methods###
def updateMenu(event,player):
    menu=player.currentMenu
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      if newKey=='escape':
        sys.exit()
      elif newKey=='[1]':
        menu.progress(player,screen)
      elif newKey=='[2]':
        menu.select("down")
      elif newKey=='[3]':
        menu.regress(player)
      elif newKey=='[4]':
        print("left")
      elif newKey=='[5]':
        print('check')
      elif newKey=='[6]':
        print('right')
      elif newKey=='[7]':
        print('square')
      elif newKey=='[8]':
        menu.select("up")
      elif newKey=='[9]':
        print('circle')

def updateTraversal(event,player,screen):
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      #msg1=msg2
      #msg2=msg3
      #msg3=msg4
      #msg4=msg5
      if newKey=='escape':
        sys.exit()
      elif newKey=='[1]':
        msg5='check'
      elif newKey=='[2]':
        msg5=checkDoor('down',player,screen)
      elif newKey=='[3]':
        msg5='x'
      elif newKey=='[4]':
        msg5=checkDoor('left',player,screen)
      elif newKey=='[5]':
        msg5='check'
      elif newKey=='[6]':
        msg5=checkDoor('right',player,screen)
      elif newKey=='[7]':
        msg5='square'
      elif newKey=='[8]':
        msg5=checkDoor('up',player,screen)
      elif newKey=='[9]':
        msg5='circle'
def updateTutorial(event,player):
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      if newKey=='escape':
        sys.exit()
      elif newKey=='[1]':
        player.tutorial.next()
      elif newKey=='[2]':
        msg5='down'
      elif newKey=='[3]':
        player.tutorial.previous()
      elif newKey=='[4]':
        player.tutorial.previous()
      elif newKey=='[5]':
        msg5='check'
      elif newKey=='[6]':
        player.tutorial.next()
      elif newKey=='[7]':
        msg5='square'
      elif newKey=='[8]':
        msg5='up'
      elif newKey=='[9]':
        msg5='circle'
def updateWaiting(event,player):
  pygame.time.wait(500)
  player.waiting=False
###Draw methods###
def drawTraversal(player,screen):
      setImage(player)
def drawWaiting(player,screen):
      screen.fill(0,(0,0,1290,700),0)

      
player=Player(0,0)
setImage(player)

#state variables
player.inTutorial=False
player.traversal=False
player.waiting=False
player.battle=False
player.mainMenu=True
player.statMenu=False
   
while pippy.pygame.next_frame():
  
  for event in pygame.event.get():
    if player.traversal:
      if player.waiting:
        updateWaiting(event,player)
      else:
        #################UPDATE##############################
        updateTraversal(event,player,screen)
    elif player.statMenu:
      ##stat menu processes
      updateStatMenu
      print(player.stat)
    elif player.battle:
      ##battle processes
      updateBattle(event)
      print(player.battle)

    elif player.mainMenu:
      ## main menu processes
      updateMenu(event,player)
      print(player.mainMenu)
    elif player.inTutorial:
      updateTutorial(event,player)

  ###############DRAW#########################
  #draw based on state
  if player.mainMenu:
    player.currentMenu.draw(player.currentRoomGroup,screen)
  else:
    screen.fill(0,bigRect,0)
    # draw the text
    tl1=font.render(msg1,True,(255,255,255))
    tl2=font.render(msg2,True,(255,255,255))
    tl3=font.render(msg3,True,(255,255,255))
    tl4=font.render(msg4,True,(255,255,255))
    tl5=font.render(msg5,True,(255,255,255))

    player.dgnMap.display(player,screen)
    screen.blit(text, textRect)
    screen.blit(tl1,line1)
    screen.blit(tl2,line2)
    screen.blit(tl3,line3)
    screen.blit(tl4,line4)
    screen.blit(tl5,line5)
    
    if player.traversal:
      if player.waiting:
        drawWaiting(player,screen)
      else:
        drawTraversal(player,screen)
    elif player.statMenu:
      drawStatMenu(player,screen)
    elif player.battle:
      drawBattle(player,screen)
    elif player.inTutorial:
      player.tutorial.draw(player.currentRoomGroup,screen)

    player.currentRoomGroup.draw(screen)
  # update the display  
  pygame.display.flip()
