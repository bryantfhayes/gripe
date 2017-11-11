from systems.System import System

import tdl

IGNORED_INPUTS = ["TEXT"]

class Input(System):
    def __init__(self):
        System.__init__(self)

    def update(self, dt):
        System.update(self, dt)
        for event in tdl.event.get(): # Iterate over recent events.
            if event.type == 'KEYDOWN':
                if event.keychar not in IGNORED_INPUTS:
                    self.event_manager.fireEvent("EVENT_KeyPressed", {"char" : event.keychar.upper()})
                    if (event.keychar.upper() == "Q"): self.event_manager.fireEvent("EVENT_QuitGame", {"game" : self.event_manager._game_manager})
            if event.type == 'KEYUP':
                if event.keychar not in IGNORED_INPUTS:
                    self.event_manager.fireEvent("EVENT_KeyReleased", {"char" : event.keychar.upper()})
