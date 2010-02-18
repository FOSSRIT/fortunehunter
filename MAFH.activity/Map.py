import pygame
import math
#################################################################################
  #Map class: stores information about the layout of the dungeon for easy display
###############################################################################
class Map:
  def __init__(self,dgn):
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
          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorS:
          self.fullRooms[(x,y)]=True
          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorE:
          self.fullRooms[(x,y)]=True
          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorW:
          self.fullRooms[(x,y)]=True
          self.totalSurface.fill((255,255,255),curRect,0)
  def drawMacro(self,player,screen):
    player.currentRoomGroup.draw(screen)
    #DRAW LEGEND
    font=pygame.font.SysFont("cmr10",24,False,False)
    macroMap=pygame.transform.scale(self.totalSurface,(self.sizeX*100,self.sizeY*100))
    screen.fill((0,0,0),(200,0,800,700))
    legend=pygame.Surface((200,300))
    legend.fill((255,0,0),(0,0,40,15))
    legend.blit(font.render("LOCKED",True,(255,0,0)),(45,0,30,5))
    legend.fill((150,255,150),(0,25,40,15))
    legend.blit(font.render("OPEN",True,(150,255,150)),(45,25,30,5))
    legend.fill((255,0,255),(0,50,40,15))
    legend.blit(font.render("PUZZLE",True,(255,0,255)),(45,50,30,5))
    legend.fill((255,255,255),(0,75,40,15))
    legend.blit(font.render("EXIT",True,(255,255,255)),(45,75,30,5))
    legend.fill((50,50,50),(0,100,40,15))
    legend.blit(font.render("ENTRANCE",True,(50,50,50)),(45,100,30,5))
    screen.blit(legend,(800,0,300,300))
    screen.blit(macroMap,(200,0,800,700))
    pygame.display.flip()
  def updateMacro(self,player):
    NONE=-1
    PUZZLE=0
    LOCKED=1
    BOTH=2
    UNLOCKED=3
    EXIT=4
    ENTRANCE=5
    self.totalSurface.fill((0,255,0),(player.currentX*40,player.currentY*40,38,38))
    if player.currentRoom.doorN:
      if player.currentRoom.doorNFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==UNLOCKED or player.currentRoom.doorNFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40+5,player.currentY*40,30,5))
    if player.currentRoom.doorS:
      if player.currentRoom.doorSFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==UNLOCKED or player.currentRoom.doorSFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40+5,player.currentY*40+35,30,5))
    if player.currentRoom.doorE:
      if player.currentRoom.doorEFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==UNLOCKED or player.currentRoom.doorEFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40+35,player.currentY*40+5,5,30))
    if player.currentRoom.doorW:
      if player.currentRoom.doorWFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==UNLOCKED or player.currentRoom.doorWFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40,player.currentY*40+5,5,30))

  def display(self,player,screen):
    #pad the total surface with 100x100 pix
    totalPadded=pygame.Surface((self.totalSurface.get_width()+100,self.totalSurface.get_height()+100))
    totalPadded.blit(self.totalSurface,(100,100,self.totalSurface.get_width(),self.totalSurface.get_height()))
    #blit a player-centered map on a new square surface
    mapView=pygame.Surface((200,200))
    sectRect=((self.sizeX-player.currentX+(2-self.sizeX))*40-100,(self.sizeY-player.currentY+(2-self.sizeY))*40-100,300,300)
    mapView.blit(totalPadded,sectRect)
    mapView.fill((250,0,0),(82,82,34,34))
 
    
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
    screen.fill((0,0,0),(0,700,300,1000))
    screen.blit(mapView,(0,700,200,200))      
