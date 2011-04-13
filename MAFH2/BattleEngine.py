from fortuneengine.GameEngineElement import GameEngineElement
from Enemy import get_enemy
from BattleMenu import BattleMenuHolder
from MagicMenu import MagicMenuHolder
from Spritesheet import Spritesheet
from Items import get_item
from fortuneengine.DrawableObject import DrawableObject
from fortuneengine.DynamicDrawableObject import DynamicDrawableObject
from fortuneengine.Scene import Scene
import pygame
import time

######################################################################
#BattleEngine Class: This class is the 'engine' for the battles (attack options, etc.)
######################################################################

from constants import CHAR_PATH, HUD_PATH

from gettext import gettext as _
import random

PLAYER_WAIT = 1
PLAYER_MULT = 2
_dirtyList=[]

class BattleEngine(GameEngineElement):
    def __init__(self, dgn):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.dgn = dgn
        self.current_room = dgn.get_current_room()

        self.font = pygame.font.SysFont("cmr10",18,False,False)

        self.enemy_list = [] #Holds the list of enemies
        self.magic_list = [] #Holds list of magic used?

        self.spellType = 0  #0 = non, 1-4 are spells in order, 5 is special
        self.isMagic = False
        self.correct = False
        self.state = PLAYER_WAIT
        self.player_input = '0'
        self.active_target = 1
        self.battleTimer = -1.0
        self.tIndex = 0

        for i in range(0,4):
            e_index = self.current_room.get_enemy( i )

            if e_index != '0':
                curE = get_enemy( e_index )
                self.enemy_list.append( curE )
                self.add_to_scene([curE.get_sprite()])

        # Preload images
        self.__drawableObjects = {}
        for i in ['arrow_select']:
            self.__drawableObjects[i] = DrawableObject([pygame.image.load( HUD_PATH + i + ".gif" )], '')
            self.add_to_scene([self.__drawableObjects[i]])

        self.__drawableObjects['hp'] = DrawableObject(Spritesheet( HUD_PATH + "hp.gif" ).img_extract(11,1,100,100,[255,0,255]), '')
        self.__drawableObjects['bt'] = DrawableObject(Spritesheet( HUD_PATH + "bt.gif" ).img_extract(1,11,100,25, [255,0,255]), '', True)
        self.__drawableObjects['hp'].setColorKey((255,0,255))
        self.__drawableObjects['bt'].setColorKey((255,0,255))
        self.add_to_scene([self.__drawableObjects['hp']])
        self.add_to_scene([self.__drawableObjects['bt']])

        self.add_to_engine()
        self.game_engine.add_object('battlemenu', BattleMenuHolder( self.menu_callback ) )
        self.game_engine.get_object('battlemenu').show_menu('selection')
        self.game_engine.get_object('mesg').add_line( _('Enemies present, prepare to fight!') )

    #set menu options and actions that go along with them (during attack)
    def menu_callback(self, selection, menu):
        if selection == 'attack_show':
            menu.set_sec_disp('')
            self.player_input = ''
            self.isMagic = False
            random.seed()
            isCrit = random.randint(0,100)
            if( isCrit > 90 ):
                #Show problem
                menu.show_menu('attack')
                tempR1 = random.randint(0,10)
                tempR2 = random.randint(0,10)
                self.critAns = tempR1 * tempR2
                menu.set_disp('%d x %d' %(tempR1, tempR2))
                self.battleTimer = time.time()
                self.state = PLAYER_MULT
            else:
                #Do Attack
                #print "Non Crit"
                menu.show_menu('selection')
                menu.set_sec_disp('')
                self.__attack_phase(menu)
            
        
        elif self.state == PLAYER_MULT:
            self.isMagic = False
            if self.tIndex<10:
                if selection == 'enter':
                    #figure out damage for crit attack
                    if self.player_input == '':
                        self.player_input = '0'
                    if int(self.player_input) == (self.critAns):
                        menu.set_disp('Correct!') #this is never displayed (covered)?
                        self.correct = True
                        self.player_input = ''
                    else:
                        menu.set_disp('Incorrect') #wrong display
                        self.player_input = "Incorrect"
                        self.correct = False

                    menu.set_sec_disp('')
                    #self.player_input = '' #wrong place, overwrites everything
                    self.__attack_phase(menu)

                elif selection == 'clear':
                    self.player_input = ''
                    menu.set_sec_disp('')

                else:
                    self.player_input = self.player_input + selection
                    menu.set_sec_disp( self.player_input )
            else:
                self.player_input = ''
               # menu.set_sec_disp('')
               # if not self.correct:
                #    self.player_input = "Incorrect"
                #else:
                 #   self.player_input = ''
                self.__attack_phase(menu)
            
        elif selection == 'fire':
            menu.set_disp('')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('fire')
            self.spellType = 1
            self.isMagic = True
            self.magicWin = False
            self.battleTimer = time.time()
        elif selection == 'lightning':
            menu.set_disp('')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('lightning')
            self.spellType = 2
            self.isMagic = True
            self.magicWin = False
            self.battleTimer = time.time()
        elif selection == 'missile':
            menu.set_disp('')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('missile')
            self.spellType = 3
            self.isMagic = True
            self.magicWin = False
            self.battleTimer = time.time()
        elif selection == 'heal':
            menu.set_disp('')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('heal')
            self.spellType = 4
            self.isMagic = True
            self.magicWin = False
            self.battleTimer = time.time()
        elif selection == 'scan':
            menu.set_disp('Enemy Scanned!')
            self.isMagic = False
            curTarget = self.active_target - 1
            self.game_engine.get_object('mesg').add_line(_("Remaining HP: "+repr(self.enemy_list[curTarget].HP)))
            self.game_engine.get_object('mesg').add_line(_("Enemy Weakness: "+repr(self.enemy_list[curTarget].weakness)))
