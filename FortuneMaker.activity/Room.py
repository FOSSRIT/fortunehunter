from constants import (
    DOOR_ORDER, DOOR_INDEX, DOOR_FLAGS, SPEC_FLAGS,
    ENEM_INDEX, ITEM_INDEX, ITEM_FLAGS, DOOR_COLOR,
    SPEC_COLOR
    )

import gtk
import pango

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
            self.doors[door] = ['0', '0']
            self.has_doors = False
            for door in self.doors:
                if self.doors[door][1] != "0":
                    self.has_doors = True
                    break

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

    def add_item( self, item, flag ):
        for index in range( 0,4 ):
            if self.item[index][0] == "0":
                return self.set_item(index, item, flag)
        return False

    def set_item(self, pos, id, flag):
        if pos >= 0 and pos <=3 and id in ITEM_INDEX and flag in ITEM_FLAGS:
            self.item[ pos ] = [id, flag]

            self.has_item = False
            for item in self.item:
                if item[0] != "0":
                    self.has_item = True
                    break

            return True
        else:
            print "INVALID POS OR ID OR FLAG"
            return False

    def get_item(self, pos):
        if pos >=0 and pos <=3:
            return self.item[pos]

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
        def expose_handler(widget, event):
            w, h = widget.window.get_size()
            xgc = widget.window.new_gc()

            door_thick = 5
            third_w = w / 3
            third_h = h / 3

            # Fill in if room
            if self.not_empty_room():
                xgc.set_rgb_fg_color(gtk.gdk.color_parse(SPEC_COLOR[self.special]))
                widget.window.draw_rectangle(xgc, True, 1, 1, w-2, h-2)

            # Draw Border
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000000"))
            widget.window.draw_rectangle(xgc, False, 1, 1, w-2, h-2)

            if self.doors['N'][1] != '0':
                xgc.set_rgb_fg_color(gtk.gdk.color_parse(DOOR_COLOR[self.doors['N'][1]]))
                widget.window.draw_rectangle(xgc, True, third_w, 1, third_w, door_thick)

            if self.doors['S'][1] != '0':
                xgc.set_rgb_fg_color(gtk.gdk.color_parse(DOOR_COLOR[self.doors['S'][1]]))
                widget.window.draw_rectangle(xgc, True, third_w, h-door_thick, third_w, door_thick)

            if self.doors['E'][1] != '0':
                xgc.set_rgb_fg_color(gtk.gdk.color_parse(DOOR_COLOR[self.doors['E'][1]]))
                widget.window.draw_rectangle(xgc, True, w-door_thick, third_h, door_thick, third_h)

            if self.doors['W'][1] != '0':
                xgc.set_rgb_fg_color(gtk.gdk.color_parse(DOOR_COLOR[self.doors['W'][1]]))
                widget.window.draw_rectangle(xgc, True, 1, third_h, door_thick, third_h)

            room_text = ""

            for enemy in self.enemy:
                if enemy != '0':
                    room_text += ENEM_INDEX[enemy] + "\n"

            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000000"))
            font_desc = pango.FontDescription('Serif 4')
            layout = widget.create_pango_layout( room_text )
            layout.set_font_description(font_desc)
            widget.window.draw_layout(xgc, 7, 7, layout)

        drawing_area = gtk.DrawingArea()
        drawing_area.set_size_request(100, 100)
        drawing_area.connect("expose-event", expose_handler)
        drawing_area.set_events(gtk.gdk.BUTTON_PRESS_MASK)

        return drawing_area
