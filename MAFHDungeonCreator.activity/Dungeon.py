from Room import Room

class Dungeon:
    def __init__( self, name, theme, width, height ):
        self.name = name
        self.theme = theme

        self.roomlist = []
        for y in range(0, width):
            room_row = []
            for x in range(0, height):
                room_row.append( Room(x,y) )
            self.roomlist.append(room_row)

    def get_room_array(self):
        return self.roomlist
