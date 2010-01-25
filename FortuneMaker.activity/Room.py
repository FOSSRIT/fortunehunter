from constants import (
    DOOR_ORDER, DOOR_INDEX, DOOR_FLAGS, SPEC_FLAGS,
    ENEM_INDEX, ITEM_INDEX, ITEM_FLAGS
    )

import gtk

class Room:
    def __init__(self, x = -1, y = -1, str=None):
        self._x = x
        self._y = y
        self.doors = {}
        self.enemy = []
        self.item = []

        self.has_doors = False
        self.has_enemy = False
        self.has_item = False

        for index in DOOR_INDEX:
            self.doors[index] = ['0', '0']

        self.special = '0'

        for index in range(0,4):
            self.enemy.append( '0' )

        for index in range(0,4):
            self.item.append( ['0', '0'] )

        # Load room from str
        # TODO VALIDATE FLAGS
        if str:
            self.add_door( str[0], str[1] )
            self.add_door( str[2], str[3] )
            self.add_door( str[4], str[5] )
            self.add_door( str[6], str[7] )
            self.set_room_flag( str[8] )
            self.set_enemy( 0, str[9] )
            self.set_enemy( 1, str[10] )
            self.set_enemy( 2, str[11] )
            self.set_enemy( 3, str[12] )
            self.set_item( 0, str[13], str[14] )
            self.set_item( 1, str[15], str[16] )
            self.set_item( 2, str[17], str[18] )
            self.set_item( 3, str[19], str[20] )

    def add_door(self, door, flag):
        if door == "0":
            return
        elif door in DOOR_INDEX and flag in DOOR_FLAGS:
            self.has_doors = True
            self.doors[door] = [door, flag]
            return True
        else:
            print "INVALID DOOR AND/OR FLAG"
            return False

    def remove_door(self, door):
        if door in DOOR_INDEX:
            #TODO Check if should change has_door
            self.doors[door] = ['0', '0']
            return True
        else:
            print "INVALID DOOR"
            return False

    def get_door( self, door):
        if door in DOOR_INDEX:
            return self.doors[door][1]

    def set_room_flag(self, flag):
        if flag in SPEC_FLAGS:
            self.special = flag
            return True
        else:
            print "INVALID FLAG"
            return False

    def get_room_flag( self ):
        return self.special

    def add_enemy( self, enemy ):
        for index in range( 0,4 ):
            if self.enemy[index] == "0":
                return self.set_enemy(index, enemy)
        return False

    def set_enemy( self, pos, enemy ):
        if pos >= 0 and pos <=3 and enemy in ENEM_INDEX:
            self.enemy[pos] = enemy

            self.has_enemy = False

            for enemy in self.enemy:
                if enemy != "0":
                    self.has_enemy = True
                    break

            return True
        else:
            print "INVALID ENEMY POS OR ID"
            return False

    def get_enemy(self, pos):
        if pos >=0 and pos <=3:
            return self.enemy[pos]

    def add_item( self, enemy ):
        for index in range( 0,4 ):
            if self.item[index] == "0":
                return self.set_item(index, enemy)
        return False

    def set_item(self, pos, id, flag):
        if pos >= 0 and pos <=3 and id in ITEM_INDEX and flag in ITEM_FLAGS:
            self.item[ pos ] = [id, flag]

            self.has_item = False
            for item in self.item:
                if item[0] != "0"
                self.has_item = True
                break

            return True
        else:
            print "INVALID POS OR ID OR FLAG"
            return False

    def room_to_string(self):
        str = ""
        for index in DOOR_ORDER:
            str += self.doors[index][0] + self.doors[index][1]

        str += self.special

        for enemy in self.enemy:
            str += enemy

        for item in self.item:
            str += item[0] + item[1]

        return str

    def not_empty_room(self):
        return self.has_doors or self.has_enemy or self.has_item

    def render_room(self):
        if self.not_empty_room():
            but = gtk.Button("(%d, %d)" %(self._x, self._y))
        else:
            but = gtk.Button("")

        but.set_size_request(100, 100)
        return but
