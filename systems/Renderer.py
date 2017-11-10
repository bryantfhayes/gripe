from systems.System import System

import tdl

class Renderer(System):
	def __init__(self, width, height, font='assets/arial_16x16.png'):
		System.__init__(self)
		self.width = width
		self.height = height

		# Set rendered font
		tdl.setFont(font)

		# Create console window
		self.window = tdl.init(self.width, self.height, "gripe engine")

	def update(self, dt):
		self.window.clear()
		tdl.flush()