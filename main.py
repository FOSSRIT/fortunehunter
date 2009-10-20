import pippy, pygame, sys
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
  def __init__(self,sizeX=5,sizeY=5,fileName="dungeon.txt"):
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
      print(line)
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
      print(currentX,currentY)
      rm=Room(doorN,doorS,doorE,doorW,shop,line[5],line[6],line[7],line[8])
      self.rooms[(currentX,currentY)]=rm
      ###update position in array###
      currentX+=1
      if currentX>self.sizeX:
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
    self.rectSizeX=300/(self.sizeX+1)
    self.rectSizeY=200/(self.sizeY+1)
    self.rects={}
    for y in range(self.sizeY+1):
      for x in range(self.sizeX+1):
        curRect=pygame.Rect(x*self.rectSizeX,(y*self.rectSizeY)+700,self.rectSizeX,self.rectSizeX)
        self.rects[(x,y)]=curRect
    ##usage:  from draw loop: if player moves into an unvisited room,
        ###                   fill in map rectangle a certain color
        ####                  Also, fill current room a different color
    
      
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
#####################################################################
#                           LOADING AREA
#################################################################
#set up sprite groups
currentRoomSprite=pygame.sprite.Sprite()
currentRoomSprite.image=pygame.image.load("/home/olpc/images/beyond_zork.jpg")
currentRoomSprite.rect=pygame.Rect(0,0,1200,700)

roomSprite2=pygame.sprite.Sprite()
roomSprite2.image=pygame.image.load("/home/olpc/images/zork2.gif")
roomSprite2.rect=currentRoomSprite.rect

mapSprite=pygame.sprite.Sprite()
mapSprite.image=pygame.image.load("/home/olpc/images/TreasureMap.jpg")
mapSprite.rect=(0,700,300,200)

3DoorRoomSprite=pygame.sprite.Sprite()
3DoorRoomSprite.image=pygame.image.load("/home/olpc/images/3Doors.png")
3DoorRoomSprite.rect=pygame.Rect(0,0,1200,700)

FrontRightDoorsSprite=pygame.sprite.Sprite()
FrontRightDoorsSprite.image=pygame.image.load("/home/olpc/images/FandRDoors.png")
FrontRightDoorsSprite.rect=currentRoomSprite.rect

FrontDoorRoomSprite=pygame.sprite.Sprite()
FrontDoorRoomSprite.image=pygame.image.load("/home/olpc/images/FDoor.png")
FrontDoorRoomSprite.rect=(0,700,300,200)

LeftFrontDoorsRoomSprite=pygame.sprite.Sprite()
LeftFrontDoorsRoomSprite.image=pygame.image.load("/home/olpc/images/LandFDoors.png")
LeftFrontDoorsRoomSprite.rect=pygame.Rect(0,0,1200,700)

LeftRightDoorsRoomSprite=pygame.sprite.Sprite()
LeftRightDoorsRoomSprite.image=pygame.image.load("/home/olpc/images/LandRDoors.png")
LeftRightDoorsRoomSprite.rect=currentRoomSprite.rect

LeftDoorRoomSprite=pygame.sprite.Sprite()
LeftDoorRoomSprite.image=pygame.image.load("/home/olpc/images/LDoor.png")
LeftDoorRoomSprite.rect=(0,700,300,200)

NoDoorsRoomSprite=pygame.sprite.Sprite()
NoDoorsRoomSprite.image=pygame.image.load("/home/olpc/images/NoDoors.png")
NoDoorsRoomSprite.rect=currentRoomSprite.rect

RightDoorRoomSprite=pygame.sprite.Sprite()
RightDoorRoomSprite.image=pygame.image.load("/home/olpc/images/RDoor.png")
RightDoorRoomSprite.rect=(0,700,300,200)


currentRoomGraphic=pygame.sprite.Group(currentRoomSprite)
mapScreen=pygame.sprite.Group(mapSprite)

