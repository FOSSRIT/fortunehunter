import pygame
import os.path
from gettext import gettext as _

from GameEngine import GameEngineElement

from Room import Room
from Items import get_item
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

            elif newKey=='[1]' or newKey=='e':
                self.item_pickup()
                return True

    def draw(self, screen):
        profile = self.game_engine.get_object('profile')
        dir = profile.playerFacing
        current_room = self.rooms[profile.position]

        # Draw background
        door_cfg = current_room.door_str( dir )
        screen.blit(self.__images[door_cfg],(0,0,1200,700))

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
                self.__images[path] = pygame.image.load(ENV_PATH + path)

            img_list.append( self.__images[path] )

        screen.blit(img_list[0],(270,330,50,50))
        screen.blit(img_list[1],(100,600,50,50))
        screen.blit(img_list[2],(1100,600,50,50))
        screen.blit(img_list[3],(900,330,50,50))
