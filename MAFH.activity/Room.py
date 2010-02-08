from Shop import Shop
from Items import get_item
import pygame.image

##################################################################################
#Room class: stores data about a room in the dungeon.  IE doors, enemies, mood etc
####################################################################################
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

    if it1 != '0':
        self.it1=get_item(it1)
    else:
        self.it1=None

    if it2 != '0':
        self.it2=get_item(it2)
    else:
        self.it2=None

    if it3 != '0':
        self.it3=get_item(it3)
    else:
        self.it3=None

    if it4 != '0':
        self.it4=get_item(it4)
    else:
        self.it4=None

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

  def setShop(self,player):
    self.shop=Shop(player)
