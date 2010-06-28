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

from pyconsole.pyconsole import Console


class GameEngineConsole(Console):

    def __init__(self, gei, pos):

        # functions exposed to the console
        function_list = {
            "quit": gei.stop_event_loop,

            "list_objects": gei.list_objects,
            "list_drawcb": gei.list_draw_callbacks,
            "list_eventcb": gei.list_event_callbacks,
            "list_timers": gei.list_event_timers,
            "inspect": gei.inspect_object,

            "set_str": gei.set_str,
            "set_int": gei.set_int,
            "set_eval": gei.set_eval,
        }

        # Ctrl + key mappings
        key_calls = {
            "d": gei.stop_event_loop,
            "m": self.console_mode,
        }

        Console.__init__(self, gei.screen, pos,
                           functions=function_list, key_calls=key_calls,
                           vars={}, syntax={})

    def console_mode(self):
        """
        Switches console between console and python interpreter
        """
        # Deactivate Console if showing
        if self.console.active:
            self.console.set_active()
        self.console.setvar("python_mode",
                            not self.console.getvar("python_mode"))

        self.console.set_interpreter()
        self.console.set_active()
