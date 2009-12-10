#Map class: stores information about the layout of the dungeon for easy display
###############################################################################
import pippy, pygame, sys, math
from player import *
from hero import *
from enemy import *
from battleEngine import *
from menu import *
from dungeon import *
from room import *
from tutorial import *
from item import *
from pygame.locals import *
from random import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

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
        

