from fortuneengine.GameEngineElement import GameEngineElement
from Enemy import get_enemy
from BattleMenu import BattleMenuHolder
from MagicMenu import MagicMenuHolder
from AnimatedSprite import Spritesheet
import pygame

from constants import CHAR_PATH, HUD_PATH

from gettext import gettext as _
import random

PLAYER_WAIT = 1
PLAYER_MULT = 2

class BattleEngine(GameEngineElement):
    def __init__(self, dgn):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.dgn = dgn
        self.current_room = dgn.get_current_room()

        self.font = pygame.font.SysFont("cmr10",18,False,False)

        self.enemy_list = []
        self.magic_list = []

        self.spellType = 0  #0 = non, 1-4 are spells in order, 5 is special
        self.isMagic = False
        self.state = PLAYER_WAIT
        self.player_input = '0'
        self.active_target = 1

        for i in range(0,4):
            e_index = self.current_room.get_enemy( i )

            if e_index != '0':
                self.enemy_list.append( get_enemy( e_index ) )

        # Preload images
        self.__images = {}
        for i in ['arrow_select']:
            self.__images[i] = pygame.image.load( HUD_PATH + i + ".gif" )

        self.__images['hp'] = Spritesheet( HUD_PATH + "hp.png" ).img_extract(11,1,100,100)
        self.__images['bt'] = Spritesheet( HUD_PATH + "bt.png" ).img_extract(1,11,100,25)

        self.add_to_engine()
        self.game_engine.add_object('battlemenu', BattleMenuHolder( self.menu_callback ) )
        self.game_engine.get_object('battlemenu').show_menu('selection')
        self.game_engine.get_object('mesg').add_line( _('Enemies present, prepare to fight!') )

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
                self.state = PLAYER_MULT
            else:
                #Do Attack
                print "Non Crit"
                menu.show_menu('selection')
                menu.set_sec_disp('')
                self.__attack_phase(menu)
            
        
        elif self.state == PLAYER_MULT:
            self.isMagic = False
            if selection == 'enter':
                #figure out damage for crit attack               
                if int(self.player_input) == (self.critAns):
                    menu.set_disp('Correct!')
                else:
                    menu.set_disp('Incorrect')
                
                menu.set_sec_disp('')
                self.player_input = ''
                self.__attack_phase(menu)

            elif selection == 'clear':
                self.player_input = ''
                menu.set_sec_disp('')
                               
            else:
                self.player_input = self.player_input + selection
                menu.set_sec_disp( self.player_input )
            
        elif selection == 'fire':
            menu.set_disp('Fire Cast!')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('fire')
            self.isMagic = True
            self.magicWin = False
                
        elif selection == 'heal':
            menu.set_disp('Heal Cast!')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('heal')
            self.isMagic = True
            self.magicWin = False
                
        elif selection == 'lightning':
            menu.set_disp('Lightning Cast!')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('lightning')
            self.isMagic = True
            self.magicWin = False
                
        elif selection == 'missile':
            menu.set_disp('Missile Cast!')
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('missile')
            self.isMagic = True
            self.magicWin = False
            
        elif selection == 'scan':
            menu.set_disp('Enemy Scanned!')
            self.isMagic = False
            self.__attack_phase(menu)
                
        elif selection == 'fire1':
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'fire2':
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'fire3':
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'fire4':
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig1':
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig2':
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig3':
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'lig4':
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss1':
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss2':
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss3':
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'miss4':
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal1':
            if(0 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(0)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal2':
            if(1 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(1)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal3':
            if(2 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(2)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'heal4':
            if(3 in self.magic_list):
                self.__attack_phase(menu)
            else:
                self.magic_list.append(3)
                if(len(self.magic_list) > 3):
                    self.magicWin = True
                    self.__attack_phase(menu)
        elif selection == 'wrongchoice':
            self.__attack_phase(menu)

    def __attack_phase(self, menu):
        # Check to see how much hp enemy has left.
        # Enemy Attack
        # Check player health
        hero = self.game_engine.get_object('profile').hero
        weakness = self.enemy_list[self.active_target]
        spellTypes = ['none', 'fire', 'lightning', 'missile', 'heal', 'special']
        bonus = 0
        if spellTypes[self.spellType] == weakness:
            bonus = 60
        
        
        
        
        
        
        self.state = PLAYER_WAIT
        self.magic_list = []
        print("in __attack_phase")
        self.__end_battle(menu)

    def __end_battle(self, menu):
        #Give items if any
        #self terminate
        if (self.isMagic):
            self.game_engine.get_object('magicmenu').remove_from_engine()
            self.game_engine.remove_object('magicmenu')
        else:
            menu.show_menu('selection')

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
                
                #do damage calculations
                return True


        # We don't want to allow other things to run during battle
        return True

    def draw(self,screen,time_delta):
        x=250
        y=150
        i = 1

        tick_time = pygame.time.get_ticks()

        # Draw Enemy and Item Selection
        for enemy in self.enemy_list:
            if self.active_target == i:
                screen.blit(self.__images['arrow_select'], (x+(i*200),y-25))
            enemy.sprite.update( tick_time )
            screen.blit(enemy.sprite.image, (x+(i*200),y))
            i = i+1

        # Draw Hud
        profile = self.game_engine.get_object('profile')

        # Player Health
        health = 10 - profile.hero.healthLevel()
        screen.blit(self.__images['hp'][health], (25,25))
