from Items import get_item
from random import *
import pygame
from pygame.locals import *
from constants import MENU_PATH, CHAR_PATH

############################################################################
#Merchant class
############################################################################
class Merchant:
    def __init__(self,player):
	    self.player = player
        self.itemList=[get_item('l'),get_item('m')]
        self.selItem=0
        self.numItem=[0,0]
        self.totalPrice=0
        self.selDigit=3
        self.enteredDigits=[0,0,0,0]
        self.buyScreen=False
        self.buyMode=True
        self.sellMode=False
        self.yes=True
        self.shopKeeperVariable=0
        self.message=[]
        
        if self.player.shopTutorial = False:
            self.message.append("WELCOME TO SHOP - TUTORIAL MESSAGE")
        else:
            self.message.append("NORMAL SHOP MESSAGE")
			
			#tickets - win screen missing, hold+flash amulet search missing, scan does damage, when you die you restart dungeon w current inventory, fast clicking through battle crashes game