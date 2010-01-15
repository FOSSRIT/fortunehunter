from Room import Room
from Dungeon import Dungeon
from constants import (
                        THEME_NAME, DOOR_INDEX, DOOR_FLAGS,
                        SPEC_FLAGS, ENEM_INDEX, ITEM_FLAGS,
                        ITEM_INDEX
                      )

from sugar.activity.activity import Activity, ActivityToolbox
from gettext import gettext as _

import gtk

MAX_GRID_WIDTH = 15
MAX_GRID_HEIGHT = 15
MIN_GRID_WIDTH = 2
MIN_GRID_HEIGHT = 2

class FortuneMaker(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.dungeon = None
        self.active_room = None

        # INITIALIZE GUI
        ################
        self.set_title('File Share')

        # Create Toolbox
        toolbox = ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        self.set_create_dungeon_settings()

    def view_change_cb(self, widget, view=None):
        if view == 'stats':
            self.view_dungeon_stats()
        elif view == 'layout':
            self.view_dungeon_grid()
        elif view == 'room':
            self.view_room()

    def set_gui_view(self,  view, buttons=False):
        if buttons:
            box = gtk.VBox()
            box.pack_start( self.get_button_bar(), False )
            box.pack_start(view)
            self.set_canvas( box )
        else:
            self.set_canvas( view )
        self.show_all()

    def get_button_bar(self):
        button_tabs = gtk.HBox()
        stats = gtk.Button( _("Dungeon Summary") )
        stats.set_alignment(0,.5)
        stats.connect( 'clicked', self.view_change_cb, 'stats')
        button_tabs.pack_start( stats, False )

        layout = gtk.Button( _("Dungeon Layout") )
        layout.set_alignment(0,.5)
        layout.connect( 'clicked', self.view_change_cb, 'layout')
        button_tabs.pack_start( layout, False )

        room = gtk.Button( _("Room Layout") )
        room.set_alignment(0,.5)
        room.connect( 'clicked', self.view_change_cb, 'room')
        button_tabs.pack_start( room, False )

        return button_tabs

    def set_create_dungeon_settings(self):
        window_container = gtk.VBox()

        ## Dungeon Properties
        ###############
        frame = gtk.Frame(_("Dungeon Properties"))

        container =  gtk.VBox()

        # Name
        row = gtk.HBox()
        label = gtk.Label(_("Name:"))
        label.set_alignment( 0, 0.5)
        row.pack_start( label )
        name = gtk.Entry()
        row.pack_end( name )
        container.pack_start( row, False )

        # Theme
        row = gtk.HBox()
        label = gtk.Label(_("Theme:"))
        label.set_alignment( 0, 0.5)
        row.pack_start( label )
        theme = gtk.combo_box_new_text()
        for option in THEME_NAME:
            theme.append_text( option )
        theme.set_active( 0 )
        row.pack_end( theme )
        container.pack_start( row, False )

        frame.add( container )
        window_container.pack_start( frame, False )

        ## Dungeon Size
        ###############
        frame = gtk.Frame(_("Dungeon Size"))

        # Width
        widthADJ = gtk.Adjustment(MIN_GRID_WIDTH, MIN_GRID_WIDTH, MAX_GRID_WIDTH, 1.0, 5.0, 0.0)
        widthspin = gtk.SpinButton(widthADJ, 0, 0)
        container = gtk.VBox()
        row = gtk.HBox()
        label = gtk.Label(_("Width:") )
        label.set_alignment( 0, 0.5)
        row.pack_start( label)
        row.pack_end( widthspin )
        container.pack_start( row, False )

        # Height
        heightADJ = gtk.Adjustment(MIN_GRID_HEIGHT, MIN_GRID_HEIGHT, MAX_GRID_HEIGHT, 1.0, 5.0, 0.0)
        heightspin = gtk.SpinButton(heightADJ, 0, 0)
        row = gtk.HBox()
        label = gtk.Label(_("Height:") )
        label.set_alignment( 0, 0.5)
        row.pack_start( label )
        row.pack_end( heightspin )
        container.pack_start( row, False )

        frame.add( container )
        window_container.pack_start( frame, False )

        ## Make Dungeon Button
        make_dungeon = gtk.Button(_("Create Dungeon"))
        make_dungeon.connect("clicked", self.create_dungeon_cb, {'name':name,'theme':theme,'width':widthspin,'height':heightspin})

        window_container.pack_start( make_dungeon, False )

        self.set_gui_view( window_container )

    def create_dungeon_cb(self, widget, data):
        name = data['name'].get_text()
        theme = data['theme'].get_active()  #.get_active_text()
        width = data['width'].get_value_as_int()
        height = data['height'].get_value_as_int()

        self.dungeon = Dungeon( name, theme, width, height )
        self.view_dungeon_stats()

    def view_dungeon_stats(self):
        dungeon_stats = gtk.HBox()
        dungeon_stats.pack_start(gtk.Label("Dungeon Statistics to be implemented"))
        self.set_gui_view( dungeon_stats, True )

    def view_dungeon_grid(self):
        room_array = self.dungeon.get_room_array()
        box = gtk.VBox()
        for row_array in room_array:
            row = gtk.HBox()
            box.pack_start( row, False )
            for room in row_array:
                room_gui = room.render_room()
                room_gui.connect('clicked', self.set_active_room, room)
                row.pack_start( room_gui, False )

        scroll = gtk.ScrolledWindow()
        scroll.add_with_viewport( box )

        self.set_gui_view( scroll, True )

    def view_room(self):
        #TODO CHECK IF ACTIVE ROOM SET

        room_holder = gtk.VBox()

        ## Room Doors
        #############
        frame = gtk.Frame(_("Room Doors"))
        holder = gtk.VBox()

        doors = {}

        door_flags = [ _("None") ]
        door_flags.extend( DOOR_FLAGS.values() )
        for door_key in DOOR_INDEX:
            row = gtk.HBox()
            label = gtk.Label(DOOR_INDEX[door_key])
            label.set_alignment( 0, 0.5 )
            row.pack_start( label )

            doors[door_key] = gtk.combo_box_new_text()

            for value in door_flags:
                doors[door_key].append_text( value )

            door_flag = self.active_room.get_door( door_key )
            if door_flag != '0':
                doors[door_key].set_active( door_flags.index( DOOR_FLAGS[door_flag] ) )
            else:
                doors[door_key].set_active( 0 )

            row.pack_start( doors[door_key] )
            holder.pack_start( row, True )

        frame.add( holder )
        room_holder.pack_start( frame, False )

        ##Room Flags
        ############
        frame = gtk.Frame(_("Room Properties"))
        holder = gtk.VBox()

        row = gtk.HBox()
        label = gtk.Label(_("Room Flag"))
        label.set_alignment( 0, 0.5 )
        row.pack_start( label )

        flag_sel = gtk.combo_box_new_text()
        spec_flags = SPEC_FLAGS.values()
        for flag in spec_flags:
            flag_sel.append_text( flag )

        flag = self.active_room.get_room_flag()
        flag_sel.set_active( spec_flags.index( SPEC_FLAGS[flag] ) )

        row.pack_start( flag_sel )
        holder.pack_start( row, True)

        frame.add( holder )
        room_holder.pack_start( frame, False )

        ## Room Enemies
        ###############
        frame = gtk.Frame(_("Room Enemies"))
        holder = gtk.VBox()

        enem = []

        for i in range(0,4):
            enem.append( gtk.combo_box_new_text() )

            row = gtk.HBox()
            label = gtk.Label("%s (%d)" % (_("Enemy"), i))
            label.set_alignment( 0, 0.5 )

            row.pack_start(label)
            em_list = ENEM_INDEX.values()
            for em in em_list:
                enem[i].append_text( em )

            enem[i].set_active( em_list.index(ENEM_INDEX[self.active_room.get_enemy( i )] ) )
            row.pack_start( enem[i] )

            holder.pack_start( row, False )

        frame.add( holder )
        room_holder.pack_start( frame, False )

        ## Room Items
        #############
        frame = gtk.Frame(_("Room Item"))
        holder = gtk.VBox()

        item_arr = []

        item_list = ITEM_INDEX.values()
        item_flags = ITEM_FLAGS.values()

        for i in range(0,4):
            itemType = gtk.combo_box_new_text()
            itemFlag= gtk.combo_box_new_text()

            for item in item_list:
                itemType.append_text( item )

            #TODO: ADD DEFUALT Flag

            for item in item_flags:
                itemFlag.append_text( item )

            #TODO: ADD DEFUALT Flag

            item_arr.append( [itemType, itemFlag] )

            row = gtk.HBox()
            row.pack_start( itemType )
            row.pack_start( itemFlag )

            holder.pack_start( row, False )

        frame.add( holder )
        room_holder.pack_start( frame, False )

        self.set_gui_view( room_holder, True )

    def set_active_room(self, widgit, room):
        self.active_room  = room
        self.view_room()

if __name__ == "__main__":

    aroom = Room()

    aroom.add_door('N', 'u')
    aroom.add_door('E', 'p')

    aroom.set_enemy(1,'2')
    aroom.set_enemy(3,'4')

    aroom.set_room_flag('P')
    #ADD SET ITEM WHEN CODED

    print aroom.room_to_string()
