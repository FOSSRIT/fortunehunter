import pygame

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

        self.debug = False

    def start_event_timer(self, id, time):
        pygame.time.set_timer(pygame.USEREVENT + id, time)

    def stop_event_timer(self, id):
        pygame.time.set_timer(pygame.USEREVENT + id, 0)

    def start_event_loop(self):
        """
        Starts the pygame event loop.
        """
        self.__run = True
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        while self.__run:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                self.__run = False

            else:
                # Send event to all event listeners
                # Make a copy first so that adding events don't get fired right away
                list_cp = self.__event_cb[:]

                # Reverse list so that newest stuff is on top
                list_cp.reverse()

                for cb in list_cp:
                    # Fire the event for all in cb and stop if return True
                    if cb(event) == True:
                        break
                self.draw()


                if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == '`':
                    self.debug = not self.debug
                    print "Debug set:",self.debug

            if self.debug:
                print "\n\n",event
                print "Event Listeners:", self.__event_cb
                for eventlst in self.__event_cb:
                    print "\t",eventlst

                print "\nDraw Callbacks:", self.__draw_lst
                for eventlst in self.__draw_lst:
                    print "\t",eventlst

                print "\nObjects Registered:"
                for eventlst in self.__object_hold:
                    print "\t",eventlst

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
        pygame.display.flip()

    def add_event_callback(self, cb):
        """
        Adds event callback to the event callback stack

        @param cb       Callback to be added to the stack when events are fired
        """
        self.__event_cb.append( cb )

    def remove_event_callback(self, cb):
        """
        Removes an event from the event callback stack

        @param cb       The callback to remove from the event callback stack
        @return         Returns true if sucessful in removing callback
        """
        try:
            self.__event_cb.remove( cb )
            return True
        except:
            return False

    def add_draw_callback(self, fnc):
        """
        Adds a callback to the draw list.  Function will be passed the game screen

        @param fnc      The funciton to call when system is drawing
        """
        self.__draw_lst.append( fnc )

    def pop_draw_callback(self):
        """
        Removes top of draw stack and returns it

        @return         Returns the top callback function that was removed
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

        @param fnc      The callback function to remove
        @return         Returns true if sucessful removal of the function
        """
        try:
            self.__draw_lst.remove(fnc)
            return True
        except:
            return False

    def has_object(self, name):
        """
        Returns true if object is stored in game engine

        @param name     Name of the object to check if exists
        @return         Returns true if object found
        """
        return self.__object_hold.has_key( name )

    def add_object(self, name, obj):
        """
        Adds an object to the game engine datastore

        @param name     The name used to store the object
        @param obj      The object to store
        """
        self.__object_hold[name] = obj

    def get_object(self, name):
        """
        Returns an object from the game engine datastore

        @param name     The name of object to return
        @return         Returns the object
        """
        return self.__object_hold[name]

    def remove_object(self, name):
        """
        Removes an object from the game engine datastore

        @param name     The name of the object to remove
        """
        del self.__object_hold[name]

class GameEngineElement(object):
    def __init__(self, has_draw=True, has_event=True):
        self.__has_draw = has_draw
        self.__has_event = has_event
        self.__in_engine = False
        self.game_engine = GameEngine.instance

    def is_in_engine(self):
        return self.__in_engine

    def add_to_engine(self):
        if not self.__in_engine:
            self.__in_engine = True

            if self.__has_draw:
                self.game_engine.add_draw_callback( self.draw )

            if self.__has_event:
                self.game_engine.add_event_callback( self.event_handler )

    def remove_from_engine(self):
        if self.__in_engine:
            self.__in_engine = False

            if self.__has_draw:
                self.game_engine.remove_draw_callback(self.draw)

            if self.__has_event:
                self.game_engine.remove_event_callback( self.event_handler )

    def event_handler(self, event):
        pass

    def draw(self, screen):
        pass
