from systems.System import System

from components.Transform2D import Transform2D

from util.Vector2D import Vector2D
from util.Misc import *
import util.Colors as colors

import tdl, six

class Panel(object):
    Right = 0
    Bottom = 1
    def __init__(self, window, offsetX, offsetY, width, height, side, bounded=False):
        self.window = window
        self.width = width
        self.height = height
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.bounded = bounded
        self.side = side
        self.data = {"Hello World:" : {"color" : colors.red}}
        print(offsetX, offsetY, width, height)
        self.console = tdl.Console(width, height)

    def draw(self):
        if self.bounded:
            self.console.draw_rect(0, 0, self.width, self.height, None, fg=colors.red, bg=colors.dark_grey)

        # Draw stuff on panel
        count = 0
        for msg, fmt in six.iteritems(self.data):
            self.console.draw_str(0, count, "{0}".format(msg), bg=None, fg=fmt["color"])
            count += 1

        # Blit panel to main window
        self.window.blit(self.console, self.offsetX, self.offsetY, self.width, self.height)

class GamePanel(Panel):
    def __init__(self, window, offsetX, offsetY, width, height, parent, bounded=True):
        Panel.__init__(self, window, offsetX, offsetY, width, height, bounded)
        self.parent = parent

    def draw(self):
        for entity, transform in self.parent.entity_manager.pairs_for_type(Transform2D):
            position = transform.position + (self.parent.console_mid - self.parent.offset_transform.position)

            # Only draw characters within bounds of screen
            if vectorInRange(position, 0, self.width, 0, self.height):
                self.console.draw_char(position.x, position.y, entity.symbol)

        # Blit the contents of "console" to the root console
        self.window.blit(self.console, 0, 0, self.width, self.height, 0, 0)

class Renderer(System):
    def __init__(self, width, height, font='assets/terminal_8x12.png'):
        System.__init__(self)

        # Define screen sizes
        self.screen_width = width
        self.screen_height = height

        # Set rendered font
        tdl.set_font(font)

        # Create console window
        self.window = tdl.init(self.screen_width, self.screen_height, "gripe engine")

        # Initial screen properties
        self.console_mid = Vector2D(int(self.screen_width / 2), int(self.screen_height / 2))
        self.offset_transform = Transform2D(self.console_mid)

        # Add initial game panel (panel[0] is main game always)
        self.game_panel = GamePanel(self.window, 0, 0, self.screen_width, self.screen_height, self)
        self.panels = []

    def addPanel(self, panel):
        self.panels.append(panel)

        # Shrink game panel to fit within upper left hand corner
        if panel.side == Panel.Right:
            if panel.offsetX < self.game_panel.width:
                print("shrink x to: {}".format(panel.offsetX))
                self.game_panel.width = panel.offsetX
        elif panel.side == Panel.Bottom:
            if panel.offsetY < self.game_panel.height:
                print("shrink y to: {}".format(panel.offsetY))
                self.game_panel.height = panel.offsetY

        # Setup game window center in relation to panel[0] (main game scene)
        self.console_mid = Vector2D(int(self.game_panel.width / 2), int(self.game_panel.height / 2))
        self.offset_transform = Transform2D(self.console_mid)

    def init(self):
        # Register listener for setting camera focus
        self.event_manager.subscribe("EVENT_FocusCameraOnEntity", self.setCameraFocus)

    def setCameraFocus(self, entity):
        if entity == None:
            self.offset_transform = Transform2D(self.console_mid)
        else:
            try:
                self.offset_transform = entity.components["Transform2D"]
            except:
                print("[ERROR] Entity has no Transform2D component!")

    def drawAll(self):
        for panel in self.panels:
            panel.draw()

        # Draw game panel last
        self.game_panel.draw()

    def clearAll(self):
        # Clear windows
        self.game_panel.console.clear()
        for panel in self.panels:
            panel.console.clear(fg=colors.white, bg=colors.black)
        self.window.clear()

    def update(self, dt):
        self.clearAll()
        self.drawAll()
        tdl.flush()