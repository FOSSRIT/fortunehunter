from GameEngine import GameEngineElement
from Enemy import get_enemy
from BattleMenu import BattleMenuHolder
from AnimatedSprite import Spritesheet
import pygame

from constants import CHAR_PATH, HUD_PATH

from gettext import gettext as _

class BattleEngine(GameEngineElement):
    def __init__(self, dgn):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.dgn = dgn
        self.current_room = dgn.get_current_room()

        self.enemy_list = []

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

        self.game_engine.start_event_timer(1, 150)

        self.add_to_engine()
        self.game_engine.add_object('battlemenu', BattleMenuHolder( self.menu_callback ) )
        self.game_engine.get_object('battlemenu').show_menu('selection')
        self.game_engine.get_object('mesg').add_line( _('Enemies present, prepare to fight!') )

    def menu_callback(self, selection, menu):
        print selection

    def __attack_phase(self):
        # Enemy Attack
        # Check player health
        pass

    def __end_battle(self):
        #Give items if any
        #self terminate
        pass

    def event_handler(self, event):
        if event.type == pygame.USEREVENT+1:
            return True

        elif event.type == pygame.KEYDOWN:

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


        # We don't want to allow other things to run durning battle
        return True

    def draw(self, screen):
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
