from ..engines.state import *
from ..resources.constants import *

class HPCounterDecisor(Decisor):
	def __init__(self, state):
		Decisor.__init__(self, state)

class HPCounterStateInit(State):
	def __init__(self, actor):
		State.__init__(self, actor, HPCounterDecisor(self))
		self.actor.physics.position = self.calculatePosition()
		print self.actor.physics.position
		
	def calculatePosition(self):
		'''This method should be edited to define the behaviour of the movement.
		Right now, it's fixed in the same position the creator is + 30 pixels'''
		(baseposx, baseposy) = self.actor.creator.physics.position
		rect = self.actor.creator.rect
		if self.actor.creator.graphics.direction == LEFT:
			basepox = rect.left - (self.actor.rect.left-self.actor.rect.width)
		else:
			baseposx = rect.left + rect.width
		return (baseposx,baseposy)


