from Room import Room
from Dungeon import Dungeon
from constants import (
                        THEME_NAME, DOOR_INDEX, DOOR_FLAGS,
                        SPEC_FLAGS, ENEM_INDEX, ITEM_FLAGS,
                        ITEM_INDEX, DOOR_COLOR, SPEC_COLOR
                      )

from sugar.activity.activity import Activity, ActivityToolbox
from sugar.datastore import datastore
from gettext import gettext as _

from sugar.activity.activity import ActivityToolbox
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.icon import Icon
from sugar.graphics.alert import NotifyAlert

import gtk
import os
import re
FILE_MIME = "application/x-fortune-map"

MAX_GRID_WIDTH = 15
MAX_GRID_HEIGHT = 15
MIN_GRID_WIDTH = 2
MIN_GRID_HEIGHT = 2

class BadInputException(Exception):pass

class FortuneMaker(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.dungeon = None
        self.active_room = None
        self.action_but_group = None

        # INITIALIZE GUI
        ################
        self.set_title('FortuneMaker')

        # Create Toolbox
        self.build_toolbars()
        self.enable_room_icons(False)

        self.show_home()

    def build_toolbars(self):
        self.dungeon_buttons = {}
        self.dungeon_bar = gtk.Toolbar()
        self.view_bar = gtk.Toolbar()

        # BUILD CUSTOM TOOLBAR
        # Dungeon Bar
        self.dungeon_buttons['new'] = ToolButton('add')
        self.dungeon_buttons['new'].set_tooltip(_("New Dungeon"))
        self.dungeon_buttons['new'].connect("clicked", self.view_change_cb, 'new')
        self.dungeon_bar.insert(self.dungeon_buttons['new'], -1)

        self.dungeon_buttons['load'] = ToolButton('fileopen')
        self.dungeon_buttons['load'].set_tooltip(_("Open Dungeon"))
        self.dungeon_buttons['load'].connect("clicked", self.view_change_cb, 'load')
        self.dungeon_bar.insert(self.dungeon_buttons['load'], -1)

        self.dungeon_buttons['save'] = ToolButton('filesave')
        self.dungeon_buttons['save'].set_tooltip( _("Export dungeon file to journal") )
        self.dungeon_buttons['save'].connect("clicked", self.view_change_cb, 'export')
        self.dungeon_bar.insert(self.dungeon_buttons['save'], -1)
        self.dungeon_buttons['save'].set_sensitive( False )

        # VIEW BAR
        self.dungeon_buttons['home'] = ToolButton('go-home')
        self.dungeon_buttons['home'].set_tooltip(_("Welcome Screen"))
        self.dungeon_buttons['home'].connect("clicked", self.view_change_cb, 'home')
        self.view_bar.insert(self.dungeon_buttons['home'], -1)

        self.dungeon_buttons['settings'] = ToolButton('view-spiral')
        self.dungeon_buttons['settings'].set_tooltip(_("View Dungeon Settings"))
        self.dungeon_buttons['settings'].connect("clicked", self.view_change_cb, 'settings')
        self.view_bar.insert(self.dungeon_buttons['settings'], -1)
        self.dungeon_buttons['settings'].set_sensitive( False )

        self.dungeon_buttons['layout'] = ToolButton('view-freeform')
        self.dungeon_buttons['layout'].set_tooltip(_("View Dungeon Layout"))
        self.dungeon_buttons['layout'].connect("clicked", self.view_change_cb, 'layout')
        self.view_bar.insert(self.dungeon_buttons['layout'], -1)
        self.dungeon_buttons['layout'].set_sensitive( False )

        self.toolbox = ActivityToolbox(self)

        # Remove Share Bar
        activity_toolbar = self.toolbox.get_activity_toolbar()
        activity_toolbar.remove(activity_toolbar.share)
        activity_toolbar.share = None

        #Add our custom items to the toolbar
        self.toolbox.add_toolbar(_("Dungeon"), self.dungeon_bar)
        self.toolbox.add_toolbar(_("View"), self.view_bar)

        self.set_toolbox(self.toolbox)
        self.toolbox.show()

    def enable_room_icons(self, dn=True):
        self.dungeon_buttons['settings'].set_sensitive( dn )
        self.dungeon_buttons['save'].set_sensitive( dn )
        self.dungeon_buttons['layout'].set_sensitive( dn )


    def view_change_cb(self, widget, view=None):
        if view == 'layout':
            self.view_dungeon_grid()
        elif view == 'export':
            self.export_view()
        elif view == 'new':
            self.set_create_dungeon_settings()
        elif view == 'load':
            self.show_dungeon_selection()
        elif view == 'settings':
            self.show_dungeon_settings()
        elif view == 'home':
            self.show_home()

    def list_fh_files(self):
        ds_objects, num_objects = datastore.find({'FortuneMaker_VERSION':'1'})
        file_list = []
        for i in xrange(0, num_objects, 1):
            if ds_objects[i].metadata.has_key('FM_UID'):
                file_list.append( ds_objects[i] )
            else:
                #TODO: Attempt to read uid from file?
                self._alert('WARNING: File missing uid',ds_objects.metadata['title'])
        return file_list

    def show_home(self):
        window_container = gtk.VBox()

        label = gtk.Label(_("Welcome Message Here"))
        window_container.pack_start(label, False)

        # New Dungeon
        button = gtk.Button()
        button.set_image( Icon( icon_name="add" ) )
        button.set_label( _("New Dungeon") )
        button.set_alignment(0.0,0.5)
        button.connect( 'clicked', self.view_change_cb, 'new')
        window_container.pack_start(button, False)

        # load fileopen
        button = gtk.Button()
        button.set_image( Icon( icon_name="fileopen" ) )
        button.set_label( _("Load Exported Dungeon") )
        button.set_alignment(0.0,0.5)
        button.connect( 'clicked', self.view_change_cb, 'load')
        window_container.pack_start(button, False)

        #HELP EXAMPLES
        label = gtk.Label(_("Dungeon Toolbar") )
        label.set_alignment( 0, 0.5 )
        window_container.pack_start(gtk.Label(" "), False)
        window_container.pack_start(label, False)

        row = gtk.HBox()
        row.pack_start( Icon( icon_name="add" ), False )
        label = gtk.Label( _("Creates New Dungeon") )
        label.set_alignment( 0, 0.5 )
        row.pack_start(gtk.Label(" "), False)
        row.pack_start( label )
        window_container.pack_start(row, False)

        row = gtk.HBox()
        row.pack_start( Icon( icon_name="fileopen" ), False )
        label = gtk.Label( _("Opens existing dungeon file") )
        label.set_alignment( 0, 0.5 )
        row.pack_start(gtk.Label(" "), False)
        row.pack_start( label )
        window_container.pack_start(row, False)

        row = gtk.HBox()
        row.pack_start( Icon( icon_name="filesave" ), False )
        label = gtk.Label( _("Export dungeon file to journal") )
        label.set_alignment( 0, 0.5 )
        row.pack_start(gtk.Label(" "), False)
        row.pack_start( label )
        window_container.pack_start(row, False)

        # View Bar Help
        label = gtk.Label(_("View Toolbar") )
        label.set_alignment( 0, 0.5 )
        window_container.pack_start(gtk.Label(" "), False)
        window_container.pack_start(label, False)

        row = gtk.HBox()
        row.pack_start( Icon( icon_name="go-home" ), False )
        label = gtk.Label( _("Display this home screen") )
        label.set_alignment( 0, 0.5 )
        row.pack_start(gtk.Label(" "), False)
        row.pack_start( label )
        window_container.pack_start(row, False)

        row = gtk.HBox()
        row.pack_start( Icon( icon_name="view-spiral" ), False )
        label = gtk.Label( _("Shows the dungeon settings") )
        label.set_alignment( 0, 0.5 )
        row.pack_start(gtk.Label(" "), False)
        row.pack_start( label )
        window_container.pack_start(row, False)

        row = gtk.HBox()
        row.pack_start( Icon( icon_name="view-freeform" ), False )
        label = gtk.Label( _("Shows the dungeon layout") )
        label.set_alignment( 0, 0.5 )
        row.pack_start(gtk.Label(" "), False)
        row.pack_start( label )
        window_container.pack_start(row, False)

        window_container.pack_start( gtk.Label(" "), False )
        label = gtk.Label(_("Files must be exported before they\n" +
                            "may be loaded into Fortune Hunter\n" +
                            "or linked as a next dungeon."))
        window_container.pack_start( label, False)

        room_center = gtk.HBox()
        room_center.pack_start( gtk.Label() )
        room_center.pack_start( window_container )
        room_center.pack_start( gtk.Label() )

        self.set_gui_view( room_center )

    def export_view(self):
        data = self.dungeon.export()

        textbuffer = gtk.Label()
        filename = self.dungeon.name

        self._write_textfile( filename, data)

        textbuffer.set_text( "File Saved to %s"%(filename) )

        self.set_gui_view( textbuffer )



    #### Method: _write_textfile, which creates a simple text file
    # with filetext as the data put in the file.
    # @Returns: a DSObject representing the file in the datastore.
    def _write_textfile(self, filename, filetext=''):
        ds_objects, num_objects = datastore.find({'title':filename,'FortuneMaker_VERSION':'1'})

        if num_objects == 0:
            # Create a datastore object
            file_dsobject = datastore.create()

        else:
            file_dsobject = ds_objects[0]

        # Store unique id for easy search of journal
        file_dsobject.metadata['FM_UID'] = self.dungeon.id

        # Write any metadata (here we specifically set the title of the file and
        # specify that this is a plain text file).
        file_dsobject.metadata['title'] = filename
        file_dsobject.metadata['mime_type'] = FILE_MIME
        file_dsobject.metadata['FortuneMaker_VERSION'] = '1'

        #Write the actual file to the data directory of this activity's root.
        file_path = os.path.join(self.get_activity_root(), 'instance', filename)
        f = open(file_path, 'w')
        try:
            f.write(filetext)
        finally:
            f.close()

        #Set the file_path in the datastore.
        file_dsobject.set_file_path(file_path)

        datastore.write(file_dsobject)
        return file_dsobject


    def set_gui_view(self,  view):
        self.set_canvas( view )
        self.show_all()


    def show_dungeon_selection(self):
        window_container = gtk.VBox()
        frame = gtk.Frame( _("Load Dungeon") )
        file_container = gtk.VBox()

        ##LOAD FILE LIST HERE
        file_list = self.list_fh_files()

        for dfile in file_list:
            row = gtk.HBox()
            label = gtk.Label(dfile.metadata['title'])
            row.pack_start( label, False )

            button = gtk.Button(_("Load"))
            button.connect( 'clicked', self.load_dungeon, dfile )
            row.pack_end(button, False)

            file_container.pack_start( row, False )

        frame.add( make_it_scroll( file_container ) )
        window_container.pack_start( frame )

        room_center = gtk.HBox()
        room_center.pack_start( gtk.Label() )
        room_center.pack_start( window_container )
        room_center.pack_start( gtk.Label() )

        self.set_gui_view( room_center )



    def show_dungeon_settings(self):
        window_container, name, theme, next_dungeon, file_list_map = self._get_dungeon_prop_box(False)

        save_dungeon = gtk.Button(_("Save Dungeon Settings"))
        save_dungeon.connect("clicked", self.edit_dungeon_cb, {'name':name,
                                'theme':theme, 'next_dungeon':next_dungeon,
                                'd_list':file_list_map})

        window_container.pack_start( save_dungeon, False )

        room_center = gtk.HBox()
        room_center.pack_start( gtk.Label() )
        room_center.pack_start( window_container )
        room_center.pack_start( gtk.Label() )

        self.set_gui_view( room_center )

    def _get_dungeon_prop_box(self, new_prop=True):
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

        # Next Dungeon
        row = gtk.HBox()
        label = gtk.Label(_("Next Dungeon:"))
        label.set_alignment( 0, .5)
        row.pack_start( label )

        next_dungeon = gtk.combo_box_new_text()

        file_list = self.list_fh_files()
        file_list_map = {}
        file_list_map["0"] = _("None")
        next_dungeon.append_text( file_list_map["0"] )
        next_dungeon.set_active(0)
        order_map = ["0"]

        for dfile in file_list:
            file_list_map[dfile.metadata['FM_UID']] = dfile.metadata['title']
            next_dungeon.append_text( dfile.metadata['title'] )
            order_map.append( dfile.metadata['FM_UID'] )

        row.pack_start(next_dungeon)
        container.pack_start( row, False )

        frame.add( container )
        window_container.pack_start( frame, False )

        if not new_prop and self.dungeon:
            name.set_text( self.dungeon.name )
            theme.set_active( self.dungeon.theme )
            next_dungeon.set_active( order_map.index( self.dungeon.next ) )

        return (window_container, name, theme, next_dungeon, file_list_map)

    def set_create_dungeon_settings(self, trash=None, trash2=None):
        window_container, name, theme, next_dungeon, file_list_map = self._get_dungeon_prop_box(True)

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
        make_dungeon.connect("clicked", self.create_dungeon_cb, {'name':name,
                                'theme':theme,'width':widthspin, 'height':heightspin,
                                'next_dungeon':next_dungeon, 'd_list':file_list_map})

        window_container.pack_start( make_dungeon, False )

        room_center = gtk.HBox()
        room_center.pack_start( gtk.Label() )
        room_center.pack_start( window_container )
        room_center.pack_start( gtk.Label() )

        self.set_gui_view( room_center )

    def load_dungeon(self, widget, file_data):
        dgnFile=open(file_data.get_file_path(),'r')
        self.do_load( dgnFile)
        dngFile.close()

    def do_load( self, dgnFile ):
        grab = 0
        room_str = []
        for line in dgnFile:
            if grab == 0:
                name = line.strip()
                grab = 1

            elif grab == 1:
                d_id = line.strip()
                grab = 2

            elif grab == 2:
                match = re.match('(\d+)x(\d+)',line)
                if match:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    grab = 3
                else:
                    raise BadInputException()

            elif grab == 3:
                theme = int(line)
                grab = 4

            elif grab == 4:
                next = line.strip()
                grab = 5

            elif grab == 5:
                room_str.append(line.strip())

        if grab == 5:
            self.dungeon = Dungeon( name, theme, next, x, y, room_str, d_id)
            self.enable_room_icons(True)
            self.view_dungeon_grid()


    def edit_dungeon_cb(self, widget, data):
        self.dungeon.name = data['name'].get_text()
        self.dungeon.theme = data['theme'].get_active()
        self.dungeon.next = find_key( data['d_list'], data['next_dungeon'].get_active_text())
        self._alert(_("Dungeon Setting Saved"), self.dungeon.theme)

    def create_dungeon_cb(self, widget, data):
        name = data['name'].get_text()
        theme = data['theme'].get_active()  #.get_active_text()
        next = find_key( data['d_list'], data['next_dungeon'].get_active_text())
        width = data['width'].get_value_as_int()
        height = data['height'].get_value_as_int()

        self.dungeon = Dungeon( name, theme, next, width, height )
        self.enable_room_icons(True)
        self.view_dungeon_grid()

    def _draw_room_button_grid(self):
        # Setup Room Pannel
        room_array = self.dungeon.get_room_array()
        box = gtk.VBox()
        for row_array in room_array:
            row = gtk.HBox()
            box.pack_start( row, False )
            for room in row_array:
                room_gui = room.render_room()
                room_gui.connect('button-press-event', self.add_prop_to_room, room, room_gui)
                row.pack_start( room_gui, False )
        if self._pane2:
            self.edit_pane.remove( self._pane2 )
        self._pane2 = make_it_scroll( box )
        self._pane2.show_all()
        self.edit_pane.add2( self._pane2 )

    def view_dungeon_grid(self):
        self.edit_pane = gtk.HPaned()
        self._pane2 = None

        # Setup Button Pannel
        listbox = gtk.VBox()

        lbl = gtk.RadioButton(None,_('Remove Enemy'))
        lbl.track_mode = 'REM_ENEMY'
        listbox.pack_start( lbl, False )

        lbl = gtk.RadioButton(lbl,_('Remove Item'))
        lbl.track_mode = 'REM_ITEM'
        listbox.pack_start( lbl, False )

        # Doors
        exp = gtk.Expander(_("Doors"))
        box = gtk.VBox()

        for door_mode_key in DOOR_FLAGS:
            lbl = gtk.RadioButton(lbl,DOOR_FLAGS[door_mode_key])
            lbl.track_mode = 'DOOR'

            lbl.track_flag = door_mode_key
            box.pack_start(lbl, False)

        exp.add( box )
        listbox.pack_start( exp, False )

        # Room Properties
        exp = gtk.Expander(_("Room Flags"))
        box = gtk.VBox()
        SPEC_FLAGS
        for flag_key in SPEC_FLAGS:
            lbl = gtk.RadioButton(lbl, SPEC_FLAGS[flag_key])
            lbl.track_mode = 'SPEC_FLAG'
            lbl.track_flag = flag_key
            box.pack_start(lbl, False)
        exp.add( box )
        listbox.pack_start( exp, False )

        # Enemies
        exp = gtk.Expander(_("Enemies"))
        box = gtk.VBox()
        for enemy_key in ENEM_INDEX:
            # Ignore None Key
            if enemy_key != '0':
                lbl = gtk.RadioButton(lbl, ENEM_INDEX[enemy_key])
                lbl.track_mode = 'ENEMY'
                lbl.track_flag = enemy_key
                box.pack_start(lbl, False)

        exp.add( box )
        listbox.pack_start( exp, False )

        # Items
        exp = gtk.Expander(_("Items"))
        box = gtk.VBox()
        for item_key in ITEM_INDEX:
            # Ignore None Key
            if item_key != '0':
                lbl = gtk.RadioButton(lbl,ITEM_INDEX[item_key])
                lbl.track_mode = 'ITEM'
                lbl.track_flag = item_key
                box.pack_start(lbl, False)

        exp.add(box)
        listbox.pack_start( exp, False )

        # Save the button group
        self.action_but_group = lbl.get_group()

        # Make Legend
        legendBox = gtk.VBox()
        legendBox.pack_start(gtk.Label(_("Door Legend")),False)

        for door_key in DOOR_FLAGS:
            if door_key != '0':
                row = gtk.HBox()
                colorbox = gtk.EventBox()
                colorbox.add( gtk.Label("    ") )
                colorbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(DOOR_COLOR[door_key]))
                row.pack_start(colorbox, False)
                row.pack_start( gtk.Label("  "), False )
                label = gtk.Label(DOOR_FLAGS[door_key])
                label.set_alignment( 0, 0.5 )
                row.pack_start( label )
                legendBox.pack_start(row, False)

        legendBox.pack_start(gtk.Label(_("Room Legend")),False)

        for spec_key in SPEC_FLAGS:
            if spec_key != '0':
                row = gtk.HBox()
                colorbox = gtk.EventBox()
                colorbox.add( gtk.Label("    ") )
                colorbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(SPEC_COLOR[spec_key]))
                row.pack_start(colorbox, False)
                row.pack_start( gtk.Label("  "), False )
                label = gtk.Label(SPEC_FLAGS[spec_key])
                label.set_alignment( 0, 0.5 )
                row.pack_start( label )
                legendBox.pack_start(row, False)


        split = gtk.VBox()
        split.pack_start( make_it_scroll( listbox, False ) )

        exp = gtk.Expander(_("Legend"))
        exp.add(legendBox)
        split.pack_end( exp, False )

        self.edit_pane.add1( split )
        self._draw_room_button_grid()
        self.set_gui_view( self.edit_pane )

    def set_active_room(self, widgit, room):
        self.active_room = room
        self.view_room()

    def add_prop_to_room(self, widget, event, room, room_gui):
        self.active_room = room
        for but in self.action_but_group:
            if but.get_active():
                if but.track_mode == 'VIEW':
                    self.view_room()
                    return

                elif but.track_mode == 'REM_ENEMY':
                    dialog = gtk.Dialog(_("Remove Enemy"), buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
                    def rem_enm(widget, pos, row):
                        room.set_enemy( pos, '0')
                        row.hide()

                    display_box = False
                    for i in range(0,4):
                        if room.enemy[i] != '0':
                            display_box = True
                            row = gtk.HBox()
                            label = gtk.Label( ENEM_INDEX[room.enemy[i]] )
                            label.set_alignment(0.0,0.5)
                            row.pack_start(label)
                            but = gtk.Button(_("Remove"))
                            but.connect('clicked', rem_enm, i, row)
                            row.pack_end(but, False)
                            dialog.vbox.pack_start(row, False)

                    if display_box:
                        dialog.show_all()
                        result = dialog.run()
                    else:
                        self._alert(_("No enemies found in this room"))
                    dialog.destroy()

                elif but.track_mode == 'REM_ITEM':
                    dialog = gtk.Dialog(_("Remove Item"), buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))

                    def rem_enm(widget, pos, row):
                        room.set_item( pos, '0', '0')
                        row.hide()

                    display_box = False
                    for i in range(0,4):
                        if room.item[i][0] != '0':
                            display_box = True
                            row = gtk.HBox()
                            label = gtk.Label( ITEM_INDEX[room.item[i][0]] )
                            label.set_alignment(0.0,0.5)
                            row.pack_start(label)
                            but = gtk.Button(_("Remove"))
                            but.connect('clicked', rem_enm, i, row)
                            row.pack_end(but, False)
                            dialog.vbox.pack_start(row, False)

                    if display_box:
                        dialog.show_all()
                        result = dialog.run()
                    else:
                        self._alert(_("No items found in this room"))
                    dialog.destroy()


                elif but.track_mode == 'DOOR':
                    door_pos = room.get_door_from_click( event.x, event.y )
                    if not door_pos:
                        return

                    if but.track_flag == '0':
                        self.active_room.remove_door( door_pos )
                        try:
                            adj_room = self.dungeon.get_adj_room( room, door_pos )
                            if door_pos == "N":
                                adj_room.remove_door( "S" )
                            elif door_pos == "E":
                                adj_room.remove_door( "W" )
                            elif door_pos == "S":
                                adj_room.remove_door( "N" )
                            elif door_pos == "W":
                                adj_room.remove_door( "E" )
                            adj_room._room_gui.queue_draw()
                        except:
                            pass

                    else:
                        # If not e or x, add door to adjoining room
                        if not (but.track_flag == 'e' or but.track_flag == 'x'):
                            adj_room = self.dungeon.get_adj_room( room, door_pos )

                            if adj_room:
                                self.active_room.add_door( door_pos, but.track_flag )
                                if door_pos == "N":
                                    adj_room.add_door( "S", but.track_flag)
                                elif door_pos == "E":
                                    adj_room.add_door( "W", but.track_flag)
                                elif door_pos == "S":
                                    adj_room.add_door( "N", but.track_flag)
                                elif door_pos == "W":
                                    adj_room.add_door( "E", but.track_flag)
                                adj_room._room_gui.queue_draw()
                            else:
                                self._alert( _("Door Not Added"), _("This door can not be placed at edge of dungeon"))
                        else:
                            self.active_room.add_door( door_pos, but.track_flag )


                elif but.track_mode == 'SPEC_FLAG':
                    self.active_room.set_room_flag( but.track_flag )

                elif but.track_mode == 'ENEMY':
                    if not self.active_room.add_enemy( but.track_flag ):
                        self._alert( _("Enemy not added to room"), _("Room can not hold any more enemies"))

                elif but.track_mode == 'ITEM':

                    def add_item(click, flag):
                        if not self.active_room.add_item( but.track_flag, flag ):
                            self._alert( _("Item not added to room"), _("Room can not hold any more items"))
                        self.dungeon.update_room( self.active_room )
                        room_gui.queue_draw()

                    menu = gtk.Menu()
                    for flag in ITEM_FLAGS:
                        if flag != '0':
                            opt = gtk.MenuItem(ITEM_FLAGS[flag])
                            opt.connect("activate", add_item, flag)
                            menu.append(opt)

                    menu.show_all()
                    menu.popup(None, None, None, event.button, event.get_time())
                    return

                self.dungeon.update_room( self.active_room )
                room_gui.queue_draw()
                #self._draw_room_button_grid()
                break

    def _alert(self, title, text=None, timeout=5):
        alert = NotifyAlert(timeout=timeout)
        alert.props.title = title
        alert.props.msg = text
        self.add_alert(alert)
        alert.connect('response', self._alert_cancel_cb)
        alert.show()

    def _alert_cancel_cb(self, alert, response_id):
        self.remove_alert(alert)

    def read_file(self, file_path):
        if hasattr(self, "SHUT_UP_XO_CALLING_ME"):
            print "CALLED YET AGAIN! (%s)"%file_path
            return

        self.SHUT_UP_XO_CALLING_ME = True
        dgnFile=open(file_path,'r')
        self.do_load( dgnFile )
        dgnFile.close()
        return

    def write_file(self, file_path):
        if self.dungeon:
            f = open( file_path, 'w' )
            f.write( self.dungeon.export() )
            f.close()
            self.metadata['dungeon_title'] = self.dungeon.name
        else:
            # Basically touch file to prevent it from keep error
            open( file_path, 'w' ).close()


#### HELPER FUNCTIONS ####
def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    try:
        return [k for k, v in dic.iteritems() if v == val][0]
    except:
        return False

def make_it_scroll(widget, allow_horz=True):
    scroll = gtk.ScrolledWindow()
    if allow_horz:
        scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
    else:
        scroll.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
    scroll.add_with_viewport( widget )
    return scroll
