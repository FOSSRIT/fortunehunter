import pygame
import random
from fortuneengine.GameEngineElement import GameEngineElement
from fortuneengine.DrawableObject import DrawableObject
from fortuneengine.DynamicDrawableObject import DynamicDrawableObject
from AnimatedSprite import Spritesheet

from constants import MENU_PATH, PUZZLE_PATH
from gettext import gettext as _


class MagicMenuHolder( GameEngineElement ):
    def __init__(self, callback):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        self.background = DrawableObject([pygame.image.load( MENU_PATH + "battleMenubackground.gif")], '')
        self.background.setPosition(0,286)
        self.game_engine.get_scene().addObject(self.background)

    def remove_from_engine(self):
        self.game_engine.get_scene().removeObject(self.background)
        super( MagicMenuHolder, self ).remove_from_engine()
        self.clear_menu()
        
    def draw(self,screen,time_delta):
        pass

    def menu_called(self, id):
        self.callback(id, self)

    def clear_menu(self):
        if self.menu:
            self.menu.clear()
            self.menu.remove_from_engine()
            self.menu = None
            
    def show_menu(self,id):
        if self.is_in_engine():
            self.clear_menu()
        else:
            self.add_to_engine()
         
        if id == "fire":
            spell_type = 0
            menu_options = [
                        [_('1'), lambda: self.menu_called("fire1"), 140],
                        [_('2'), lambda: self.menu_called("fire2"), 140],
                        [_('3'), lambda: self.menu_called("fire3"), 140],
                        [_('4'), lambda: self.menu_called("fire4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        elif id == "lightning":
            spell_type = 1
            menu_options = [
                        [_('1'), lambda: self.menu_called("lig1"), 140],
                        [_('2'), lambda: self.menu_called("lig2"), 140],
                        [_('3'), lambda: self.menu_called("lig3"), 140],
                        [_('4'), lambda: self.menu_called("lig4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        elif id == "missile":
            spell_type = 2
            menu_options = [
                        [_('1'), lambda: self.menu_called("miss1"), 140],
                        [_('2'), lambda: self.menu_called("miss2"), 140],
                        [_('3'), lambda: self.menu_called("miss3"), 140],
                        [_('4'), lambda: self.menu_called("miss4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        elif id == "heal":
            spell_type = 3
            menu_options = [
                        [_('1'), lambda: self.menu_called("heal1"), 140],
                        [_('2'), lambda: self.menu_called("heal2"), 140],
                        [_('3'), lambda: self.menu_called("heal3"), 140],
                        [_('4'), lambda: self.menu_called("heal4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        self.menu = MagicMenu(menu_options, 237, 375, spell_type)

class MagicMenu(GameEngineElement):
    def __init__(self, menu_options, x, y, spell_type):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        magic_list = self.game_engine.get_object('battle').magic_list
        self.menu = Menu(menu_options, spell_type, magic_list, self.game_engine.get_scene())
        self.menu.set_pos(x, y)
        self.add_to_engine()

    def event_handler(self, event):
        return self.menu.update(event)

    def draw(self,screen,time_delta):
        self.menu.draw( screen )
    
    def clear(self):
        self.menu.clear()

class Menu(object):
    def __init__(self, options, spelltype, magic_list, scene):
        """Initialize the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""
        
        self.scene = scene
        self.buttons = []
        self.options = options
        self.x = 0
        self.y = 0
        self.cols = 2
        self.option = 0
        self.width = 2
        self.spelltype = spelltype
        self.magic_list = magic_list
        self.reference = []
        
        lightning = []
        fire = []
        missile = []
        heal = []
        

        fire = Spritesheet(PUZZLE_PATH + "FireGlyph.gif").img_extract(2,2,150,150,(255,0,255))
        lightning = Spritesheet(PUZZLE_PATH + "LightningGlyph.gif").img_extract(2,2,150,150,(255,0,255))
        missile = Spritesheet(PUZZLE_PATH + "MissileGlyph.gif").img_extract(2,2,150,150,(255,0,255))
        heal = Spritesheet(PUZZLE_PATH + "HealGlyph.gif").img_extract(2,2,150,150,(255,0,255))

        if(spelltype == 0):
            #fire attack
            for i in range(4):
                self.buttons.append(DrawableObject([pygame.transform.scale(fire[i] , (60,60))], ""))
            #filler buttons
            for i in range(0,2):
                self.buttons.append(DrawableObject([pygame.transform.scale(lightning[i] , (60,60))], ""))
            random.seed()
            self.buttons.append(DrawableObject([pygame.transform.scale(heal[random.randint(0,3)] , (60,60))], ""))
            self.buttons.append(DrawableObject([pygame.transform.scale(missile[random.randint(0,3)] , (60,60))], ""))
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "FireGlyph.gif").convert_alpha()
            self.glyphs = fire
            
        elif(spelltype == 1):
            #lightning attack
            for i in range(4):
                self.buttons.append(DrawableObject([pygame.transform.scale(lightning[i] , (60,60))], ""))
            #filler buttons
            for i in range(0,2):
                self.buttons.append(DrawableObject([pygame.transform.scale(fire[i] , (60,60))], ""))
            random.seed()
            self.buttons.append(DrawableObject([pygame.transform.scale(heal[random.randint(0,3)] , (60,60))], ""))
            self.buttons.append(DrawableObject([pygame.transform.scale(missile[random.randint(0,3)] , (60,60))], ""))
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "LightningGlyph.gif").convert_alpha()
            self.glyphs = lightning
            
        elif(spelltype == 2):
            #missile attack
            for i in range(4):
                self.buttons.append(DrawableObject([pygame.transform.scale(missile[i] , (60,60))], ""))
            #filler buttons
            for i in range(0,2):
                self.buttons.append(DrawableObject([pygame.transform.scale(lightning[i] , (60,60))], ""))
            random.seed()
            self.buttons.append(DrawableObject([pygame.transform.scale(heal[random.randint(0,3)] , (60,60))], ""))
            self.buttons.append(DrawableObject([pygame.transform.scale(fire[random.randint(0,3)] , (60,60))], ""))
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "MissileGlyph.gif").convert_alpha()
            self.glyphs = missile
        elif(spelltype == 3):
            #heal
            for i in range(4):
                self.buttons.append(DrawableObject([pygame.transform.scale(heal[i] , (60,60))], ""))
            #filler buttons
            for i in range(0,2):
                self.buttons.append(DrawableObject([pygame.transform.scale(lightning[i] , (60,60))], ""))
            random.seed()
            self.buttons.append(DrawableObject([pygame.transform.scale(missile[random.randint(0,3)] , (60,60))], ""))
            self.buttons.append(DrawableObject([pygame.transform.scale(fire[random.randint(0,3)] , (60,60))], ""))
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "HealGlyph.gif").convert_alpha()
            self.glyphs = heal
        
        deck = [0,1,2,3,4,5,6,7]
        random.seed()
        random.shuffle(deck)
        tOptions = []
        tButtons = []
        for i in range(8):
            tOptions.append(self.options[deck[i]])
            tButtons.append(self.buttons[deck[i]])
            
        self.buttons = tButtons
        self.options = tOptions
        
        surf = pygame.Surface((60,60))
        surf.fill((4, 119, 152))
        self.selectRect = DynamicDrawableObject([surf],"")
        self.selectRect.setPosition(297, 435)
        self.scene.addObject(self.selectRect)
        self.scene.addObjects(self.buttons)
        
        self.mainGlyph.set_colorkey((255,0,255), pygame.RLEACCEL)
        self.mainGlyphDO = DrawableObject([self.mainGlyph],"")
        self.mainGlyphDO.setPosition(485,350)
        
        for image in self.glyphs:
            tempDO = DrawableObject([image],"",True)
            #tempDO.makeTransparent(True)
            self.reference.append(tempDO)
        self.scene.addObjects(self.reference)
        self.scene.addObject(self.mainGlyphDO)
        
        self.height = (len(self.options)*self.buttons[1].getYSize()) / self.cols

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0 # Row Spacing
        h=0 # Selection Spacing
        j=0 # Col Spacing
        index=0 #current spot in buttons list
        height = 60
        width = 60
        
        for o in self.options:

            newX = self.x + width * j
            newY = self.y + i * height
            
            if h==self.option:
                self.selectRect.setPosition(newX, newY)
            self.buttons[index].setPosition(newX, newY)
            #surface.blit(self.buttons[index], (newX, newY) )

            j+=1
            h+=1
            index+=1
            if j >= self.cols:
                i+=1
                j=0
                
        # Draw reference glyphs
        for i in range(4):
            if i in self.magic_list:
                #surface.blit(self.glyphs[i], (800+((i%2) * 150), 350+(i/2 * 150)))
                self.reference[i].makeTransparent(False)
                self.reference[i].setPosition(800+((i%2) * 150), 350+(i/2 * 150))
                
    def update(self, event):
        """Update the menu and get input for the menu."""
        return_val = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.cols != 1:
                    self.option += self.cols
                else:
                    self.option += 1
                return_val = True
            elif event.key == pygame.K_UP:
                if self.cols != 1:
                    self.option -= self.cols
                else:
                    self.option -= 1
                return_val = True
            elif event.key == pygame.K_RIGHT:
                if self.cols != 1:
                    self.option += 1
                    return_val = True
            elif event.key == pygame.K_LEFT:
                if self.cols != 1:
                    self.option -= 1
                    return_val = True
            elif event.key == pygame.K_RETURN:
                self.options[self.option][1]()
                return_val = True

            self.option = self.option % len(self.options)

        return return_val

    def clear(self):
        for object in self.buttons:
            self.scene.removeObject(object)
        for object in self.reference:
            self.scene.removeObject(object)
        self.scene.removeObject(self.mainGlyphDO)
        self.scene.removeObject(self.selectRect)

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
