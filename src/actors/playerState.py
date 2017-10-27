# -*- coding: utf-8 -*-
import pygame
from actorState import *
from ..resources.constants import *


'''NOTE: Before reading this, read state and actorState documentation and/or incode comments'''

'''PlayerDecisor is the first "complex" decisor in the game. Using DRIN keys-related atributtes, user input
is proccesed, and then the onX functions are called. Magic happens'''

'''DECISOR'''
class PlayerDecisor(ActorDecisor):
	def __init__(self, state):
		ActorDecisor.__init__(self, state)

	def newState(self, state):
		actor = self.getActor()
		meleed = actor.keys[self.melee]
		shooted = actor.keys[self.ranged]
		jumped = actor.keys[self.arriba]
		movedLeft = actor.keys[self.izquierda]
		movedRight = actor.keys[self.derecha]
		down = actor.keys[self.abajo]
	
		idled = (meleed or shooted or jumped or movedLeft or movedRight) == False
		
		nState = self.state
		'''When the state is constructed, he apply some changes to his actor. Look careful, because
		more than one state can be built each time'''
		if movedLeft:
			nState = self.onMoveLeft()
		elif movedRight:
			nState = self.onMoveRight()
		else:
			nState = self.onStopMoving()
		if idled:
			nState = self.onIdle()
		if jumped:
			nState = self.onJump()
		if meleed:
			nState = self.onMelee()
		elif shooted:
			nState = self.onShoot()
		if down:
			nState = self.onDown()

		return nState

	def assignKeys(self):
		'''Just some setters. You know, it's easier like this'''
		actor = self.getActor()
		self.arriba = actor.keyCode[0]
		self.abajo = actor.keyCode[1]
		self.izquierda = actor.keyCode[2]
		self.derecha = actor.keyCode[3]
		self.melee = actor.keyCode[4]
		self.ranged = actor.keyCode[5]

	def getMeleeClass(self, actor): #Remember, override shots to make them allies
		return PlayerMelee(actor, self)

	def getShootingClass(self, actor, direction = None):
		return PlayerShooting(actor, self, direction)

'''STATES'''

class PlayerInit(ActorInit):
	def __init__(self, actor):
		ActorInit.__init__(self, actor, PlayerDecisor(self))
		self.decisor.assignKeys()

class PlayerShooting(ActorShooting):
	def registerShot(self, shot):
		self.actor.stage.registerPlayerShot(shot)
	def createShot(self):
		from shot import DrinRangedShot
		return DrinRangedShot(self.actor, self.actor.stage)  

class PlayerMelee(ActorMelee):
	def registerShot(self, shot):
		self.actor.stage.registerPlayerHit(shot)
	def createShot(self):				
		from shot import DrinMeleeShot
		return DrinMeleeShot(self.actor)