# -*- coding: utf-8 -*-
from ..engines.state import *
from ..resources.constants import *

'''NOTE: Before reading this, read state documentation and/or incode comments'''


'''Here I defined 2 example "shots": a melee one ("attached" to his actor), and a ranged one.
They are pretty simple, single state automatons, and use the default implementation of Decisor.'''

class ShotDecisor(Decisor):
	def __init__(self, state):
		Decisor.__init__(self, state)

	def prolog(self, stage):
		self.state.checkKill()

class ShotState(State):
	def __init__(self, actor, decisor = None):
		State.__init__(self, actor, decisor)

	def checkKill(self):
		"If shoot leaves screen, he will suicide. Only the good die young"
		if (self.actor.rect.left>=0 and self.actor.rect.right<ANCHO_PANTALLA +50 and self.actor.rect.bottom>=0 and self.actor.rect.top<ALTO_PANTALLA)  == False:
			self.actor.remove(self.actor.groups())
			self.actor.kill() #Kill removes actor from all groups, but it's still calleable, so next I call remove


class ShotMovingInit(ShotState):
	'''This class is the idea we all have of a shot. It moves. It hurts. It suicides if hit. Just a shot'''
	def __init__(self, actor):
		ShotState.__init__(self, actor, ShotDecisor(self))

class ShotAttachedInit(ShotState):
	'''Have you ever realised every time you punch someone you're shooting him? No? Of course not. But
	having melee attacks as a "shot" gaves us the ability to have attacks with extremly accurate hit-boxes.
	Also, we can reuse some shot methods, so it is less work. MODULARITY!!!!'''

	'''Attached shots (melee attacks) should be destroyed when the attack finishes. In order to check this,
	this state has a lifetime attribute. When lifetime is 0... caput.

	Also, in order to get the "sticky" behaviour, each frame, in prolog, shot position is recalculated 
	using creator's (the one who shooted) current position'''

	def __init__(self, actor):
		ShotState.__init__(self, actor, ShotDecisor(self))
		self.lifetime = self.actor.creator.stats.getMeleeAttackDuration()
		self.actor.physics.position = self.calculatePosition()

	def checkKill(self):
		self.lifetime -=1
		if self.lifetime <= 0:
			self.actor.kill()
			self.actor.remove()
		self.actor.physics.position = self.calculatePosition()
		
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


