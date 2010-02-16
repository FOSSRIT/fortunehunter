from gettext import gettext as _
from constants import CHAR_PATH
class InvalidEnemyException(Exception): pass

import pygame
from Actor import Actor
ENEMY = {
    '1':{'name':_('Wizard Adept'),'img':"concept_wizard.gif",'hp':20,'att':2,'weak':'special'},
    '2':{'name':_('Goblin'),'img':"concept_goblin.gif",'hp':40,'att':3,'weak':'fire'},
    '3':{'name':_('Orc'),'img':"concept_orc.gif",'hp':50,'att':5,'weak':'lightning'},
    '4':{'name':_('Stone Golem'),'img':"concept_orc.gif",'hp':10,'att':6,'weak':'missile'},
    '5':{'name':_('Serratula'),'img':"Crab.png",'hp':125,'att':12,'weak':'crit'},
    '6':{'name':_('Feren'),'img':"merchant.gif",'hp':200,'att':10,'weak':'special'},
    '7':{'name':_('Cave Crab'),'img':"Crab.png",'hp':50,'att':7,'weak':'missile'},
    '8':{'name':_('Frost Giant'),'img':"frost_giant.gif",'hp':45,'att':9,'weak':'fire'}
}

class Enemy(Actor):
    def __init__(self, id):
        Actor.__init__(self)

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

    #returns player's current attack power
    def attackPower(self,name):
        if name=="basic":
            return self.ATT+self.BAE
        elif name=="critical":
            return int((self.ATT+self.BAE) * 1.5)
        elif name=="special":
            return int((self.ATT+self.BAE) * 1.3)


def get_enemy(key):
    if key in ENEMY:
        return Enemy( key )
    else:
        raise InvalidEnemyException()

