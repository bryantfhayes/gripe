class Entity(object):
    __slots__ = ("_guid", "components", "symbol")
    """Encapsulation of a GUID to use in the entity database."""
    def __init__(self, guid, symbol=' '):
        """:param guid: globally unique identifier
        :type guid: :class:`int`
        """
        self._guid = guid
        self.components = {}
        self.symbol = symbol

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, self._guid)

    def __hash__(self):
        return self._guid

    def __eq__(self, other):
        return self._guid == hash(other)