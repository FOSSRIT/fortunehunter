import pygtk
pygtk.require('2.0')
import gtk, gobject
import pango
import md5
import logging
import os

IMG_PATH = os.path.dirname(__file__) + "/images/"

import utils
from types import TupleType, ListType
from random import random
from time import time
from math import sqrt
from cStringIO import StringIO


up_key =    ['Up', 'KP_Up', 'KP_8']
down_key =  ['Down', 'KP_Down', 'KP_2']
left_key =  ['Left', 'KP_Left', 'KP_4']
right_key = ['Right', 'KP_Right', 'KP_6']

SLIDE_UP = 1
SLIDE_DOWN = 2
SLIDE_LEFT = 3
SLIDE_RIGHT = 4

THUMB_SIZE = 48
IMAGE_SIZE = 200
GAME_SIZE = 574

COLOR_FRAME_OUTER = "#B7B7B7"
COLOR_FRAME_GAME = "#FF0099"
COLOR_FRAME_THUMB = COLOR_FRAME_GAME
COLOR_FRAME_CONTROLS = "#FFFF00"
COLOR_BG_CONTROLS = "#66CC00"
COLOR_FG_BUTTONS = (
    (gtk.STATE_NORMAL,"#CCFF99"),
    (gtk.STATE_ACTIVE,"#CCFF99"),
    (gtk.STATE_PRELIGHT,"#CCFF99"),
    (gtk.STATE_SELECTED,"#CCFF99"),
    (gtk.STATE_INSENSITIVE,"#CCFF99"),
    )
COLOR_BG_BUTTONS = (
    (gtk.STATE_NORMAL,"#027F01"),
    (gtk.STATE_ACTIVE,"#014D01"),
    (gtk.STATE_PRELIGHT,"#016D01"),
    (gtk.STATE_SELECTED,"#027F01"),
    (gtk.STATE_INSENSITIVE,"#CCCCCC"),
    )


def calculate_matrix (pieces):
    """ Given a number of pieces, calculate the best fit 2 dimensional matrix """
    rows = int(sqrt(pieces))
    cols = int(float(pieces) / rows)
    return rows*cols, rows, cols
    
def prepare_btn(btn, w=-1, h=-1):
    for state, color in COLOR_BG_BUTTONS:
        btn.modify_bg(state, gtk.gdk.color_parse(color))
    c = btn.get_child()
    if c is not None:
        for state, color in COLOR_FG_BUTTONS:
            c.modify_fg(state, gtk.gdk.color_parse(color))
    else:
        for state, color in COLOR_FG_BUTTONS:
            btn.modify_fg(state, gtk.gdk.color_parse(color))
    if w>0 or h>0:
        btn.set_size_request(w, h)
    return btn


