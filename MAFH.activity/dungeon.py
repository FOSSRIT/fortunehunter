import pippy, pygame, sys, math
from map import *
from room import *
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

class Dungeon:
  def __init__(self,sizeX=5,sizeY=5,fileName="dungeon2.txt"):
    self.sizeX=sizeX
    self.sizeY=sizeY
    self.fileName=fileName
    self.types=["none","Wizard","Goblin","Gru","Eye","Octopus"]
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
      if line[4]=='T':
        rm.transport=True
      self.rooms[(currentX,currentY)]=rm
      ###update position in array###
      currentX+=1

      if currentX==self.sizeX:
        currentY+=1
        currentX=0

      if currentY>self.sizeY:
        break

