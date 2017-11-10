from systems.System import System

from components.Transform2D import Transform2D

from util.Vector2D import Vector2D

class Physics(System):
	def __init__(self):
		System.__init__(self)

	def init(self):
		self.event_manager.subscribe("EVENT_moveEntity", self.attemptMove)

	def attemptMove(self, args):
		entity = args["entity"]
		transform = self.entity_manager.component_for_entity(entity, Transform2D)
		if transform != None:
			vector2D = args["vector2D"]
			newPosition = transform.position + vector2D
			
			# Check for collisions
			for e, component in self.entity_manager.pairs_for_type(Transform2D):
				if newPosition == component.position:
					return


			print("{0} + {1} = {2}".format(transform.position.x, vector2D.x, newPosition.x))
			print("MOVING PLAYER TO [{0} ,{1}]".format(newPosition.x, newPosition.y))

			# No collisions, so it is okay to move!
			transform.position = newPosition

	def update(self, dt):
		pass