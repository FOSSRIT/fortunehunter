from gettext import gettext as _
from constants import CHAR_PATH
class InvalidEnemyException(Exception): pass

import pygame
from Actor import Actor
from AnimatedSprite import Spritesheet, AnimatedSprite
ENEMY = {
    '1':{'name':_('Wizard Adept'),'img':"concept_wizard.png",'hp':20,'att':2,'weak':'special', 'sprite':(1,1,181,365)},
    '2':{'name':_('Goblin'),'img':"concept_goblin.png",'hp':40,'att':3,'weak':'fire','sprite':(1,1,217,317)},
    '3':{'name':_('Orc'),'img':"concept_orc.png",'hp':50,'att':5,'weak':'lightning','sprite':(1,1,264,338)},
    '4':{'name':_('Stone Golem'),'img':"concept_orc.png",'hp':10,'att':6,'weak':'missile','sprite':(1,1,264,338)},
    '5':{'name':_('Serratula'),'img':"Crab.png",'hp':125,'att':12,'weak':'crit','sprite':(1,1,400,400)},
    '6':{'name':_('Feren'),'img':"faren.png",'hp':1500,'att':10,'weak':'special','sprite':(1,1,250,250)},
    '7':{'name':_('Cave Crab'),'img':"Crab.png",'hp':50,'att':7,'weak':'missile','sprite':(1,1,400,400)},
    '8':{'name':_('Frost Giant'),'img':"frost_giant.png",'hp':45,'att':9,'weak':'fire','sprite':(1,1,250,250)},
    #UPDATE BONESPROUT VALUES
    '9':{'name':_('Bonesprout'),'img':"bonesprout.png",'hp':45,'att':9,'weak':'fire','sprite':(1,1,250,250)},
    'a':{'name':_('anim_test'),'img':"anim_test.gif",'hp':45,'att':9,'weak':'fire','sprite':(3,2, 156, 166)}
}

class Enemy(Actor):
    def __init__(self, id):
        Actor.__init__(self)
        id = 'a'
        self.weakness=None
        self.eqItems_Ar = []    #equipped items
        self.attacks_Ar = []    #associated array for attack string names and attack power values
        self.eqItem_Ar = []
        self.inv_Ar = []
        self.attacks_Ar = []
        col,row,width,height = ENEMY[id]['sprite']
        self.sprite=AnimatedSprite(Spritesheet(CHAR_PATH + ENEMY[id]['img']).img_extract(col,row,width,height))
        self.place=0

        #load image based on type later
        self.name=ENEMY[id]['name']
        #self.sprite.image=pygame.image.load(CHAR_PATH + ENEMY[id]['img'])
        self.HP = ENEMY[id]['hp']
        self.MHP=ENEMY[id]['hp']
        self.ATT = ENEMY[id]['att']
        self.weakness=ENEMY[id]['weak']

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

