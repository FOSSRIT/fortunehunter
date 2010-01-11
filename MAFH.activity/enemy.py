import pippy, pygame, sys, math
from player import *
from battleEngine import *
from map import *
from item import *
from pygame.locals import *
from random import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

##############################################################################		
#Enemy class - represents an enemy and holds all of its data
#############################################################
class Enemy:
  def __init__(self,player,name):
#****property********value**********************description**********************#
	self.MHP 	= 12				#maximum health points (base HP)
	self.HP		= 12				#cur print "Fire"rent health points
	self.BHP 	= 0				#bonus health points (from equipment)
	self.ATT 	= 13 				#base attack power
	self.BAE	= 0				#bonus attack power (from equipment)
	self.DEF	= 1				#base defense power
	self.BDE	= 0				#bonus defense  power(from equipment)
	self.eqItems_Ar	= []	#equipped items
	self.attacks_Ar = []	#associated array for attack string names and attack power values
	self.eqItem_Ar = []
	self.inv_Ar = []
	self.attacks_Ar = []
        self.sprite=pygame.sprite.Sprite()
        self.place=0
        #load image based on type later
        self.name=player.dgn.types[int(name)]
        print(self.name)
        if self.name=="Wizard":
          self.sprite.image=pygame.image.load(IMG_PATH+"concept_wizard.gif")
          self.HP=20
          self.ATT=3
        elif self.name=="Goblin":
          self.sprite.image=pygame.image.load(IMG_PATH+"concept_goblin.gif")
          self.HP=40
          self.ATT=10
        elif self.name=="Orc":
          self.sprite.image=pygame.image.load(IMG_PATH+"concept_orc.gif")
          self.HP=60
          self.ATT=35
        else:
          self.sprite.image=pygame.image.load(IMG_PATH+"concept_orc.gif")
          #TODO:  add all enemy types here as artwork is completed
        self.sprite.rect=(200,200,50,300) 

#****ENEMY ACCESSORS*********************************************#
  #returns enemy's maximum health
  def maxHealthPoints(self):
    return (self.HP + self.BHP)	

  #returns enemy's current health
  def healthPoints(self):
    return (self.HP)

  #returns enemy's current attack power
  def attackPower(self):
    return (self.ATT+self.BAE)

  #returns enemy's current defense power
  def defensePower(self):
    return (self.DEF + self.BDE)

  #returns enemy's equipped items
  def equipment(self):
    return self.eqItems_Ar

  #returns enemy's current inventory
  def inventory(self):
    return self.inv_Ar

#returns player's current attack power
  def attackPower(self,name):
    if name=="basic":
      return self.ATT+self.BAE
    elif name=="critical":
      return int((self.ATT+self.BAE) * 1.5)
    elif name=="special":
      return int((self.ATT+self.BAE) * 1.3)
#****ENEMY MUTATORS************************************************#
  #sets enemy's current health
  def setHealth(self,_HP):
    self.HP = _HP

  #sets enemy's bonus health
  def setBonusHP(self,_BHP):
    self.BHP = _BHP

  #sets enemy's bonus attack power (from battle timer)
  def setBonusAP(self,_BAP):
    self.BAP = _BAP

  #sets enemy's bonus attack power (from equipment)
  def setBonusAE(self,_BAE):
    self.BAE = _BAE

  #sets enemy's bonus defense power (from equipment)
  def setBonusDE(self,_BDE):
    self.BDE = _BDE

  #increases enemy's current health by given amount
  def giveHealth(self,_inc):
    self.HP += _inc
    if healthPoints(self) > maxHealthPoints(self):
	setHealth(self,maxHealthPoints(self))

  #enemy is attacked by given damage
  def defendAttack(self,dmg):
    self.HP -= (dmg - self.defensePower())
    if self.HP<0:
      self.HP=0

#****BATTLE ACCESSORS***********************************************#
  #returns player's list of attacks that are currently available for use
  def availableAttacks(self):
    return self.attacks_Ar

#****INVENTORY MUTATORS********************************************#
  #add item to equipment
  def addEquipment(self,_item):
    print("add equip")
      #add  _item to equipment
      #if _item is weapon - add to first slot
      #if _item is armor - add to second slot
      #if _item is consumable - add to slots 3-6
      #remove item from equipment

  def remEquipment(self,_item):
    print("remove equip")
    #remove _item from equipment -- leave cell empty
#end class Enemy
