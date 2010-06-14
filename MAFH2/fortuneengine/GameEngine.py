#    FortuneEngine is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    FortuneEngine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with the FortuneEngine.  If not, see <http://www.gnu.org/licenses/>.
#
#    Author: Justin Lewis  <jlew.blackout@gmail.com>

import pygame
import fortuneengine.pyconsole.pyconsole as pyconsole

class GameEngine(object):
    instance = None
    def __init__(self, width=1200, height=900):
        GameEngine.instance = self
        pygame.init()
        pygame.mouse.set_visible(False)

        self.width = width
        self.height = height
        size = width, height

        self.screen = pygame.display.set_mode(size)

        self.__event_cb = []
        self.__draw_lst = []
        self.__object_hold = {}

        self.__active_event_timers = {}

        self.clock = pygame.time.Clock()

        # functions exposed to the console
        function_list = {
            "ge_stop":self.stop_event_loop,

            "ge_list_objects":self.list_objects,
            "ge_list_drawcb":self.list_draw_callbacks,
            "ge_list_eventcb":self.list_event_callbacks,
            "ge_list_timers":self.list_event_timers,
            "inspect":self.inspect_object,
        }

        # Ctrl + key mappings
        key_calls = {
            "d":self.stop_event_loop,
            "m":self.console_mode,
        }

        # Initialize Py Console
        self.console = pyconsole.Console(
            self.screen, (0,0,width,height/2),
            functions=function_list, key_calls=key_calls,
            vars={}, syntax={}
        )
    def console_mode(self):
        """
        Switches console between console and python interpreter
        """
        # Deactivate Console if showing
        if self.console.active:
            self.console.set_active()
        self.console.setvar("python_mode", not self.console.getvar("python_mode"))
        self.console.set_interpreter()
        self.console.set_active()

    def start_event_timer(self, id, time):
        """
        Starts a timer that fires a user event into the queue every "time" 
        milliseconds
        """
        pygame.time.set_timer(pygame.USEREVENT + id, time)
        self.__active_event_timers[id] = time

    def stop_event_timer(self, id):
        """
        Stops the timer that has id from firing
        """
        pygame.time.set_timer(pygame.USEREVENT + id, 0)
        self.__active_event_timers[id] = 0

    def list_event_timers(self):
        """
        returns a list of configured timers, if the timers has a time of 0 the 
        timer is disabled
        """
        timer_list = "Event Timers:\n"
        for timer_key in self.__active_event_timers.keys():
            timer_list += "\t%d: %d\n" % (timer_key, self.__active_event_timers[timer_key])
        return timer_list

    def start_event_loop(self):
        """
        Starts the pygame event loop.
        """
        self.__run = True
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        while self.__run:
            self.clock.tick(15)
            update_draw = False
            console_active = self.console.active

            self.console.process_input()

            # Force to re-draw if removing console
            # This is necessary as queue will be empty at this time
            # and not update
            if console_active and not self.console.active:
                self.draw()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.__run = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_w \
                     and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.console.set_active()
                        update_draw = True

                else:
                    # Send event to all event listeners
                    # Make a copy first so that adding events don't get fired right away
                    list_cp = self.__event_cb[:]

                    # Reverse list so that newest stuff is on top
                    list_cp.reverse()

                    for cb in list_cp:
                        # Fire the event for all in cb and stop if return True
                        if cb(event) == True:
                            update_draw = True
                            break

            # If console is active, we want to draw console, pausing
            # game drawing (events are still being fired, just no
            # draw updates.
            if console_active:
                self.console.draw()
                pygame.display.flip()
            elif update_draw:
                self.draw()

    def stop_event_loop(self):
        """
        Sends a pygame.QUIT event into the event queue which exits the event loop
        """
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self):
        """
        Calls draw on the draw callback stack then calls the pygame flip command
        """
        for fnc in self.__draw_lst:
            fnc(self.screen)

        self.console.draw()
        pygame.display.flip()

    def add_event_callback(self, cb):
        """
        Adds event callback to the event callback stack

        @param cb:       Callback to be added to the stack when events are fired
        """
        self.__event_cb.append( cb )

    def remove_event_callback(self, cb):
        """
        Removes an event from the event callback stack

        @param cb:       The callback to remove from the event callback stack
        @return:         Returns true if successful in removing callback
        """
        try:
            self.__event_cb.remove( cb )
            return True
        except:
            return False

    def list_event_callbacks( self ):
        """
        Returns a string representation of all events registered with the game
        engine
        """
        event_callbacks = "Event Listeners:\n"
        for eventlst in self.__event_cb:
            event_callbacks = "\t%s\n"%str(eventlst)
        return event_callbacks


    def add_draw_callback(self, fnc):
        """
        Adds a callback to the draw list.  Function will be passed the game screen

        @param	fnc:	The function to call when system is drawing
        """
        self.__draw_lst.append( fnc )

    def pop_draw_callback(self):
        """
        Removes top of draw stack and returns it

        @return:         Returns the top callback function that was removed
        """
        return self.__draw_lst.pop()

    def clear_draw_callback(self):
        """
        Empties draw callback stack
        """
        self.__draw_lst = []

    def remove_draw_callback(self, fnc):
        """
        Removes a draw callback from the game engine draw function

        @param fnc:      The callback function to remove
        @return:         Returns true if successful removal of the function
        """
        try:
            self.__draw_lst.remove(fnc)
            return True
        except:
            return False

    def list_draw_callbacks(self):
        """
        Lists all the drawing callbacks currently registered with the game engine
        """

        callbacks = "Draw Callbacks:\n"
        for eventlst in self.__draw_lst:
            callbacks += "\t%s\n" % str(eventlst)
        return callbacks

    def has_object(self, name):
        """
        Returns true if object is stored in game engine

        @param name:     Name of the object to check if exists
        @return:         Returns true if object found
        """
        return self.__object_hold.has_key( name )

    def add_object(self, name, obj):
        """
        Adds an object to the game engine datastore

        @param name:     The name used to store the object
        @param obj:      The object to store
        """
        self.__object_hold[name] = obj

    def get_object(self, name):
        """
        Returns an object from the game engine datastore

        @param name:     The name of object to return
        @return:         Returns the object
        """
        return self.__object_hold[name]

    def remove_object(self, name):
        """
        Removes an object from the game engine datastore

        @param name:     The name of the object to remove
        """
        del self.__object_hold[name]

    def list_objects(self):
        """
        Returns a sting of registered objects
        """
        objlist = "Objects Registered:\n"
        for eventlst in self.__object_hold:
            objlist += "\t%s\n" % str(eventlst)
        return objlist

    def inspect_object(self, objectname):
        object_tokens = objectname.split(".")

        try:
            obj = self.__object_hold[ object_tokens[0] ]
        except KeyError:
            return "Error, %s is not an object registered with the game engine" % object_tokens[0]

        # Handles dot notation for sub modules
        for token in object_tokens[1:]:

            dict_token = token.split('[')
            obj = getattr( obj, dict_token[0] )

            # Handles dictionaries
            for d_token in dict_token[1:]:
                if d_token[-1] == "]":
                    if hasattr(obj, "has_key") and obj.has_key( d_token[:-1] ):
                        obj.get( d_token[:-1] )
                    else:
                        return "Not a dictionary object"

                else:
                    return "Invalid Syntax, expected ] at end of %d" % d_token

        classname = obj.__class__.__name__

        if hasattr( obj, "__dict__" ):
            attribute_list = "Attributes:"
            attributes = obj.__dict__
   
            for attribute_key in attributes.keys():
                attribute_list = "%s\n\t%s:%s" % (attribute_list,attribute_key,str(attributes[attribute_key]))

        # If dictionary, show keys
        elif hasattr( obj, "keys" ):
            attribute_list = "Dictionary Items:"

            for d_obj in obj.keys():
                attribute_list = "%s\n\t%s:%s" % (attribute_list,d_obj,str(obj[d_obj]))
                
        elif type( obj ).__name__ == 'list':
            i = 0
            attribute_list = "List Items:"
            for item in obj:
                attribute_list = "%s\n\t%d:%s" % (attribute_list,i,str(item))
        else:
            attribute_list = str( obj )

        return "Class: %s\n%s"   % (classname, attribute_list)

