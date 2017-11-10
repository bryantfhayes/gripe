from core.EntityManager import EntityManager
from core.SystemManager import SystemManager
from core.EventManager import EventManager

import time

class GameManager(object):
	def __init__(self):
		# Setup links between the various managers
		self.entity_manager = EntityManager()
		self.system_manager = SystemManager(self.entity_manager)
		self.event_manager = EventManager(self, self.entity_manager, self.system_manager)
		self.entity_manager._event_manager = self.event_manager
		self.system_manager._event_manager = self.event_manager
		self.lastUpdated = 0
		self.running = True

	def run(self):
		while (self.running):
			currentTime = time.time()
			delta = currentTime - self.lastUpdated
			self.lastUpdated = currentTime
			self.system_manager.update(delta)


