from core.GameManager import GameManager

from systems.Input import Input
from systems.Renderer import Renderer
from systems.Physics import Physics

from components.Transform2D import Transform2D
from components.Health import Health

from util.Vector2D import Vector2D

player = None
game = None

def init(game):
    # Apply all sub-systems to system manager
    game.system_manager.add_system(Input(), priority=0)
    game.system_manager.add_system(Renderer(50, 30), priority=0)
    game.system_manager.add_system(Physics(), priority=0)

def create_player(game):
    global player
    player = game.entity_manager.create_entity('@')
    game.entity_manager.add_component(player, Transform2D())
    game.entity_manager.add_component(player, Health())


def onKeyPressed(args):
    char = args["char"]
    v = None

    if char == "UP":
        v = Vector2D(0, -1)
    elif char == "LEFT":
        v = Vector2D(-1, 0)
    elif char == "RIGHT":
        v = Vector2D(1, 0)
    elif char == "DOWN":
        v = Vector2D(0, 1)
    elif char == "F":
        game.event_manager.fireEvent("EVENT_FocusCameraOnEntity", player)
        return
    elif char == "G":
        game.event_manager.fireEvent("EVENT_FocusCameraOnEntity", None)
        return
    else:
        return

    game.event_manager.fireEvent("EVENT_MoveEntity", {"entity" : player, "vector2D" : v})

def quitCallback(args):
    game.running = False

def main():
    global game, player

    # Make an instance of game engine
    game = GameManager()

    # Setup game systems
    init(game)

    # DO GAME LOGIC STUFF #

    # Create a player
    create_player(game)

    # Get key presses
    game.event_manager.subscribe("EVENT_KeyPressed", onKeyPressed)

    # END GAME LOGIC STUFF #

    # Register game over callback on "Q" being pressed
    game.event_manager.subscribe("EVENT_QuitGame", quitCallback)

    # Run game
    game.run()

if __name__ == "__main__":
    main()