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
import inspect
from GameEngineConsole import GameEngineConsole


class GameEngine(object):
    """
    The Fortune Engine GameEngine is a main loop wrapper around pygame.
    It manages the event and drawing loops allowing the user to just
    register for user events and drawing time in the draw loop.
    """
    instance = None

    def __init__(self, width=1200, height=900):
        GameEngine.instance = self
        pygame.init()
        pygame.mouse.set_visible(False)

        self.width = width
        self.height = height
        size = width, height

        self.screen = pygame.display.set_mode(size)

        self.__showfps = False
        self.__dirty = True
        self.__always_draw = True
        self.__font = pygame.font.Font(None, 17)

        self.__run_event = False
        self.__event_cb = []
        self.__draw_lst = []
        self.__object_hold = {}

        self.__active_event_timers = []
        self.__active_event_timers_tick = []

        self.clock = pygame.time.Clock()

        # Initialize Py Console
        self.console = GameEngineConsole(self, (0, 0, width, height / 2))

        # Disable Mouse Usage
        # TODO Allow mouse motion on request
        pygame.event.set_blocked(pygame.MOUSEMOTION)

    def start_event_timer(self, function_cb, time):
        """
        Starts a timer that fires a user event into the queue every "time"
        milliseconds
        """
        avail_timer = len(self.__active_event_timers)

        if avail_timer + pygame.USEREVENT < pygame.NUMEVENTS:
            if function_cb not in self.__active_event_timers:
                self.__active_event_timers.append(function_cb)
                self.__active_event_timers_tick.append(time)
                pygame.time.set_timer(pygame.USEREVENT + avail_timer, time)
            else:
                print "ERROR TIMER IN LIST"
        else:
            print "Ran out of timers :("
            self.stop_event_loop()

    def stop_event_timer(self, function_cb):
        """
        Stops the timer that has id from firing
        """
        try:
            timer_id = self.__active_event_timers.index(function_cb)
        except ValueError:
            return

        pygame.time.set_timer(pygame.USEREVENT + timer_id, 0)
        del self.__active_event_timers[timer_id]
        del self.__active_event_timers_tick[timer_id]

        # Timers have been removed, now need to clear any events
        # already fired and in the queue
        pygame.event.clear(pygame.USEREVENT + timer_id)

    def list_event_timers(self):
        """
        returns a list of configured timers, if the timers has a time of 0 the
        timer is disabled
        """
        timer_list = "Event Timers:\n"
        i = 0
        for timer_item in self.__active_event_timers:
            timer_list += "\t%d: %d\n" % (timer_item,
                          self.__active_event_timers_tick[i])
            i = i + 1

        return timer_list

    def start_main_loop(self):
        self.__run_event = True
        self._event_loop()

    def _draw(self):
        tick_time = self.clock.tick(15)
        screen = self.screen

        # If console is active, we want to draw console, pausing
        # game drawing (events are still being fired, just no
        # draw updates.
        if self.console.active:
            self.console.draw()
            pygame.display.flip()

        else:
            for fnc in self.__draw_lst:
                fnc(screen, tick_time)

            # Print Frame Rate
            if self.__showfps:
                text = self.__font.render('FPS: %d' % self.clock.get_fps(),
                       False, (255, 255, 255), (159, 182, 205))
                screen.blit(text, (0, 0))

            pygame.display.flip()

    def _event_loop(self):
        while self.__run_event:

            event = pygame.event.poll()

            # Handle Game Quit Message
            if event.type == pygame.QUIT:
                self.__run_event = False
                self.__run_draw = False

            # No-Op sent, draw if set to always draw
            elif event.type == pygame.NOEVENT:
                if self.__always_draw or self.__dirty == True:
                    self.__dirty = False
                    self._draw()


            # Handle User event Timers
            elif event.type >= pygame.USEREVENT and \
                event.type < pygame.NUMEVENTS:

                timer_id = event.type - pygame.USEREVENT

                # Call timer
                self.__active_event_timers[timer_id]()

            # Check if we should activate the console
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w \
                    and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.console.set_active()

            # Pass event to console
            # console will return false if not used. If it is not used
            # Then pass them to all
            elif not self.console.process_input(event):
                # Make a copy first so that adding events don't get fired
                # right away
                list_cp = self.__event_cb[:]

                # Reverse list so that newest stuff is on top
                # TODO: cache this list
                list_cp.reverse()

                for cb in list_cp:
                    # Fire the event for all in cb and stop
                    # if the callback returns True
                    if cb(event) == True:
                        break

    def stop_event_loop(self):
        """
        Sends a pygame.QUIT event into the event queue which
        exits the event loop
        """
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def add_event_callback(self, cb):
        """
        Adds event callback to the event callback stack

        @param cb:  Callback to be added to the stack when events are fired.
        """
        self.__event_cb.append(cb)

    def remove_event_callback(self, cb):
        """
        Removes an event from the event callback stack

        @param cb:       The callback to remove from the event callback stack
        @return:         Returns true if successful in removing callback
        """
        try:
            self.__event_cb.remove(cb)
            return True
        except:
            return False

    def list_event_callbacks(self):
        """
        Returns a string representation of all events registered with the game
        engine
        """
        event_callbacks = "Event Listeners:\n"
        for eventlst in self.__event_cb:
            event_callbacks = "%s\t%s\n" % (event_callbacks, str(eventlst))
        return event_callbacks

    def add_draw_callback(self, fnc):
        """
        Adds a callback to the draw list.  Function will be passed the
        game screen it should draw too.

        @param fnc:    The function to call when system is drawing
        """
        self.__draw_lst.append(fnc)

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
        Lists all the draw callbacks currently registered with the game engine
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
        return name in self.__object_hold

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

    def toggle_fps(self):
        """
        Toggles fps display
        """
        self.__showfps = not self.__showfps

    def __drilldown_object(self, objectname):
        """
        Takes the objectname string and tries to find the object that it is
        representing and returns that object.

        Example: battle.enemy_list[1].sprite._images[1]

        @param objectname:  The string that represents the object's path.
        @return:            Returns the object requested
        @raise Exception:   Throws an Exception with the string being the
                            path error.
        """
        last = "empt"
        obj = "empt"
        last_token = ""

        # Objects are separated by the period (".") symbol
        object_tokens = objectname.split(".")

        # Check if the first part of the name is registered with the
        # game engine as that is our starting point
        try:
            obj = self.__object_hold[object_tokens[0]]
            last = obj
            last_token = object_tokens[0]

        except KeyError:
            raise Exception("%s is not registered with the game engine" %
                   object_tokens[0])

        # Handles dot notation for sub modules by looping through the tokens
        for token in object_tokens[1:]:

            # Splits the dictionary/list token ("[")
            dict_token = token.split('[')
            try:
                last = obj
                obj = getattr(obj, dict_token[0])
                last_token = dict_token[0]

            except:
                raise Exception("Error finding member element: %s" % token)

            # Handles dictionaries
            for d_token in dict_token[1:]:
                if d_token[-1] == "]":
                    d_token = d_token[:-1]
                    # Try list notation first then try dictionary notation
                    try:
                        key = int(d_token)
                    except:
                        key = d_token

                    try:
                        last = obj
                        obj = obj[key]
                        last_token = key
                    except:
                        raise Exception("Unable to find %s" % key)

                else:
                    raise Exception("Invalid Syntax, expected ] at end of %s" %
                                    d_token)

        return obj, last, last_token

    def set_eval(self, objectname, statement):
        """
        Sets the object referenced by objectname to a value returned by
        passing the string stored in the val parameter to an eval statement.

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        @param val:         A string to be evaluated and set to the object.
        """
        try:
            obj, last, last_token = self.__drilldown_object(objectname)
        except Exception as detail:
            return str(detail)

        try:
            setattr(last, last_token, eval(str(statement)))
        except Exception as detail:
            return str(detail)

    def set_str(self, objectname, val):
        """
        Sets the object referenced by objectname to a string passed into the
        val parameter.

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        @param val:         A string to be set as the value of the object.
        """
        try:
            obj, last, last_token = self.__drilldown_object(objectname)
        except Exception as detail:
            return str(detail)

        setattr(last, last_token, val)

    def set_int(self, objectname, val):
        """
        Sets the object referenced by objectname to an integer passed into the
        val parameter. It may be a string that holds the int as it will be
        type casted.

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        @param val:         An int/string containing an int to be set as
                            the value of the object.
        """
        try:
            obj, last, last_token = self.__drilldown_object(objectname)
        except Exception as detail:
            return str(detail)

        try:
            setattr(last, last_token, int(val))
        except:
            return str(detail)

    def inspect_object(self, objectname):
        """
        Displays information about the object path it is passed

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        """
        try:
            obj, last, last_token = self.__drilldown_object(objectname)

        except Exception as detail:
            return str(detail)

        classname = obj.__class__.__name__

        # If it has the __dict__ attribute, it is an object we can inspect
        if hasattr(obj, "__dict__"):
            attribute_list = "Attributes:"
            attributes = obj.__dict__
            for attribute_key in attributes.keys():
                attribute_list = "%s\n\t%s:%s" % (attribute_list,
                                 attribute_key, str(attributes[attribute_key]))

            # Inspect the object for all its methods
            method_list = inspect.getmembers(obj, inspect.ismethod)
            if method_list != []:

                # Loop through the methods in the object and print them
                # to the console
                attribute_list = "%s\n\nMethods:" % attribute_list
                for method in method_list:
                    attribute_list = "%s\n\t%s" % (attribute_list, method[0])

                    # Inspect the arguments to the current method
                    args, vargs, kwargs, local = inspect.getargspec(method[1])

                    # Display function arguments
                    attribute_list = "%s\n\t\tArgs: %s" % \
                        (attribute_list, ",".join(args))

                    # Display * and ** arguments if they were found
                    if vargs:
                        attribute_list = "%s\n\t\tVArgs: %s" % \
                            (attribute_list, ",".join(vargs))

                    # Display KW Arguments if they were found
                    if kwargs:
                        attribute_list = "%s\n\t\tKWArgs: %s" % \
                            (attribute_list, ",".join(kwargs))

        # If dictionary, show keys
        elif hasattr(obj, "keys"):
            attribute_list = "Dictionary Items:"

            for d_obj in obj.keys():
                attribute_list = "%s\n\t%s:%s" % (attribute_list, d_obj,
                                                  str(obj[d_obj]))

        # If list, iterate over the list and show its values
        elif type(obj).__name__ == 'list':
            i = 0
            attribute_list = "List Items:"
            for item in obj:
                attribute_list = "%s\n\t%d:%s" % (attribute_list, i, str(item))
                i = i + 1

        # We don't know what it is, so just display string representation
        # of the object in question
        else:
            attribute_list = str(obj)

        return "Class: %s\n%s" % (classname, attribute_list)

    def art_scale(self, original, expected, width=True):
        if width:
            return int(self.width / float(expected) * float(original))
        else:

            return int(self.height / float(expected) * float(original))
