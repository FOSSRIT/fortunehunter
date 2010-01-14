# Copyright 2007 World Wide Workshop Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# If you find this activity useful or end up using parts of it in one of your
# own creations we would love to hear from you at info@WorldWideWorkshop.org !
#

import pygtk
pygtk.require('2.0')
import gtk
import logging

RESIZE_STRETCH = 1
RESIZE_CUT = 2
RESIZE_PAD = 3

TYPE_REG = []

def register_image_type (handler):
    TYPE_REG.append(handler)

def calculate_relative_size (orig_width, orig_height, width, height):
    """ If any of width or height is -1, the returned width or height will be in the same relative scale as the
    given part.
    >>> calculate_relative_size(100, 100, 50, -1)
    (50, 50)
    >>> calculate_relative_size(200, 100, -1, 50)
    (100, 50)

    If both width and height are given, the same values will be returned. If none is given, the orig_* will be returned.
    >>> calculate_relative_size(200,200,100,150)
    (100, 150)
    >>> calculate_relative_size(200,200,-1,-1)
    (200, 200)
    """
    if width < 0:
        if height >= 0:
            out_w = int(orig_width * (float(height)/orig_height))
            out_h = height
        else:
            out_w = orig_width
            out_h = orig_height
    else:
        out_w = width
        if height < 0:
            out_h = int(orig_height * (float(width)/orig_width))
        else:
            out_h = height
    return out_w, out_h

def load_image (filename, width=-1, height=-1, method=RESIZE_CUT):
    """ load an image from filename, returning it's gtk.gdk.PixBuf().
    If any or all of width and height are given, scale the loaded image to fit the given size(s).
    If both width and height and requested scaling can be achieved in two flavours, as defined by
    the method argument:
      RESIZE_CUT : resize so one of width or height fits the requirement and the other fits or overflows,
                   cut the center of the image to fit the request.
      RESIZE_STRETCH : fit the requested sizes exactly, by scaling with stretching sides if needed.
      RESIZE_PAD : resize so one of width or height fits the requirement and the other underflows.

    Example: Image with 500x500, requested 200x100
      - RESIZE_CUT: scale to 200x200, cut 50 off each top and bottom to fit 200x100
      - RESIZE STRETCH : scale to 200x100, by changing the image WxH ratio from 1:1 to 2:1, thus distorting it.
      - RESIZE_PAD: scale to 100x100, add 50 pixel padding for top and bottom to fit 200x100
    """
    for ht in TYPE_REG:
        if ht.can_handle(filename):
            return ht(width, height, filename)
#    if filename.lower().endswith('.sequence'):
#        slider = None
#        cmds = file(filename).readlines()
#        if len(cmds) > 1:
#            _x_ = eval(cmds[0])
#            items = []
#            for i in range(16):
#                items.append(_x_)
#                _x_ = eval(cmds[1])
#            slider = SliderCreator(width, height, items)
#            slider.prepare_stringed(2,2)
#        return slider
#
    img = gtk.Image()
    try:
        img.set_from_file(filename)
        pb = img.get_pixbuf()
    except:
        return None
    return resize_image(pb, width, height, method)

def resize_image (pb, width=-1, height=-1, method=RESIZE_CUT):
    if pb is None:
        return None
    logging.debug("utils: method=%i" % method)
    if method == RESIZE_STRETCH or width == -1 or height == -1:
        w,h = calculate_relative_size(pb.get_width(), pb.get_height(), width, height)
        scaled_pb = pb.scale_simple(w,h, gtk.gdk.INTERP_BILINEAR)
    elif method == RESIZE_PAD:
        w,h = pb.get_width(), pb.get_height()
        hr = float(height)/h
        wr = float(width)/w
        factor = min(hr, wr)
        w = w * factor
        h = h * factor
        logging.debug("RESIZE_PAD: %i,%i,%f" % (w,h,factor))
        scaled_pb = pb.scale_simple(int(w), int(h), gtk.gdk.INTERP_BILINEAR)
    else: # RESIZE_CUT / default
        w,h = pb.get_width(), pb.get_height()
        if width > w:
            if height > h:
                #calc which side needs more scaling up as both are smaller
                hr = float(height)/h
                wr = float(width)/w
                if hr < wr:
                    w = width
                    h = -1
                else:
                    h = height
                    w = -1
            else:
                # requested height smaller than image, scale width up and cut on height
                h = -1
                w = width
        else:
            if height > h:
                #requested width smaller than image, scale height up and cut on width
                h = height
                w = -1
            else:
                # calc which side needs less scaling down as both are bigger
                hr = float(height)/h
                wr = float(width)/w
                if hr < wr:
                    w = width
                    h = -1
                else:
                    h = height
                    w = -1
        # w, h now have -1 for the side that should be relatively scaled, to keep the aspect ratio and
        # assuring that the image is at least as big as the request.
        w,h = calculate_relative_size(pb.get_width(), pb.get_height(), w,h)
        scaled_pb = pb.scale_simple(w,h, gtk.gdk.INTERP_BILINEAR)
        # now we cut whatever is left to make the requested size
        scaled_pb = scaled_pb.subpixbuf(abs((width-w)/2),abs((height-h)/2), width, height)
    return scaled_pb

### Helper decorators

def trace (func):
    def wrapped (*args, **kwargs):
        logging.debug("TRACE %s %s %s" % (func.func_name, args, kwargs))
        return func(*args, **kwargs)
    return wrapped