class SliderCreator (gtk.gdk.Pixbuf):
    def __init__ (self, width, height, fname=None, tlist=None): #tlist):
        if width == -1:
            width = 564
        if height == -1:
            height = 564
        super(SliderCreator, self).__init__(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
        if tlist is None:
          items = []
          cmds = file(fname).readlines()
          if len(cmds) > 1:
              _x_ = eval(cmds[0])
              for i in range(16):
                  items.append(_x_)
                  _x_ = eval(cmds[1])
        else:
            items = tlist
        self.width = width
        self.height = height
        self.tlist = items
        self.prepare_stringed(2,2)

    #def scale_simple (self, w,h,m):
    #    return SliderCreator(w,h,tlist=self.tlist)

    #def subpixbuf (self, x,y,w,h):
    #    return SliderCreator(w,h,tlist=self.tlist)

    @classmethod
    def can_handle(klass, fname):
        return fname.lower().endswith('.sequence')

    def prepare_stringed (self, rows, cols):
        # We use a Pixmap as offscreen drawing canvas
        cm = gtk.gdk.colormap_get_system()
        pm = gtk.gdk.Pixmap(None, self.width, self.height, cm.get_visual().depth)
        #pangolayout = pm.create_pango_layout("")
        font_size = int(self.width / cols / 4)
        l = gtk.Label()
        pangolayout = pango.Layout(l.create_pango_context())
        pangolayout.set_font_description(pango.FontDescription("sans bold %i" % font_size))
        gc = pm.new_gc()
        gc.set_colormap(gtk.gdk.colormap_get_system())
        color = cm.alloc_color('white')
        gc.set_foreground(color)
        pm.draw_rectangle(gc, True, 0, 0, self.width, self.height)
        color = cm.alloc_color('black')
        gc.set_foreground(color)

        sw, sh = (self.width / cols), (self.height / rows)
        item = iter(self.tlist)
        for r in range(rows):
            for c in range(cols):
                px = sw * c
                py = sh * r
                #if c > 0 and r > 0:
                #    pm.draw_line(gc, px, 0, px, self.height-1)
                #    pm.draw_line(gc, 0, py, self.width-1, py)
                pangolayout.set_text(str(item.next()))
                pe = pangolayout.get_pixel_extents()
                pe = pe[1][2]/2, pe[1][3]/2
                pm.draw_layout(gc, px + (sw / 2) - pe[0],  py + (sh / 2) - pe[1], pangolayout)
        self.get_from_drawable(pm, cm, 0, 0, 0, 0, -1, -1)

utils.register_image_type(SliderCreator)

###
# Game Logic
###

class MatrixPosition (object):
    """ Helper class to hold a x/y coordinate, and move it by passing a direction,
    taking care of enforcing boundaries as needed.
    The x and y coords are 0 based. """
    def __init__ (self, rowsize, colsize, x=0, y=0):
        self.rowsize = rowsize
        self.colsize = colsize
        self.x = min(x, colsize-1)
        self.y = min(y, rowsize-1)

    def __eq__ (self, other):
        if isinstance(other, (TupleType, ListType)) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        return False

    def __ne__ (self, other):
        return not self.__eq__ (other)

    def bottom_right (self):
        """ Move to the lower right position of the matrix, having 0,0 as the top left corner """
        self.x = self.colsize - 1
        self.y = self.rowsize-1

    def move (self, direction, count=1):
        """ Moving direction is actually the opposite of what is passed.
        We are moving the hole position, so if you slice a piece down into the hole,
        that hole is actually moving up.
        Returns bool, false if we can't move in the requested direction."""
        if direction == SLIDE_UP and self.y < self.rowsize-1:
            self.y += 1
            return True
        if direction == SLIDE_DOWN and self.y > 0:
            self.y -= 1
            return True
        if direction == SLIDE_LEFT and self.x < self.colsize-1:
            self.x += 1
            return True
        if direction == SLIDE_RIGHT and self.x > 0:
            self.x -= 1
            return True
        return False

    def clone (self):
        return MatrixPosition(self.rowsize, self.colsize, self.x, self.y)
        

class SliderPuzzleMap (object):
    """ This class holds the game logic.
    The current pieces position is held in self.pieces_map[YROW][XROW].
    """
    def __init__ (self, pieces=9, move_cb=None):
        self.reset(pieces)
        self.move_cb = move_cb
        self.solved = True

    def reset (self, pieces=9):
        self.pieces, self.rowsize, self.colsize = calculate_matrix(pieces)
        pieces_map = range(1,self.pieces+1)
        self.pieces_map = []
        for i in range(self.rowsize):
            self.pieces_map.append(pieces_map[i*self.colsize:(i+1)*self.colsize])
        self.hole_pos = MatrixPosition(self.rowsize, self.colsize)
        self.hole_pos.bottom_right()
        self.solved_map = [list(x) for x in self.pieces_map]
        self.solved_map[-1][-1] = None

    def randomize (self):
        """ To make sure the randomization is solvable, we don't simply shuffle the numbers.
        We move the hole in random directions through a finite number of iteractions. """
        # Remove the move callback temporarily
        cb = self.move_cb
        self.move_cb = None

        iteractions = self.rowsize * self.colsize * (int(100*random())+1)

        t = time()
        for i in range(iteractions):
            while not (self.do_move(int(4*random())+1)):
                pass

        t = time() - t

        # Now move the hole to the bottom right
        for x in range(self.colsize-self.hole_pos.x-1):
            self.do_move(SLIDE_LEFT)
        for y in range(self.rowsize-self.hole_pos.y-1):
            self.do_move(SLIDE_UP)

        # Put the callback where it was
        self.move_cb = cb
        self.solved = False

    def do_move (self, slide_direction):
        """
        The moves are relative to the moving piece:
        
        >>> jm = SliderPuzzleMap()
        >>> jm.debug_map()
        1 2 3
        4 5 6
        7 8 *
        >>> jm.do_move(SLIDE_DOWN)
        True
        >>> jm.debug_map() # DOWN
        1 2 3
        4 5 *
        7 8 6
        >>> jm.do_move(SLIDE_RIGHT)
        True
        >>> jm.debug_map() # RIGHT
        1 2 3
        4 * 5
        7 8 6
        >>> jm.do_move(SLIDE_UP)
        True
        >>> jm.debug_map() # UP
        1 2 3
        4 8 5
        7 * 6
        >>> jm.do_move(SLIDE_LEFT)
        True
        >>> jm.debug_map() # LEFT
        1 2 3
        4 8 5
        7 6 *

        We can't move over the matrix edges:

        >>> jm.do_move(SLIDE_LEFT)
        False
        >>> jm.debug_map() # LEFT
        1 2 3
        4 8 5
        7 6 *
        >>> jm.do_move(SLIDE_UP)
        False
        >>> jm.debug_map() # UP
        1 2 3
        4 8 5
        7 6 *
        >>> jm.do_move(SLIDE_RIGHT)
        True
        >>> jm.do_move(SLIDE_RIGHT)
        True
        >>> jm.do_move(SLIDE_RIGHT)
        False
        >>> jm.debug_map() # RIGHT x 3
        1 2 3
        4 8 5
        * 7 6
        >>> jm.do_move(SLIDE_DOWN)
        True
        >>> jm.do_move(SLIDE_DOWN)
        True
        >>> jm.do_move(SLIDE_DOWN)
        False
        >>> jm.debug_map() # DOWN x 3
        * 2 3
        1 8 5
        4 7 6
       """
        # What piece are we going to move?
        old_hole_pos = self.hole_pos.clone()
        if self.hole_pos.move(slide_direction):
            # Move was a success, now update the map
            self.pieces_map[old_hole_pos.y][old_hole_pos.x] = self.pieces_map[self.hole_pos.y][self.hole_pos.x]
            self.is_solved()
            if self.move_cb is not None:
                self.move_cb(self.hole_pos.x, self.hole_pos.y, old_hole_pos.x, old_hole_pos.y)
            return True
        return False

    def do_move_piece (self, piece):
        """ Move the piece (1 based index) into the hole, if possible
        >>> jm = SliderPuzzleMap()
        >>> jm.debug_map()
        1 2 3
        4 5 6
        7 8 *
        >>> jm.do_move_piece(6)
        True
        >>> jm.debug_map() # Moved 6
        1 2 3
        4 5 *
        7 8 6
        >>> jm.do_move_piece(2)
        False
        >>> jm.debug_map() # No move
        1 2 3
        4 5 *
        7 8 6

        Return True if a move was done, False otherwise.
        """
        for y in range(self.rowsize):
            for x in range(self.colsize):
                if self.pieces_map[y][x] == piece:
                    if self.hole_pos.x == x:
                        if abs(self.hole_pos.y-y) == 1:
                            return self.do_move(self.hole_pos.y > y and SLIDE_DOWN or SLIDE_UP)
                    elif self.hole_pos.y == y:
                        if abs(self.hole_pos.x-x) == 1:
                            return self.do_move(self.hole_pos.x > x and SLIDE_RIGHT or SLIDE_LEFT)
                    else:
                        return False
        return False

    def is_hole_at (self, x, y):
        """
        >>> jm = SliderPuzzleMap()
        >>> jm.debug_map()
        1 2 3
        4 5 6
        7 8 *
        >>> jm.is_hole_at(2,2)
        True
        >>> jm.is_hole_at(0,0)
        False
        """
        return self.hole_pos == (x,y)

    def is_solved (self):
        """
        >>> jm = SliderPuzzleMap()
        >>> jm.do_move_piece(6)
        True
        >>> jm.is_solved()
        False
        >>> jm.do_move_piece(6)
        True
        >>> jm.is_solved()
        True
        """
        if self.hole_pos != (self.colsize-1, self.rowsize-1):
            return False
        self.pieces_map[self.hole_pos.y][self.hole_pos.x] = None
        self.solved = self.pieces_map == self.solved_map
        return self.solved
        
        

    def get_cell_at (self, x, y):
        if x < 0 or x >= self.colsize or y < 0 or y >= self.rowsize or self.is_hole_at(x,y):
            return None
        return self.pieces_map[y][x]

    def debug_map (self):
        for y in range(self.rowsize):
            for x in range(self.colsize):
                if self.hole_pos == (x,y):
                    logging.debug("*")
                else:
                    logging.debug(self.pieces_map[y][x])

    def __call__ (self):
        self.debug_map()



###
# Widget Definition
###

class SliderPuzzleWidget (gtk.Table):
    __gsignals__ = {'solved' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
                    'shuffled' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
                    'moved' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),}
    
    def __init__ (self, pieces=9, width=480, height=480):
        self.jumbler = SliderPuzzleMap(pieces, self.jumblermap_piece_move_cb)
        # We take this from the jumbler object because it may have altered our requested value
        gtk.Table.__init__(self, self.jumbler.rowsize, self.jumbler.colsize)
        self.image = None #gtk.Image()
        self.width = width
        self.height = height
        self.set_size_request(width, height)
        self.filename = None

    def prepare_pieces (self):
        """ set up a list of UI objects that will serve as pieces, ordered correctly """
        self.pieces = []
        if self.image is None:
        #    pb = self.image.get_pixbuf()
        #if self.image is None or pb is None:
            for i in range(self.jumbler.pieces):
                self.pieces.append(gtk.Button(str(i+1)))
                self.pieces[-1].connect("button-release-event", self.process_mouse_click, i+1)
                self.pieces[-1].show()
        else:
            if isinstance(self.image, SliderCreator):
                # ask for image creation
                self.image.prepare_stringed(self.jumbler.rowsize, self.jumbler.colsize)
        
            w = self.image.get_width() / self.jumbler.colsize
            h = self.image.get_height() / self.jumbler.rowsize
            for y in range(self.jumbler.rowsize):
                for x in range(self.jumbler.colsize):
                    img = gtk.Image()
                    img.set_from_pixbuf(self.image.subpixbuf(x*w, y*h, w-1, h-1))
                    img.show()
                    self.pieces.append(gtk.EventBox())
                    self.pieces[-1].add(img)
                    self.pieces[-1].connect("button-press-event", self.process_mouse_click, (y*self.jumbler.colsize)+x+1)
                    self.pieces[-1].show()
            self.set_row_spacings(1)
            self.set_col_spacings(1)

    @utils.trace
    def full_refresh (self):
        # Delete everything
        self.foreach(self.remove)
        self.prepare_pieces()
        # Add the pieces in their respective places
        for y in range(self.jumbler.rowsize):
            for x in range(self.jumbler.colsize):
                pos = self.jumbler.get_cell_at(x, y)
                if pos is not None:
                    self.attach(self.pieces[pos-1], x, x+1, y, y+1)

    def process_mouse_click (self, b, e, i):
        # i is the 1 based index of the piece
        self.jumbler.do_move_piece(i)

    def process_key (self, w, e):
        if self.get_parent() == None:
            return False
        k = gtk.gdk.keyval_name(e.keyval)
        if k in up_key:
            self.jumbler.do_move(SLIDE_UP)
            return True
        if k in down_key:
            self.jumbler.do_move(SLIDE_DOWN)
            return True
        if k in left_key:
            self.jumbler.do_move(SLIDE_LEFT)
            return True
        if k in right_key:
            self.jumbler.do_move(SLIDE_RIGHT)
            return True
        return False

    ### SliderPuzzleMap specific callbacks ###

    def jumblermap_piece_move_cb (self, hx, hy, px, py):
        if not hasattr(self, 'pieces'):
            return
        piece = self.pieces[self.jumbler.get_cell_at(px, py)-1]
        self.remove(piece)
        self.attach(piece, px, px+1, py, py+1)
        self.emit("moved")
        if self.jumbler.solved:
            self.emit("solved")

    ### Parent callable interface ###

    def get_nr_pieces (self):
        return self.jumbler.pieces

    @utils.trace
    def set_nr_pieces (self, nr_pieces):
        self.jumbler.reset(nr_pieces)
        self.resize(self.jumbler.rowsize, self.jumbler.colsize)
        self.randomize()

    @utils.trace
    def randomize (self):
        """ Jumble the SliderPuzzle """
        self.jumbler.randomize()
        self.full_refresh()
        self.emit("shuffled")

    @utils.trace
    def load_image (self, image, width=0, height=0):
        """ Loads an image from the file.
        width and height are processed as follows:
          -1 : follow the loaded image size
           0 : follow the size set on widget instantiation
           * : use that specific size"""
        if width == 0:
            width = self.width
        if height == 0:
            height = self.height
        if not isinstance(image, SliderCreator):
            self.image = utils.resize_image(image, width, height)
        else:
            self.image = image
        self.filename = True
        self.full_refresh()

    def set_image (self, image):
        # image is a pixbuf!
        self.image = image
        self.filename = True

    def set_image_from_str (self, image):
        fn = os.tempnam() 
        f = file(fn, 'w+b')
        f.write(image)
        f.close()
        i = gtk.Image()
        i.set_from_file(fn)
        os.remove(fn)
        self.image = i.get_pixbuf()
        self.filename = True

    def show_image (self):
        """ Shows the full image, used as visual clue for solved puzzle """
        # Delete everything
        self.foreach(self.remove)
        if hasattr(self, 'pieces'):
            del self.pieces
        # Resize to a single cell and use that for the image
        self.resize(1,1)
        img = gtk.Image()
        img.set_from_pixbuf(self.image)
        self.attach(img, 0,1,0,1)
        img.show()

    def get_image_as_png (self, cb=None):
        if self.image is None:
            return None
        rv = None
        if cb is None:
            rv = StringIO()
            cb = rv.write
        self.image.save_to_callback(cb, "png")
        if rv is not None:
            return rv.getvalue()
        else:
            return True
            
