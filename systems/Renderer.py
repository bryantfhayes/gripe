from systems.System import System

from components.Transform2D import Transform2D

from util.Vector2D import Vector2D
from util.Misc import *

import tdl

class Renderer(System):
	def __init__(self, width, height, font='assets/arial_16x16.png'):
		System.__init__(self)
		self.width = width
		self.height = height

		self.mid = Vector2D(int(self.width / 2), int(self.height / 2))
		self.offset_transform = Transform2D(self.mid)

		# Set rendered font
		tdl.setFont(font)

		# Create console window
		self.window = tdl.init(self.width, self.height, "gripe engine")

	def init(self):
		# Register listener for setting camera focus
		self.event_manager.subscribe("EVENT_FocusCameraOnEntity", self.setCameraFocus)

	def setCameraFocus(self, entity):
		if entity == None:
			self.offset_transform = Transform2D(self.mid)
		else:
			try:
				self.offset_transform = entity.components["Transform2D"]
			except:
				print("[ERROR] Entity has no Transform2D component!")

	def drawEntities(self):
		for entity, transform in self.entity_manager.pairs_for_type(Transform2D):
			position = transform.position + (self.mid - self.offset_transform.position)

			# Only draw characters within bounds of screen
			if vectorInRange(position, 0, self.width, 0, self.height):
				self.window.drawChar(position.x, position.y, entity.symbol)

	def update(self, dt):
		self.window.clear()
		self.drawEntities()
		tdl.flush()