from Room import Room

class Dungeon:
    def __init__( self, name, theme, width, height ):
        self.name = name
        self.theme = theme
        self.width = width
        self.height = height

        self.roomlist = []
        for y in range(0, width):
            room_row = []
            for x in range(0, height):
                room_row.append( Room(x,y) )
            self.roomlist.append(room_row)

    def get_room_array(self):
        return self.roomlist

    def update_room(self, room):
        self.roomlist[room._y][room._x] = room

    def export(self):
        text = str(self.width) + "x" + str(self.height) + "\n"
        for row in self.roomlist:
            for room in row:
                text += room.room_to_string() + "\n"
        return text
