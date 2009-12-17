import pippy, pygame, sys, math
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

################################################################################
#Item class: stores info about items
################################################################################
class Item:
  def __init__(self,name,typ):
    self.name=name
    self.type=typ
    self.power=0
    self.hidden=False
    if self.name=="Potion":
      self.power=20
    elif self.name=="Sword":
      self.power=25
    elif self.name=="Vest":
      self.power=10
    elif self.name=="Ring":
      self.power=5