from GameEngine import GameEngineElement
from Enemy import get_enemy
import pygame

from constants import CHAR_PATH

from gettext import gettext as _

class BattleEngine(GameEngineElement):
    def __init__(self, dgn):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.dgn = dgn
        self.current_room = dgn.get_current_room()

        self.enemy_list = []

        for i in range(0,4):
            e_index = self.current_room.get_enemy( i )

            if e_index != '0':
                self.enemy_list.append( get_enemy( e_index ) )


        self.game_engine.start_event_timer(1, 150)

        self.add_to_engine()
        self.game_engine.get_object('mesg').add_line( _('Enemies present, prepare to fight!') )

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

        # We don't want to allow other things to run durning battle
        return True

    def draw(self, screen):
        x=250
        y=150
        i = 1

        tick_time = pygame.time.get_ticks()

        for enemy in self.enemy_list:
            enemy.sprite.update( tick_time )
            screen.blit(enemy.sprite.image, (x+(i*200),y,200,200))
            i = i+1
