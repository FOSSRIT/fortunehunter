import pygame
import os.path
from time import time
from gettext import gettext as _

from fortuneengine.GameEngineElement import GameEngineElement

from BattleEngine import BattleEngine
from Map import Map
from Room import Room
from Items import get_item
from constants import (
        MAP_PATH, ENV_PATH, ITEM_PATH, RIGHT, LEFT, NORTH, SOUTH, EAST,
        WEST, UNLOCKED_DOOR, LOCKED_DOOR, PUZZLE_DOOR, LOCKED_PUZZLE_DOOR,
        ENTRANCE_DOOR, EXIT_DOOR
        )
from JournalIntegration import do_load, load_dungeon_by_id

SEARCH_TIME = 2
COLOR_DELTA = 255/SEARCH_TIME

class Dungeon(GameEngineElement):
    def __init__(self, id):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.id = id
        self.rooms={}
        self.__images={}
        self.__load_dungeon()
        self.__load_images()
        profile = self.game_engine.get_object('profile')

        if profile.position == (-1, -1):
            x,y = self.start
            profile.move_to( x, y )

        self.add_to_engine()

    def add_to_engine(self):
        super(Dungeon, self).add_to_engine()
        self.game_engine.add_object('map', Map( self ) )

    def remove_from_engine(self):
        super(Dungeon, self).remove_from_engine()
        self.game_engine.get_object('map').remove_from_engine()
        self.game_engine.remove_object('map')

    def __load_dungeon(self):
        currentX=0
        currentY=0

        if os.path.exists( MAP_PATH + self.id ):
            dgnFile=open( MAP_PATH + self.id,'r')
            d_dict = do_load( dgnFile )
            dgnFile.close()
        else:
            d_dict = load_dungeon_by_id( self.id )

        self.sizeX = d_dict['x']
        self.sizeY = d_dict['y']
        self.theme = d_dict['theme']
        self.name = d_dict['name']
        self.next = d_dict['next']

        for line in d_dict['roomstr']:
            the_room = Room( currentX, currentY, line )
            self.rooms[(currentX,currentY)] = the_room

            if the_room.is_entrance():
                self.start=(currentX,currentY)

            currentX+=1
            if currentX==self.sizeX:
                currentY+=1
                currentX=0

            if currentY>self.sizeY:
                break


    def __load_images(self):
        #LVL_PATH = ENV_PATH + "ice/"
        #LVL_PATH = ENV_PATH + "celestial/"
        LVL_PATH = ENV_PATH + "pyramid/"

        for img_key in ['Room','F','L']:
            img = pygame.image.load(LVL_PATH+img_key+".png").convert()
            img.set_colorkey((255,0,255))
            width,height = img.get_size()
            
            img = pygame.transform.scale(img, (self.game_engine.art_scale(width, 1200, True), self.game_engine.art_scale(height, 900, False)))

            self.__images[img_key] = img
            
    def get_current_room(self):
        profile = self.game_engine.get_object('profile')
        return self.rooms[profile.position]

    def move_permissions(self, door_type):
        if door_type == UNLOCKED_DOOR:
            return True

        elif door_type == LOCKED_DOOR:
            #Checks if they have a small key
            for item in self.game_engine.get_object('profile').inventory:
                # Search for small key (ID: 'q')
                if item.id == 'q':
                    self.game_engine.get_object('mesg').add_line(_("You use a SMALL KEY"))
                    return True

            self.game_engine.get_object('mesg').add_line(_("This door is locked, you need a SMALL KEY"))
            return False

        elif door_type == PUZZLE_DOOR or door_type == LOCKED_PUZZLE_DOOR:
            #TODO: START PUZZLE
            return False

        elif door_type == ENTRANCE_DOOR:
            self.game_engine.get_object('mesg').add_line(_("There is no turning back now"))
            return False

        elif door_type == EXIT_DOOR:
            #Checks if they have a big key
            for item in self.game_engine.get_object('profile').inventory:
                # Search for big key (ID: 'r')
                if item.id == 'r':
                    self.game_engine.get_object('mesg').add_line(_("You use the BIG KEY, and the door slams behind you!"))
                    return True


            self.game_engine.get_object('mesg').add_line(_("This door is locked, you need a BIG KEY"))
            return False

        return False


    def move_forward(self):
        profile = self.game_engine.get_object('profile')
        x,y = profile.position

        if profile.playerFacing == NORTH:
            dX = x
            dY = y - 1
            dc = 'N'

        elif profile.playerFacing == SOUTH:
            dX = x
            dY = y + 1
            dc = 'S'

        elif profile.playerFacing == EAST:
            dX = x + 1
            dY = y
            dc = 'E'

        elif profile.playerFacing == WEST:
            dX = x - 1
            dY = y
            dc = 'W'

        if self.rooms.has_key( (dX, dY) ):
            door_flag = self.rooms[profile.position].get_door( dc )
            if self.move_permissions( door_flag ):
                self.game_engine.get_object('mesg').add_line(_("You enter room at %i,%i")%(dX, dY))
                profile.move_to( dX, dY )
                self.game_engine.get_object('map').update_macro()
                self.check_for_enemies()
        else:
            #Entrance or exit may be on a border of the grid
            door_flag = self.rooms[profile.position].get_door( dc )
            if door_flag == EXIT_DOOR or door_flag == ENTRANCE_DOOR:
                if self.move_permissions( door_flag ):
                    # TODO: Next Dungeon
                    pass

    def check_for_enemies(self):
        current_room = self.get_current_room()
        if current_room.has_enemy:
            self.game_engine.add_object('battle', BattleEngine( self ) )

    def item_pickup(self):
        profile = self.game_engine.get_object('profile')
        current_room = self.rooms[profile.position]

        for i in range( 0, 4 ):
            item_key = current_room.get_item( i )

            # If visible, remove from room and place in players inventory
            if item_key[0] != '0' and item_key[1] == 'v':
                item = get_item( item_key[0] )
                profile.give_item( item )
                current_room.remove_item( i )
                self.game_engine.get_object('mesg').add_line(_("%s discovered!")% item.name)
                return
        self.game_engine.get_object('mesg').add_line(_("No items found."))

    def amulet_search(self):
        current_room = self.get_current_room()

        found = False
        for i in range( 0, 4 ):
            item_key = current_room.get_item( i )

            # If visible, remove from room and place in players inventory
            if item_key[0] != '0' and item_key[1] == 'h':
                current_room.set_item( i, item_key[0], 'v' )
                found = True
        if found:
            self.game_engine.get_object('mesg').add_line(_("Amulet Search has revealed new items."))
        else:
            self.game_engine.get_object('mesg').add_line(_("Amulet search found nothing."))

    def search_timer_handler(self):
        """
        Called when the timer has expired, fires off the amulet search
        """
        self.game_engine.stop_event_timer( \
            self.search_timer_handler )
        del self.pickup_time
        self.amulet_search()

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            newKey=pygame.key.name(event.key)

            if newKey=='[4]' or newKey=='left':
                self.game_engine.get_object('profile').turn( LEFT )
                return True

            elif newKey=='[6]' or newKey=='right':
                self.game_engine.get_object('profile').turn( RIGHT )
                return True

            elif newKey=='[8]' or newKey=='up':
                self.move_forward()
                return True

            elif newKey=='[1]' or newKey=='e':
                self.pickup_time = time()
                self.game_engine.start_event_timer( \
                    self.search_timer_handler, SEARCH_TIME * 1000 )
                return True

        elif event.type == pygame.KEYUP:
            newKey=pygame.key.name(event.key)

            if newKey=='[1]' or newKey=='e':
                if hasattr( self, 'pickup_time' ):
                    if time() - self.pickup_time < SEARCH_TIME:
                        self.item_pickup()

                    self.game_engine.stop_event_timer( \
                        self.search_timer_handler )
                    del self.pickup_time
                return True

    def normalize_dir( self ):
        profile = self.game_engine.get_object('profile')
        dir = profile.playerFacing

        if dir == NORTH:
            return 'W', 'N', 'E'

        elif dir == SOUTH:
            return 'E', 'S', 'W'

        elif dir == EAST:
            return 'N', 'E', 'S'

        elif dir == WEST:
            return 'S', 'W', 'N'

