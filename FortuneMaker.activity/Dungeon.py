from Room import Room

class Dungeon:
    def __init__( self, name, theme, next, width, height, room_str = None ):
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

    def update_room(self, room):
        self.roomlist[room._y][room._x] = room

    def export(self):
        text = str(self.width) + "x" + str(self.height) + "\n"
        text += str(self.theme) + "\n"
        text += str(self.next) + "\n"
        for row in self.roomlist:
            for room in row:
                text += room.room_to_string() + "\n"
        return text