RESIZE_STRETCH = 1
RESIZE_CUT = 2
RESIZE_PAD = 3

class ImageSelectorWidget (gtk.Table):
    __gsignals__ = {'category_press' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
                    'image_press' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),}

    def __init__ (self,
                  width=IMAGE_SIZE,
                  height=IMAGE_SIZE,
                  frame_color=None,
                  prepare_btn_cb=prepare_btn,
                  method=RESIZE_CUT,
                  image_dir=None):
        gtk.Table.__init__(self, 2,5,False)
        self._signals = []
        self.width = width
        self.height = height
        self.image = gtk.Image()
        self.method = method
        #self.set_myownpath(MYOWNPIC_FOLDER)
        img_box = BorderFrame(border_color=frame_color)
        img_box.add(self.image)
        img_box.set_border_width(5)
        self._signals.append((img_box, img_box.connect('button_press_event', self.emit_image_pressed)))
        self.attach(img_box, 0,5,0,1,0,0)
        self.attach(gtk.Label(), 0,1,1,2)
        self.bl = gtk.Button()

        il = gtk.Image()
        il.set_from_pixbuf(load_image(os.path.join(iconpath, 'arrow_left.png')))
        self.bl.set_image(il)

        self.bl.connect('clicked', self.previous)
        self.attach(prepare_btn_cb(self.bl), 1,2,1,2,0,0)

        cteb = gtk.EventBox()
        self.cat_thumb = gtk.Image()
        self.cat_thumb.set_size_request(THUMB_SIZE, THUMB_SIZE)
        cteb.add(self.cat_thumb)
        self._signals.append((cteb, cteb.connect('button_press_event', self.emit_cat_pressed)))
        self.attach(cteb, 2,3,1,2,0,0,xpadding=10)
        
        self.br = gtk.Button()
        ir = gtk.Image()
        ir.set_from_pixbuf(load_image(os.path.join(iconpath,'arrow_right.png')))
        self.br.set_image(ir)
        self.br.connect('clicked', self.next)
        self.attach(prepare_btn_cb(self.br), 3,4,1,2,0,0)
        self.attach(gtk.Label(),4,5,1,2)
        self.filename = None
        self.show_all()
        self.image.set_size_request(width, height)
        if image_dir is None:
            image_dir = os.path.join(mmmpath, "mmm_images")
        self.set_image_dir(image_dir)

    def add_image (self, *args):#widget=None, response=None, *args):
        """ Use to trigger and process the My Own Image selector. """

        if hasattr(mime, 'GENERIC_TYPE_IMAGE'):
            filter = { 'what_filter': mime.GENERIC_TYPE_IMAGE }
        else:
            filter = { }

        chooser = ObjectChooser(_('Choose image'), None, #self._parent,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                **filter)
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                jobject = chooser.get_selected_object()
                if jobject and jobject.file_path:
                    if self.load_image(str(jobject.file_path), True):
                        pass
                    else:
                        err = gtk.MessageDialog(self._parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                                _("Not a valid image file"))
                        err.run()
                        err.destroy()
                        return
        finally:
            chooser.destroy()
            del chooser

    def set_readonly (self, ro=True):
        if ro:
            self.bl.hide()
            self.br.hide()
            for w, s in self._signals:
                w.handler_block(s)

    def emit_cat_pressed (self, *args):
        self.emit('category_press')
        return True

    def emit_image_pressed (self, *args):
        self.emit('image_press')
        return True

    def has_image (self):
        return self.category.has_image()

    def get_category_name (self):
        return self.category.name

    def get_filename (self):
        return self.category.filename

    def get_image (self):
        return self.category.pb

    def next (self, *args, **kwargs):
        pb = self.category.get_next_image()
        if pb is not None:
            self.image.set_from_pixbuf(pb)

    def previous (self, *args, **kwargs):
        pb = self.category.get_previous_image()
        if pb is not None:
            self.image.set_from_pixbuf(pb)

    def get_image_dir (self):
        return self.category.path

    def set_image_dir (self, directory):
        if os.path.exists(directory) and not os.path.isdir(directory):
            filename = directory
            directory = os.path.dirname(directory)
            logging.debug("dir=%s, filename=%s" % (directory, filename))
        else:
            logging.debug("dir=%s" % (directory))
            filename = None
        self.category = CategoryDirectory(directory, self.width, self.height, self.method)
        self.cat_thumb.set_from_pixbuf(self.category.thumb)
        if filename:
            self.image.set_from_pixbuf(self.category.get_image(filename))
        else:
            if self.category.has_images():
                self.next()

    def load_image(self, filename, fromJournal=False):
        """ Loads an image from the file """
        self.category = CategoryDirectory(filename, self.width, self.height, method=self.method)
        self.next()
        self.cat_thumb.set_from_pixbuf(self.category.thumb)
        return self.image.get_pixbuf() is not None

    def load_pb (self, pb):
        self.category.pb = pb
        self.image.set_from_pixbuf(resize_image(pb, self.width, self.height, method=self.method))
            
GAME_SIZE = 450
class Puzzle:
    def __init__ (self, parent, image):
        self._parent = parent
        
        self.game = SliderPuzzleWidget(pieces, GAME_SIZE, GAME_SIZE)
        self.game.connect("solved", self.do_solve)
        self.game.connect("moved", self.slider_move_cb)
        self._parent.connect("key_press_event",self.game.process_key)
        self._parent.connect("key_press_event",self.process_key)
        self.game.show()
        self.game_wrapper = gtk.VBox()
        self.game_wrapper.show()
        
        #buttons (pieces of the larger image)
        btn_box = gtk.Table(1,5,False)
        btn_box.set_col_spacings(5)
        btn_box.set_row_spacings(5)
        btn_box.attach(gtk.Label(), 0,1,0,2)

        self.btn_9 = prepare_btn(gtk.ToggleButton("9"),50)
        self.btn_9.set_active(True)
        self.btn_9.connect("clicked", self.set_nr_pieces, 9)
        btn_box.attach(self.btn_9, 1,2,0,1,0,0)
        btn_box.attach(gtk.Label(), 4,5,0,1)

        self.thumb = ImageSelectorWidget(frame_color=COLOR_FRAME_THUMB, prepare_btn_cb=prepare_btn, image_dir='images')
        self.thumb.connect("category_press", self.do_select_category)
        self.thumb.connect("image_press", self.set_nr_pieces)
        control_panel_box.pack_start(self.thumb, False)
