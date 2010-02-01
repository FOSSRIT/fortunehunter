from Room import Room
from sugar.util import unique_id

class Dungeon:
    def __init__( self, name, theme, next, width, height, room_str = None, id = None ):
        if id:
            self.id = id
        else:
            self.id = unique_id()

        self.name = name
        self.theme = theme
        self.next = next
        self.width = width
        self.height = height

        self.roomlist = []

        for y in range(0, height):
            room_row = []
            for x in range(0, width):
                if room_str:
                    room_row.append( Room(x,y, room_str.pop(0) ) )
                else:
                    room_row.append( Room(x,y) )
            self.roomlist.append(room_row)

    def get_room_array(self):
        return self.roomlist

    def has_door_type(self, key):
        for room_row in self.roomlist:
            for room in room_row:
                for door_key in room.doors:
                    if room.doors[door_key][1] == key:
                        return True
        return False

    def valid_dungeon(self):
        return self.has_door_type( 'e' ) and self.has_door_type( 'x' )

    def get_adj_room( self, room, dir ):
        if dir == "N":
            next_x = room._x
            next_y = room._y-1
        elif dir == "E":
            next_x = room._x+1
            next_y = room._y
        elif dir == "S":
            next_x = room._x
            next_y = room._y+1
        elif dir == "W":
            next_x = room._x-1
            next_y = room._y
        else:
            return False

        if next_x < 0 or next_y < 0:
            return False

        try:
           return self.roomlist[next_y][next_x]
        except:
            return False

    def update_room(self, room):
        self.roomlist[room._y][room._x] = room

    def export(self):
        text = self.name + "\n"
        text += self.id + "\n"
        text += str(self.width) + "x" + str(self.height) + "\n"
        text += str(self.theme) + "\n"
        text += str(self.next) + "\n"
        for row in self.roomlist:
            for room in row:
                text += room.room_to_string() + "\n"
        return text
