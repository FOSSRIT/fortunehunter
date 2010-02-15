import pygame
import os.path

from GameEngine import GameEngineElement

from Room import Room
from constants import (
        MAP_PATH, ENV_PATH, RIGHT, LEFT, NORTH, SOUTH, EAST,
        WEST, UNLOCKED_DOOR, LOCKED_DOOR
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
        print door_type
        if door_type == UNLOCKED_DOOR:
            return True

        print "A WEIRD DOOR", door_type

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

        if self.rooms.has_key( (dX, dY) ) and self.move_permissions( self.rooms[profile.position].get_door( dc ) ):
            profile.move_to( dX, dY )
        else:
            print "CANT ENTER DOOR"

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
