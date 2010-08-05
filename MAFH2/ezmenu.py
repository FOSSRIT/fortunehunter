#! /usr/bin/env python

#############################################################
#EzMeNu - A simple module to quickly make menus with PyGame #
#############################################################
#Licensed under the GNU Lesser General Public License       #
#Created by PyMike <pymike93@gmail.com>                     #
#Some edits by Justin Lewis <jtl1728@rit.edu>               #
#Some edits by Kevin Hockey <kdh7733@rit.edu>               #
#############################################################

import pygame
from fortuneengine.DrawableFontObject import DrawableFontObject

class EzMenu():

    def __init__(self, options, scene):
        """Initialise the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""
        self.scene = scene
        self.options = options
        self.x = 0
        self.y = 0
        self.hx = 0
        self.hy = 0
        self.centerx = 0
        self.centery = 0
        self.font = pygame.font.Font(None, 18)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options)*self.font.get_height()
        self.font.set_italic( True )
        self.help_text = DrawableFontObject("", self.font)
        self.font.set_italic( False )
        self.font_list = []
        self.scene.addObject(self.help_text)

        for o in self.options:
            ren = self.font.render( o[0], 1, self.color)
            self.font_list.append(DrawableFontObject(o[0], self.font))
            if self.width < ren.get_width():
                self.width = ren.get_width()
                
        self.scene.addObjects(self.font_list)

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0
        help_txt = ""
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
                help_txt = o[2]
            else:
                clr = self.color
            text = o[0]
            #ren = self.font.render(text, True, clr)
            self.font_list[i].changeText(text, clr)
            self.font_list[i].setPosition( self.x, self.y + i*self.font.get_height() )
            #surface.blit(ren, (self.x, self.y + i*self.font.get_height()))
            i+=1

        # Help Text
        self.help_text.changeText(help_txt, self.color)
        self.help_text.setPosition(self.hx+5, self.hy)

    def update(self, event):
        """Update the menu and get input for the menu."""
        return_val = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.option += 1
                return_val = True
            elif event.key == pygame.K_UP:
                self.option -= 1
                return_val = True
            elif event.key == pygame.K_RETURN:
                self.options[self.option][1]()
                return_val = True

        if self.option > len(self.options)-1:
            self.option = 0
        elif self.option < 0:
            self.option = len(self.options)-1

        return return_val

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y

    def set_font(self, font):
        """Set the font used for the menu."""
        self.font = font

    def set_highlight_color(self, color):
        """Set the highlight color"""
        self.hcolor = color

    def set_normal_color(self, color):
        """Set the normal color"""
        self.color = color

    def center_at(self, x, y):
        """Center the center of the menu at x,y"""
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
        self.centerx = x
        self.centery = y

    def help_text_at(self, x, y):
        self.hx = x
        self.hy = y
        
    def clear_menu(self):
        for dfo in self.font_list:
            self.scene.removeObject(dfo)
        self.scene.removeObject(self.help_text)
