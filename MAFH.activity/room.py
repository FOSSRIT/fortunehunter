
import pippy, pygame, sys, math
from item import *
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

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
    #Item("Rusted Blade","Weapon")
    #Item("Great Sword","Weapon")
    #Item("Crescent Sword","Weapon")
    #Item("Cardinal","Weapon")
    #Item("Sun Moon","Weapon")

    #Item("Earth Vest","Armor")
    #Item("Wind Breaker","Armor")
    #Item("Flame Leggings","Armor")
    #Item("Dark Cowl","Armor")
    #Item("Celestial Armor","Armor")

    #Item("Jewel Shard","Accessory")
    #Item("Broken Hourglass","Accessory")
    #Item("Radiant Vial","Accessory")
    #Item("Honor Tome","Accessory")
    #Item("Valor Tome","Accessory")

    #Item("Remedy","Usable")
    #Item("Elixir","Usable")
    #Item("Panacea","Usable")
    #Item("High Elixir","Usable")
    #Item("Nostrum","Usable")

    #Item("Ruby","Special")
    #Item("Sapphire","Special")
    #Item("Emerald","Special")
    #Item("Diamond","Special")

    #Item("Ancient Amulet","Weapon")
    #Item("Small Key","key")
    #Item("Big Key","key")
    #depending on dungeon, item list varies: SUGGESTED FORMAT=usable items, key items, weapon, armor,special items
    #Dungeon 5
    #itemList=[0,Item("Remedy","Usable"),Item("Elixir","Usable"),Item("High Elixir","Usable"),Item("Big Key","key"),Item("Small Key","key"),Item("Sun Moon","Weapon"),Item("Celestial Armor","Armor")]  
    #Dungeon 4
    #itemList=[0,Item("Elixir","Usable"),Item("Panacea","Usable")Item("Big Key","key"),Item("Small Key","key"),Item("Cardinal","Weapon"),Item("Dark Cowl","Armor")]    
    #Dungeon 3
    #itemList=[0,Item("Elixir","Usable"),Item("High Elixir","Usable")Item("Big Key","key"),Item("Small Key","key"), Item("Crescent Sword","Weapon"),Item("Flame Leggings","Armor")]
    #Dungeon 2
    #itemList=[0,Item("Remedy","Usable"),Item("Elixir","Usable"),Item("Big Key","key"),Item("Small Key","key"), Item("Great Sword","Weapon"),Item("Wind Breaker","Armor")]
    #Dungeon 1
    itemList=[0,Item("Remedy","Usable"),Item("Small Key","key"),Item("Big Key","key"),Item("Rusted Blade","Weapon"),Item("Earth Vest","Armor")]
    if not int(self.it1)==0:
      self.it1=itemList[int(self.it1)]
    if not int(self.it2)==0:
      self.it2=itemList[int(self.it2)]
    if not int(self.it3)==0:
      self.it3=itemList[int(self.it3)]
    if not int(self.it4)==0:
      self.it4=itemList[int(self.it4)]
