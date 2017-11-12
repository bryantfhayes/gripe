from core.EntityManager import EntityManager
from core.SystemManager import SystemManager
from core.EventManager import EventManager
from core.Singleton import Singleton

import util.Colors as Colors

import time

@Singleton
class GameManager(object):
	def __init__(self):
		pass

	def Init(self):
		# Setup links between the various managers
		SystemManager.Instance().Init()
		EntityManager.Instance().Init()
		EventManager.Instance().Init()

		self.lastUpdated = 0
		self.running = True
		self.message_log = []

	#
	# @brief Send notification containing the latest message log
	# 
	def message(self, msg, color=Colors.white):
		self.message_log.append({msg : {"color" : color}})
		EventManager.Instance().fireEvent("EVENT_ConsoleMessageAdded", self.message_log)

	#
	# @brief Run the game!
	# 
	def run(self):
		while (self.running):
			currentTime = time.time()
			delta = currentTime - self.lastUpdated
			self.lastUpdated = currentTime
			SystemManager.Instance().update(delta)