# create a Font object from a file, or use the default
# font if the file name is None. size param is height
# in pixels

# usage: pygame.font.Font(filename|object, size)
font = pygame.font.Font(None, fsize)
msg = "Hello!"
msg1="this is  line 1"
msg2="this is  line 2"
msg3="this is  line 3"
msg4="this is  line 4"
msg5="this is  line 5"

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

#####Traversal testing
dgn=Dungeon(5,0,"/home/olpc/TreasureHunters/dungeon.txt")
dgn.fill()
currentRoom=Room(False,False,False,False,False,0,0,0,0)
currentX=0
currentY=0
currentRoom=dgn.rooms.get((currentX,currentY))
dgnMap=Map(dgn)
###simulate enum
NORTH=0
SOUTH=1
EAST=2
WEST=3
playerFacing=SOUTH

while pippy.pygame.next_frame():

  for event in pygame.event.get():
    #################UPDATE##############################
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      msg1=msg2
      msg2=msg3
      msg3=msg4
      msg4=msg5

      if newKey=='escape':
        sys.exit()
      elif newKey=='[1]':
        msg5='check'
      elif newKey=='[2]':
        msg5='down'
        if currentRoom.doorS:
          screen.fill((0,255,0),dgnMap.rects.get((currentX,currentY)),0)
          currentY-=1
          msg5='You enter room at '+repr(currentX)+','+repr(currentY)
        else:
          msg5='There is no door there'
      elif newKey=='[3]':
        msg5='x'
      elif newKey=='[4]':
        msg5='left'
        if currentRoom.doorW:
          screen.fill((0,255,0),dgnMap.rects.get((currentX,currentY)),0)
          currentX-=1
          msg5='You enter room at '+repr(currentX)+','+repr(currentY)
        else:
          msg5='There is no door there'
      elif newKey=='[5]':
        msg5='check'
      elif newKey=='[6]':
        msg5='right'
        if currentRoom.doorE:
          screen.fill((0,255,0),dgnMap.rects.get((currentX,currentY)),0)
          currentX+=1
          msg5='You enter room at '+repr(currentX)+','+repr(currentY)
        else:
          msg5='There is no door there'
      elif newKey=='[7]':
        msg5='square'
      elif newKey=='[8]':
        msg5='You have been eaten by a gru'
        if currentRoom.doorN:
          screen.fill((0,255,0),dgnMap.rects.get((currentX,currentY)),0)
          currentY+=1
          msg5='You enter room at '+repr(currentX)+','+repr(currentY)
        else:
          msg5='There is no door there'

      elif newKey=='[9]':
        msg5='circle'

      
      currentRoom=dgn.rooms.get((currentX,currentY))
      #currentRoomGroup.remove(currentRoomSprite)
      #currentRoomGroup.add(currentRoom.image)
      if currentRoom.doorE:
        msg5+=' there is a door to the East'
      if currentRoom.doorW:
        msg5+=' there is a door to the West'

  ###############DRAW#########################
  #screen.fill((250,250,250))
  screen.fill(0,bigRect,0)
  # draw the text
  tl1=font.render(msg1,True,(255,255,255))
  tl2=font.render(msg2,True,(255,255,255))
  tl3=font.render(msg3,True,(255,255,255))
  tl4=font.render(msg4,True,(255,255,255))
  tl5=font.render(msg5,True,(255,255,255))

  screen.blit(text, textRect)
  screen.blit(tl1,line1)
  screen.blit(tl2,line2)
  screen.blit(tl3,line3)
  screen.blit(tl4,line4)
  screen.blit(tl5,line5)
  currentRoomGraphic.draw(screen)
  #mapScreen.draw(screen)
  #screen.fill((200,0,200),dgnMap.rects.get((currentX,currentY)),0)
  screen.fill((250,0,0),dgnMap.rects.get((currentX,currentY)),0)

  # update the display
  pygame.display.flip()

