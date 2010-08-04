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

        self.enemy_list = []
        self.magic_list = []

        self.spellType = 0  #0 = non, 1-4 are spells in order, 5 is special
        self.isMagic = False
        self.correct = False
        self.state = PLAYER_WAIT
        self.player_input = '0'
        self.active_target = 1

        for i in range(0,4):
            e_index = self.current_room.get_enemy( i )

            if e_index != '0':
                curE = get_enemy( e_index )
                self.enemy_list.append( curE )
                self.game_engine.get_scene().addObject(curE.get_sprite())

        # Preload images
        self.__drawableObjects = {}
        for i in ['arrow_select']:
            self.__drawableObjects[i] = DrawableObject([pygame.image.load( HUD_PATH + i + ".gif" )], '')
            self.game_engine.get_scene().addObject(self.__drawableObjects[i])

        self.__drawableObjects['hp'] = DrawableObject(Spritesheet( HUD_PATH + "hp.gif" ).img_extract(11,1,100,100), '')
        self.__drawableObjects['bt'] = DrawableObject(Spritesheet( HUD_PATH + "bt.gif" ).img_extract(1,11,100,25), '', True)
        self.game_engine.get_scene().addObject(self.__drawableObjects['hp'])
        self.game_engine.get_scene().addObject(self.__drawableObjects['bt'])

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
                if self.player_input == '':
                    self.player_input = '0'
                if int(self.player_input) == (self.critAns):
                    menu.set_disp('Correct!')
                    self.correct = True
                else:
                    menu.set_disp('Incorrect')
                    self.correct = False
                
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
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('fire')
            self.spellType = 1
            self.isMagic = True
            self.magicWin = False
        elif selection == 'lightning':
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('lightning')
            self.spellType = 2
            self.isMagic = True
            self.magicWin = False
        elif selection == 'missile':
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('missile')
            self.spellType = 3
            self.isMagic = True
            self.magicWin = False
        elif selection == 'heal':
            self.game_engine.add_object('magicmenu', MagicMenuHolder( self.menu_callback ) )
            self.game_engine.get_object('magicmenu').show_menu('heal')
            self.spellType = 4
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
        #do the correct damage to correct enemy
        hero = self.game_engine.get_object('profile').hero
        damage = 0
        curTarget = self.active_target - 1
        if self.isMagic:
            weakness = self.enemy_list[curTarget]
            spellTypes = ['none', 'fire', 'lightning', 'missile', 'heal', 'special']
            bonus = 0
            if spellTypes[self.spellType] == weakness:
                bonus = 60
                damage += bonus
            if self.magicWin and not(self.spellType == 4):
                damage += hero.attackPower(spellTypes[self.spellType])
                self.enemy_list[curTarget].HP -= damage
                self.player_input = spellTypes[self.spellType] + ' cast!'
            elif self.spellType == 4:
                hero.giveHealth(hero.attackPower('heal'))
            else:
                self.player_input = 'Spell fizzles'
        elif self.state == PLAYER_MULT:
            if self.correct:
                damage = hero.attackPower("critical")
                self.enemy_list[curTarget].HP -= damage
                self.player_input = "Your attack crits for " + str(damage) + " damage"
        else:
            damage = hero.attackPower('basic')
            self.enemy_list[curTarget].HP -= damage
            self.player_input = "You attack for " + str(damage) + " damage"
                
        
        #generate enemy attack
        for enemy in self.enemy_list[:]:
            if enemy.HP <= 0:
                enemy.alive = False
                self.enemy_list.remove(enemy)
                enemy.makeTransparent(True)
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
        self.game_engine.get_scene().removeObject(self.background)
        for object in self.__drawableObjects:
            self.game_engine.get_scene().removeObject(object)
            
        self.game_engine.get_object('battlemenu').remove_from_engine()
        self.game_engine.remove_object('battle')
        
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

    def draw(self,screen,time_delta):
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
        self.__drawableObjects['hp'].goToAnim(health)
        self.__drawableObjects['hp'].setPosition(25,25)

