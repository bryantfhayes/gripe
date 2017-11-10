from core.Events import *

class EventManager(object):
	def __init__(self, gameManager, entityManager, systemManager):
		self._game_manager = gameManager
		self._entity_manager = entityManager
		self._system_manager = systemManager
		self._events = {}

		# For each possible event, create a list which will hold the subscribed functions to call
		for e in EVENTS:
			self._events[e] = []

	def subscribe(self, event, fn):
		# Confirm event exists
		if event not in self._events:
			return

		# Add fn to end of list
		if fn not in self._events[event]:
			self._events[event].append(fn)

	def unsubscribe(self, event, fn):
		# Confirm event exists
		if event not in self._events:
			return

		if fn in self._event[event]:
			self._events[event].remove(fn)

	def fireEvent(self, event, args):
		# Confirm event exists
		if event not in self._events:
			return

		# Fire all registered functions for this event
		triggeredEvent = self._events[event]
		for fn in triggeredEvent:
			fn(args)