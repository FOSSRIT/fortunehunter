#Room class: stores data about a room in the dungeon.  IE doors, enemies, mood etc
####################################################################################
import pippy, pygame, sys, math
from player import *
from hero import *
from enemy import *
from battleEngine import *
from menu import *
from dungeon import *
from map import *
from tutorial import *
from item import *
from pygame.locals import *
from random import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

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
    self.transport=False
  #######To string method########
  def getData(self):
    string=""
    string+=repr(self.doorN)+repr(self.doorS)+repr(self.doorE)+repr(self.doorW)
    string+=self.en1+self.en2+self.en3+self.en4
    return(string)

  def setImage(self,imagePath):
    self.image=pygame.image.load(imagePath)

