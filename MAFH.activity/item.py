import pippy, pygame, sys, math
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

#################################################################################
#Item class: stores info about items
#################################################################################
class Item:
  def __init__(self,name,typ):
    self.name=name
    self.type=typ
    self.power=0
    self.buyVal=0
    self.sellVal=0
    self.hidden=False
    self.battle=False

    #WEAPONS
    if self.name=="Ancient Amulet":
      self.power=1
    elif self.name=="Rusted Blade":
      self.power=5
    elif self.name=="Great Sword":
      self.power=15
    elif self.name=="Crescent Sword":
      self.power=25
    elif self.name=="Cardinal":
      self.power=35
    elif self.name=="Sun Moon":
      self.power=50

    #ARMOR
    elif self.name=="Earth Vest":
      self.power=5
    elif self.name=="Wind Breaker":
      self.power=15
    elif self.name=="Flame Leggings":
      self.power=25
    elif self.name=="Dark Cowl":
      self.power=35
    elif self.name=="Celestial Armor":
      self.power=50

    #ACCESSORY
    elif self.name=="Jewel Shard":
      self.power=10
    elif self.name=="Broken Hourglass":
      self.power=10
    elif self.name=="Radiant Vial":
      self.power=20
    elif self.name=="Honor Tome":
      self.power=.2
    elif self.name=="Valor Tome":
      self.power=.2

    #TREASURES
    elif self.name=="Ruby":
      self.sellVal=500
    elif self.name=="Sapphire":
      self.sellVal=500
    elif self.name=="Emerald":
      self.sellVal=500
    elif self.name=="Diamond":
      self.sellVal=500

    #HEALING
    elif self.name=="Remedy":
      self.sellVal=2
      self.buyVal=20
      self.power=.05
    elif self.name=="Elixir":
      self.sellVal=10
      self.buyVal=60
      self.power=.15
    elif self.name=="Panacea":
      self.sellVal=50
      self.buyVal=150
      self.power=.80
    elif self.name=="High Elixir":
      self.sellVal=20
      self.buyVal=100
      self.power=.40
    elif self.name=="Nostrum":
      self.sellVal=100
      self.buyVal=250
      self.power=.5
