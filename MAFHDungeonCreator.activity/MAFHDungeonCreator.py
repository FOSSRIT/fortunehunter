from Room import Room
from Dungeon import Dungeon
from constants import THEME_NAME

from sugar.activity.activity import Activity, ActivityToolbox
from gettext import gettext as _

import gtk

MAX_GRID_WIDTH = 15
MAX_GRID_HEIGHT = 15
MIN_GRID_WIDTH = 2
MIN_GRID_HEIGHT = 2

class MAFHDungeonCreator(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.notebook = gtk.Notebook()

        self.dungeon = None
        self.active_room = None

        # INITIALIZE GUI
        ################
        self.set_title('File Share')

        # Create Toolbox
        toolbox = ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        self.notebook.append_page(self.get_create_dungeon_settings(), gtk.Label(_("Create Dungeon")) )

        self.notebook.connect("switch_page", self.notebook_page_change)


        self.set_gui_view( self.notebook )

    def set_gui_view(self,  view):
        self.set_canvas( view )
        self.show_all()

    def notebook_page_change(self, widget, dummy, pagenum):
    ##WORKING HERE
        page_widget = widget.get_nth_page(pagenum)
        print "Page number switched to: %s" % pagenum
        print "Widget attached to page %s: %s" % ( pagenum, page_widget )


    def get_create_dungeon_settings(self):
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
        container.pack_start( row )

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
        container.pack_start( row )

        frame.add( container )
        window_container.pack_start( frame )

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
        row.pack_start( label )
        row.pack_end( widthspin )
        container.pack_start( row )

        # Height
        heightADJ = gtk.Adjustment(MIN_GRID_HEIGHT, MIN_GRID_HEIGHT, MAX_GRID_HEIGHT, 1.0, 5.0, 0.0)
        heightspin = gtk.SpinButton(heightADJ, 0, 0)
        row = gtk.HBox()
        label = gtk.Label(_("Height:") )
        label.set_alignment( 0, 0.5)
        row.pack_start( label )
        row.pack_end( heightspin )
        container.pack_start( row )

        frame.add( container )
        window_container.pack_start( frame )

        ## Make Dungeon Button
        make_dungeon = gtk.Button(_("Create Dungeon"))
        make_dungeon.connect("clicked", self.create_dungeon_cb, {'name':name,'theme':theme,'width':widthspin,'height':heightspin})

        window_container.pack_start( make_dungeon )

        return window_container

    def create_dungeon_cb(self, widget, data):
        name = data['name'].get_text()
        theme = data['theme'].get_active()  #.get_active_text()
        width = data['width'].get_value_as_int()
        height = data['height'].get_value_as_int()

        self.dungeon = Dungeon( name, theme, width, height )

        page = self.notebook.get_current_page()
        self.notebook.remove_page(page)

        self.setup_dungeon_grid()

    def setup_dungeon_grid(self):
        self.notebook.append_page(self.get_dungeon_stats(), gtk.Label(_("Dungeon Summery")) )
        self.notebook.append_page(self.get_dungeon_grid(), gtk.Label(_("Dungeon Layout")) )
        self.notebook.append_page(self.get_room_setup(), gtk.Label(_("Room Layout")))
        self.show_all()
        self.notebook.queue_draw_area(0,0,-1,-1)


    def get_dungeon_stats(self):
        dungeon_stats = gtk.HBox()
        dungeon_stats.pack_start(gtk.Label("Dungeon Statistics to be implemented"))
        return dungeon_stats

    def get_dungeon_grid(self):
        box = gtk.VBox()

        room_array = self.dungeon.get_room_array()
        for row_array in room_array:
            row = gtk.HBox()
            box.pack_start( row )
            for room in row_array:
                room_gui = room.render_room()
                room_gui.connect('clicked', self.set_active_room, room)
                row.pack_start( room_gui )

        scroll = gtk.ScrolledWindow()
        scroll.add_with_viewport( box )

        return scroll

    def set_active_room(self, widgit, room):
        self.active_room  = room
        self.notebook.set_page(2)

    def get_room_setup(self):
        dungeon_stats = gtk.HBox()
        dungeon_stats.pack_start(gtk.Label("room to be implemented"))
        return dungeon_stats

if __name__ == "__main__":

    aroom = Room()

    aroom.add_door('N', 'u')
    aroom.add_door('E', 'p')

    aroom.set_enemy(1,'2')
    aroom.set_enemy(3,'4')

    aroom.set_room_flag('P')
    #ADD SET ITEM WHEN CODED

    print aroom.room_to_string()