#-------------------------------------------------------------------------------------------------------------------------------------------------------
# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
#
    def draw(self,screen,time_delta):
        profile = self.game_engine.get_object('profile')
        dir = profile.playerFacing
        current_room = self.rooms[profile.position]

        # Draw Room Background
        screen.blit(self.__images['Room'],(0,0))

        # Draw Room Doors
        left, front, right = self.normalize_dir()
        if current_room.get_door( left ) != '0':
            screen.blit(self.__images['L'],(0,0))

        if current_room.get_door( front ) != '0':
            screen.blit(self.__images['F'],( self.game_engine.art_scale(360, 1200, True),0))

        if current_room.get_door( right ) != '0':
            screen.blit(pygame.transform.flip(self.__images['L'], True, False),(self.game_engine.art_scale(990, 1200, True),0))

        # Draw Items
        img_list = []

        for i in range( dir, (dir + 4) ):
            #imod for room rotation
            imod = i % 4

            item_key = current_room.get_item( imod )

            if item_key[0] == '0' or item_key[1] != 'v':
                path = "noItem.gif"
            else:
                path = get_item( item_key[0] ).path

            if not self.__images.has_key( path ):
                img = pygame.image.load(ITEM_PATH + path).convert()
                width,height = img.get_size()
                img = pygame.transform.scale(img, (self.game_engine.art_scale(width, 1200, True), self.game_engine.art_scale(height, 900, False)))
                self.__images[path] = img

            img_list.append( self.__images[path] )

        screen.blit(img_list[0],(self.game_engine.art_scale(270, 1200, True),self.game_engine.art_scale(330, 900, False)))
        screen.blit(img_list[1],(self.game_engine.art_scale(100, 1200, True),self.game_engine.art_scale(600, 900, False)))
        screen.blit(img_list[2],(self.game_engine.art_scale(1100, 1200, True),self.game_engine.art_scale(600, 900, False)))
        screen.blit(img_list[3],(self.game_engine.art_scale(900, 1200, True),self.game_engine.art_scale(330, 900, False)))

        #Amulet Search Function
        if hasattr(self, 'pickup_time'):
            elp = time() - self.pickup_time
            color_a = int(elp*COLOR_DELTA)
            if color_a > 255:
                color_a = 255
                self.game_engine.stop_event_timer(self.search_timer_handler)
            surf1 = pygame.Surface((self.game_engine.width,self.game_engine.height), pygame.SRCALPHA)
            pygame.draw.rect(surf1, (255, 255, 255, color_a), (0, 0, self.game_engine.width, self.game_engine.height))
            screen.blit( surf1, (0, 0) )
