#Room class: stores data about a room in the dungeon.  IE doors, enemies, mood etc
####################################################################################
import pippy, pygame, sys, math
from item import *
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

class Room:
  def __init__(self,doorN,doorNFlag,doorS,doorSFlag,doorE,doorEFlag,doorW,doorWFlag,roomFlag,en1,en2,en3,en4,it1,it2,it3,it4):
    self.doorN=doorN
    self.doorNFlag=doorNFlag
    self.doorS=doorS
    self.doorSFlag=doorSFlag
    self.doorE=doorE
    self.doorEFlag=doorEFlag
    self.doorW=doorW
    self.doorWFlag=doorWFlag
    self.roomFlag=roomFlag

    self.en1=en1
    self.en2=en2
    self.en3=en3
    self.en4=en4

    self.it1=it1
    self.it2=it2
    self.it3=it3
    self.it4=it4
    self.fillItems()
    self.image=0
    self.transport=False
    
  #######To string method########
  def getData(self):
    string=""
    string+=repr(self.doorN)+repr(self.doorS)+repr(self.doorE)+repr(self.doorW)
    string+=self.en1+self.en2+self.en3+self.en4
    return(string)

  def setImage(self,imagePath):
    self.image=pygame.image.load(imagePath)
  def fillItems(self):
    itemList=[0,Item("Remedy","Usable"),Item("Small Key","key"),Item("Sword","Weapon"),Item("Calculator","Special")]
    if not int(self.it1)==0:
      self.it1=itemList[int(self.it1)]
    if not int(self.it2)==0:
      self.it2=itemList[int(self.it2)]
    if not int(self.it3)==0:
      self.it3=itemList[int(self.it3)]
    if not int(self.it4)==0:
      self.it4=itemList[int(self.it4)]