#            self.__attack_phase(menu)
                
        elif selection == 'fire1' and self.tIndex<10:
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'fire2' and self.tIndex<10:
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'fire3' and self.tIndex<10:
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'fire4' and self.tIndex<10:
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig1' and self.tIndex<10:
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig2' and self.tIndex<10:
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig3' and self.tIndex<10:
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig4' and self.tIndex<10:
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss1' and self.tIndex<10:
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss2' and self.tIndex<10:
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss3' and self.tIndex<10:
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss4' and self.tIndex<10:
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal1' and self.tIndex<10:
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal2' and self.tIndex<10:
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal3' and self.tIndex<10:
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal4' and self.tIndex<10:
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'wrongchoice':
            self.__attack_phase(menu)
        elif self.tIndex==10:
            self.magicWin = False
            self.__attack_phase(menu)
        
    #engaging in actual attack--do the correct damage to the correct enemy
    def __attack_phase(self, menu):
        hero = self.game_engine.get_object('profile').hero
        damage = 0
        curTarget = self.active_target - 1
        timeRatio = time.time() - self.battleTimer
        self.battleTimer = -1.0
        if timeRatio < 10:
            timeRatio = timeRatio / 10.0
        else:
            timeRatio = 1.0
        tbonus = 1.0 - timeRatio
        tbonus += 1.3
        if self.isMagic and self.tIndex<10:
            weakness = self.enemy_list[curTarget]
            spellTypes = ['none', 'fire', 'lightning', 'missile', 'heal', 'special']
            bonus = 0
            if spellTypes[self.spellType] == weakness:
                bonus = 60
                damage += bonus
            if self.magicWin and not(self.spellType == 4):
                damage += hero.attackPower(spellTypes[self.spellType])
                damage *= tbonus
                self.enemy_list[curTarget].HP -= int(damage)
                self.player_input = spellTypes[self.spellType] + ' cast!'
            elif self.spellType == 4:
		if self.magicWin:
                    hero.giveHealth(int(hero.attackPower('heal') * tbonus))
		    self.player_input = "Healed!"
		else:
                    self.player_input = "Failed to heal"
            elif not self.magicWin:
                self.player_input = 'Spell fizzles'
        elif self.state == PLAYER_MULT and self.tIndex<10:
            if self.correct:
                damage = hero.attackPower("critical")
                damage = damage * tbonus
                self.enemy_list[curTarget].HP -= int(damage)
                self.player_input = "Your attack crits for " + str(int(damage)) + " damage"
        elif self.tIndex==10:
            self.player_input = "Time's up!"
        else:
            damage = hero.attackPower('basic')
            self.enemy_list[curTarget].HP -= damage
            self.player_input = "You attack for " + str(int(damage)) + " damage"
        self.tIndex = 0 #reset
        
        #generate enemy attack
        for enemy in self.enemy_list[:]:
            if enemy.HP <= 0:
                enemy.alive = False
                self.enemy_list.remove(enemy)
                enemy.get_sprite().makeTransparent(True)
                self.active_target = 1
            if enemy.alive:
                random.seed()
                enemyAttack = random.randint(0,100)
                if enemyAttack > 90:
                    hero.defendAttack(enemy.attackPower('special'))
                elif enemyAttack < 6:
                    hero.defendAttack(enemy.attackPower('critical'))
                else:
                    hero.defendAttack(enemy.attackPower('basic'))
            if hero.healthPoints() <= 0:
                self.__youDied()
                return
        
        self.game_engine.get_object('profile').hero = hero
        self.state = PLAYER_WAIT
        self.magic_list = []
        if (self.isMagic):
            self.game_engine.get_object('magicmenu').remove_from_engine()
            self.game_engine.remove_object('magicmenu')
        else:
            menu.show_menu('selection')
            
        self.game_engine.get_object('battlemenu').set_disp(self.player_input)

        #Are enemies dead?
        if not self.enemy_list:
            self.__end_battle(menu)

    # ends the battle
    def __end_battle(self, menu):
        #Give items if any
        room = self.game_engine.get_object('dungeon').get_current_room()
            
        for i in range( 0, 4 ):
            item_key = room.get_item( i )
            # If visible, remove from room and place in players inventory
            if item_key[0] != '0' and item_key[1] == 'b':
                item = get_item( item_key[0] )
                self.game_engine.get_object('profile').give_item( item )
                room.remove_item( i )
                self.game_engine.get_object('mesg').add_line(_("%s dropped!")% item.name)
        room.has_enemy = False
        
        #self terminate
        #print 'end battle called'
        self.remove_from_engine()
        
        self.game_engine.get_object('battlemenu').remove_from_engine()
        self.game_engine.remove_object('battlemenu')
        self.game_engine.remove_object('battle')

    #Lets actor know when it has been defeated/killed.
    def __youDied(self):
        self.remove_from_engine()
        self.game_engine.get_object('battlemenu').remove_from_engine()
        self.game_engine.remove_object('battlemenu')
        self.game_engine.remove_object('battle')
        
        self.game_engine.get_object('profile').reload_dungeon( )

        self.game_engine.get_object('mesg').add_line(
                _("You have been defeated in battle and resurrected."))

        #self.remove_from_engine()
        #self.game_engine.get_object('battlemenu').remove_from_engine()
        #self.game_engine.get_object('battle').remove_from_engine()
        #self.game_engine.get_object('dungeon').remove_from_engine()
        #self.game_engine.get_object('manager').remove_from_engine()
        #self.game_engine.get_object('mesg').remove_from_engine()
        #self.game_engine.get_object('map').remove_from_engine()
        #self.game_engine.get_object('term

    #
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:

            newKey=pygame.key.name(event.key)

            if newKey=='[4]' or newKey=='left':
                self.active_target -= 1
                if self.active_target < 1:
                    self.active_target = len(self.enemy_list)
                return True
            elif newKey=='[6]' or newKey=='right':
                self.active_target += 1
                if self.active_target > len(self.enemy_list):
                    self.active_target = 1
                return True
            
            elif newKey=='return':
                self.enemy = self.active_target
                return True


        # We don't want to allow other things to run during battle
        return True

    #Draws the sprites/actors/etc. (drawable objects)
    def draw(self):
        x=250
        y=150
        i = 1
        
        tick_time = pygame.time.get_ticks()

        # Draw Enemy and Item Selection
        for enemy in self.enemy_list:
            if enemy.alive and self.active_target == i:
                self.__drawableObjects['arrow_select'].setPosition(x+(i*200),y-25)
            enemy.get_sprite().setPosition(x+(i*200),y)
            i = i+1

        # Draw Hud
        profile = self.game_engine.get_object('profile')

        # Player Health
        health = 10 - profile.hero.healthLevel()

        self.__drawableObjects['hp'].goToFrame(health)
        self.__drawableObjects['hp'].setPosition(25,25)
        
        #Battle Timer
        if(self.battleTimer > 0):
            self.__drawableObjects['bt'].makeTransparent(False)
            self.__drawableObjects['bt'].setPosition(25,130)
            self.tIndex = int(time.time() - self.battleTimer)
            if self.tIndex > 10:
                self.tIndex = 10
            self.__drawableObjects['bt'].goToFrame(self.tIndex)
        else:
            self.__drawableObjects['bt'].makeTransparent(True)
