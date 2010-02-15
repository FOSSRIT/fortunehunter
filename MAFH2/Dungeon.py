import pygame
import os.path
from gettext import gettext as _

from GameEngine import GameEngineElement

from Room import Room
from constants import (
        MAP_PATH, ENV_PATH, RIGHT, LEFT, NORTH, SOUTH, EAST,
        WEST, UNLOCKED_DOOR, LOCKED_DOOR, PUZZLE_DOOR, LOCKED_PUZZLE_DOOR,
        ENTRANCE_DOOR, EXIT_DOOR
        )
from JournalIntegration import do_load, load_dungeon_by_id

class Dungeon(GameEngineElement):
    def __init__(self, id):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.add_to_engine()

        self.id = id
        self.rooms={}
        self.__images={}
        self.__load_dungeon()
        self.__load_images()
        profile = self.game_engine.get_object('profile')

        if profile.position == (-1, -1):
            x,y = self.start
            profile.move_to( x, y )

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
        LVL_PATH = ENV_PATH

        for img_key in ['FLR', 'FR', 'FL', 'F', 'LR', 'L', 'R', '_']:
            self.__images[img_key] = pygame.image.load(LVL_PATH+img_key.lower()+".gif")

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
        else:
            #Entrance or exit may be on a boarder of the grid
            door_flag = self.rooms[profile.position].get_door( dc )
            if door_flag == EXIT_DOOR or door_flag == ENTRANCE_DOOR:
                if self.move_permissions( door_flag ):
                    # TODO: Next Dungeon
                    pass

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            newKey=pygame.key.name(event.key)

            if newKey=='m' or newKey=='[7]':
                print "SHOW Macro Map"
                return True

            elif newKey=='[4]' or newKey=='left':
                self.game_engine.get_object('profile').turn( LEFT )
                return True

            elif newKey=='[6]' or newKey=='right':
                self.game_engine.get_object('profile').turn( RIGHT )
                return True

            elif newKey=='[8]' or newKey=='up':
                self.move_forward()
                return True

    def draw(self, screen):
        profile = self.game_engine.get_object('profile')
        dir = profile.playerFacing
        door_cfg = self.rooms[profile.position].door_str( dir )

        screen.blit(self.__images[door_cfg],(0,0,1200,700))
