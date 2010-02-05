from gettext import gettext as _
from constants import CHAR_PATH
class InvalidEnemyException(Exception): pass

import pygame

ENEMY = {
    '1':{'name':_('Wizard Adept'),'img':"concept_wizard.gif",'hp':20,'att':3,'weak':'special'},
    '2':{'name':_('Goblin'),'img':"concept_goblin.gif",'hp':40,'att':5,'weak':'fire'},
    '3':{'name':_('Orc'),'img':"concept_orc.gif",'hp':50,'att':6,'weak':'lightning'},
    '4':{'name':_('Stone Golem'),'img':"concept_orc.gif",'hp':10,'att':8,'weak':'missile'},
    #'5':{'name':_('Serratula')},
    #'6':{'name':_('Feren')},
}

class Enemy:
    def __init__(self, id):
        self.MHP    = 12                #maximum health points (base HP)
        self.HP     = 12                #current health points
        self.BHP    = 0             #bonus health points (from equipment)
        self.ATT    = 13                #base attack power
        self.BAE    = 0             #bonus attack power (from equipment)
        self.DEF    = 1             #base defense power
        self.BDE    = 0             #bonus defense  power(from equipment)
        self.weakness=None
        self.eqItems_Ar = []    #equipped items
        self.attacks_Ar = []    #associated array for attack string names and attack power values
        self.eqItem_Ar = []
        self.inv_Ar = []
        self.attacks_Ar = []
        self.sprite=pygame.sprite.Sprite()
        self.place=0

        #load image based on type later
        self.name=ENEMY[id]['name']
        self.sprite.image=pygame.image.load(CHAR_PATH + ENEMY[id]['img'])
        self.HP = ENEMY[id]['hp']
        self.ATT = ENEMY[id]['att']
        self.weakness=ENEMY[id]['weak']
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


def get_enemy(key):
    if key in ENEMY:
        return Enemy( key )
    else:
        raise InvalidEnemyException()

