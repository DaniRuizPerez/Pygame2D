# -*- coding: utf-8 -*-
import pygame
import actor as Actor
from actorState import *
from ..resources.constants import *

'''NOTE: Before reading this, read state ando actorState documentation and/or incode comments'''

'''SimpleEnemy. He moves left. I like calling him Timmy. Say hi, Timmy'''

'''DECISOR'''
class SimpleEnemyDecisor(ActorDecisor):
	def __init__(self, state):
		ActorDecisor.__init__(self, state)

	def newState(self, stage):
		return self.onMoveLeft() # HE. MOVES. LEFT. BEST AI EVER

	def getMeleeClass(self, actor):
		return SimpleEnemyMelee(actor, self)

	def getShootingClass(self, actor, direction = None):
		return SimpleEnemyShooting(actor, self, direction)

'''STATES'''

class SimpleEnemyInit(ActorInit):
	def __init__(self, actor):
		ActorInit.__init__(self, actor, SimpleEnemyDecisor(self))

class SimpleEnemyShooting(ActorShooting):
	def registerShot(self, shot): #Remember, each actor knows if his shot is Ally or not...
		self.actor.stage.registerEnemyShot(shot)

class SimpleEnemyMelee(ActorMelee):
	def registerShot(self, shot):
		self.actor.stage.registerEnemyHit(shot)


