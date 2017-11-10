# An object that represents an operation on a set of objects from the game database
class System(object):
    def __init__(self):
        # Handle for the entity manager instance
        self.entity_manager = None

        # Handle for the system manager instance
        self.system_manager = None

        # Handler for the event manager instance
        self.event_manager = None

        # The priority for this system when the system manager runs
        self.priority = None

    # Init system after it has been created
    def init(self):
        pass

    # Run the system for this frame. This method is called by the system
    # manager, and is where the functionality of the system is implemented.
    def update(self, dt):
        pass