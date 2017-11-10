from core.Exceptions import *

class SystemManager(object):
    def __init__(self):
        pass
    
    # A container and manager for :class:`ecs.models.System` objects.
    def __init__(self, entity_manager):
        self._systems = []
        self._system_types = {}
        self._entity_manager = entity_manager
        self._event_manager = None

    # Allow getting the list of systems but not directly setting it.
    @property
    def systems(self):
        return self._systems

    # Add a sub-system to the system manager
    def add_system(self, system_instance, priority=0):
        system_type = type(system_instance)
        if system_type in self._system_types:
            raise DuplicateSystemTypeError(system_type)
        if system_instance.system_manager is not None:
            raise SystemAlreadyAddedToManagerError(
                system_instance, self, system_instance.system_manager)
        system_instance.entity_manager = self._entity_manager
        system_instance.system_manager = self
        system_instance.event_manager = self._event_manager
        system_instance.init()

        self._system_types[system_type] = system_instance
        self._systems.append(system_instance)

        system_instance.priority = priority
        self._systems.sort(key=lambda x: x.priority)

    def remove_system(self, system_type):
        system = self._system_types[system_type]
        system.entity_manager = None
        system.system_manager = None
        self._systems.remove(system)
        del self._system_types[system_type]

    # Run each system's ``update()`` method for this frame. The systems
    # are run in the order in which they were added.
    def update(self, dt):

        # Iterating over a list of systems instead of values in a dictionary is
        # noticeably faster. We maintain a list in addition to a dictionary
        # specifically for this purpose.
        #
        # Though initially we had the entity manager being passed through to
        # each update() method, this turns out to cause quite a large
        # performance penalty. So now it is just set on each system.
        for system in self._systems:
            system.update(dt)