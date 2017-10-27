from shotState import *

class DrinShotMovingInit(ShotState):
	'''This class is the idea we all have of a shot. It moves. It hurts. It suicides if hit. Just a shot'''
	def __init__(self, actor):
		ShotState.__init__(self, actor, DrinShotDecisor(self))
		self.actor.graphics.currentAnimation = SPRITE_IDLE

class DrinShotMovingTravelling(ShotState):
	'''This class is the idea we all have of a shot. It moves. It hurts. It suicides if hit. Just a shot'''
	def __init__(self, actor, decisor):
		ShotState.__init__(self, actor, decisor)
		self.actor.graphics.currentAnimation = SPRITE_WALKING

class DrinShotDecisor(ShotDecisor):
	def __init__(self, state):
		ShotDecisor.__init__(self, state)
		self.timeTravelling = 0

	def prolog(self, stage):
		ShotDecisor.prolog(self, stage)
		self.timeTravelling += 1

	def newState(self, state):
		if self.timeTravelling >= 2:
			return DrinShotMovingTravelling(self.state.actor, self)
		return self.state