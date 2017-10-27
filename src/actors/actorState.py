# -*- coding: utf-8 -*-
from ..engines.state import *
from ..resources.constants import *
import pygame

'''NOTE: Before reading this, read state documentation and/or incode comments'''

'''Actor state has a default implementation for actors that can move, jump, shoot and
attack. It has no implementations for newState (so it can be used to npc or with a player
controlller) nor methods which "registers" shots (so it's possible to make a difference 
between enemy and ally shots)

This class also implements the idea of the "state-changeable" automaton. Read ActorDecisor
documentation for more info'''

'''DECISOR'''

class ActorDecisor(Decisor):
	'''The best way to understand this Decisor is trying to imagine this like a graph.
	Each graph node is one ActorX class, which inherits from ActorState.
	Each edge is one action (melee, jump, moveRight, moveLeft, idle)

	To go from nodeA to nodeB with action X, decisor calls nodeA.onX(), and it returns nodeB,
	which is the new state.

	So, if actor.state is ActorIdle, and decisor.newStates determines that next action is OnMelee,
	OnMelee should return a new State (ActorMelee), which will be assigned to actor.state

	Why so complicated? Well, this design allows something really powerful: automaton behaviour
	inheritance. Or the ability to get "changeable states".

	Let me explain: imagine you want to create DoubleShotEnemy, which has exactly the same behaviour
	as generic behaviour, except it has a double shot ability, instead the single, default one.

	Right now, when onShoot is called, mehtod ActorDecisor.getShootingClass() is called too.

	You can create an DoubleShotDecisor(Decisor) class, and only overriding getShootingClass, 
	you will get this behaviour. Why? Because the creation of the concrete state is delegated to
	getXClass methods. The "edges" are presetted. The "place" they arrive can be changed. So it's literally
	like take your automaton, rip off one state and put another once in that place.
	'''
	def __init__(self, state):
		Decisor.__init__(self, state)
		self.down = False

	'''"Edges". onXMethods call the getXMethod, which returns the newState to this action'''
	def onMelee(self):
		if self.canAttack():
			return self.getMeleeClass(self.getActor())
		else:
			return self.state

	def onShoot(self, direction = None):
		if self.canAttack():
			return self.getShootingClass(self.getActor(), direction)
		else:
			return self.state

	def onJump(self):
		if self.state.hasLanded():
			return self.getJumpingClass(self.getActor())
		else:
			return self.state

	def onDown(self):
		return self.getMovingRightClass(self.getActor())

	def onMoveLeft(self):
		return self.getMovingLeftClass(self.getActor())

	def onMoveRight(self):
		return self.getMovingRightClass(self.getActor())

	def onStopMoving(self):
		return self.getOnStopMovingClass(self.getActor())

	def onIdle(self):
		return self.getIdleClass(self.getActor())

	def onDown(self):
		return self.getDownClass(self.getActor())

	'''Getters. Return the class wich implements '''

	def getMeleeClass(self, actor):
		return ActorMelee(actor, self)

	def getShootingClass(self, actor, direction = None):
		return ActorShooting(actor, self, direction)

	def getJumpingClass(self, actor):
		return ActorJumping(actor, self)

	def getMovingLeftClass(self, actor):
		return ActorMovingLeft(actor, self)

	def getMovingRightClass(self, actor):
		return ActorMovingRight(actor, self)

	def getIdleClass(self, actor):
		return ActorIdle(actor, self)

	def getOnStopMovingClass(self, actor):
		return ActorStopMoving(actor, self)

	def getDownClass(self, actor):
		return ActorDown(actor, self)

	def prolog(self, stage=None):
		'''Remember, prolog will be executed by ALL states BEFORE asking decisor'''
		self.state.stage = stage
		self.state.updateHurt() #Updates ghostMode, if needed. Check method for more info

		#Gravity update... if needed
		if self.state.hasLanded():
			self.state.actor.physics.setSpeedY(0)
		else:
			self.state.actor.physics.addSpeedY(GRAVITY * stage.time) 
		self.down = False
		#Each attack has his own recoil/cooldown (time before attacking again). They're updated here
		self.state.actor.stats.addShootRecoil(-1)
		self.state.actor.stats.addMeleeRecoil(-1)

	def canAttack(self):
		return self.getActor().stats.getMeleeRecoil() <= 0 and self.getActor().stats.getShootRecoil() <= 0


'''STATES'''
'''Implementations for each node/action, along with some generic utilities'''
class ActorState(State):
	def __init__(self, actor, decisor):
		State.__init__(self, actor, decisor)

	'''Future versions should create a collision engine'''
	def hasLanded(self):
		return self.actor.stage.collideWithFloor(self.actor) or (not self.decisor.down and self.actor.stage.collideWithPlatform(self.actor))

	def updateHurt(self):
		'''Update hurt enables the Ghost mode mechanich. While in ghost mode, you can't be hurt,
		and your sprite blinks. It has two handlers (onHurt and onRecover) to manage it. In order
		to implement ghostMode, method activateGhostMode(true) must be called in actor.hurt() function'''
		if self.actor.stats.getGhostModeTimer() <= 0:
			self.activateGhostMode(False)
		else:
			self.actor.stats.addGhostModeTimer(-1)

	def activateGhostMode(self, value):
		'''Activates (or deactivates) ghost mode functionality'''
		if value:
			self.onHurt()
		else:
			self.onRecover()

	def onHurt(self):
		'''While in ghost mode, sprite blinks. Ghost mode has a limited duration, specified in actor.stats'''
		self.actor.graphics.setBlink(True)
		self.actor.stats.setGhostMode(True)
		self.actor.stats.setGhostModeTimer(self.actor.stats.getMaxGhostModeTimer())

	def onRecover(self):
		'''Ghostrick mode out!'''
		self.actor.graphics.setBlink(False)
		self.actor.stats.setGhostMode(False)

class ActorInit(ActorState):
	'''Just the initial state'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)

'''Implementations for each actor state. Each state redefines onMyName methods to avoid
creating duplicated instances'''
class ActorIdle(ActorState):
	'''speed(0,0), SPRITE_IDLE animation'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)
		self.actor.physics.setSpeedX(0)
		self.actor.graphics.currentAnimation = SPRITE_IDLE

class ActorDown(ActorState):
	'''speed(0,0), SPRITE_IDLE animation'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)
		self.decisor.down = True

class ActorStopMoving(ActorState):
	'''speed(0,same)'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)
		self.actor.physics.setSpeedX(0)

class ActorMovingRight(ActorState):
	'''speed(+MAX_ACTOR_SPEED,0), SPRITE_WALKING animation, direction = RIGHT'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)
		self.actor.graphics.direction = RIGHT
		self.actor.physics.setSpeedX(self.actor.stats.getMaxRunSpeed())
		self.actor.graphics.currentAnimation = SPRITE_WALKING

class ActorMovingLeft(ActorState):
	'''speed(-MAX_ACTOR_SPEED,0), SPRITE_WALKING animation, direction = LEFT'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)
		self.actor.graphics.direction = LEFT
		self.actor.physics.speed = (-self.actor.stats.getMaxRunSpeed(),self.actor.physics.speed[1])
		self.actor.graphics.currentAnimation = SPRITE_WALKING

class ActorJumping(ActorState):
	'''speed(sameXSpeed,MAX_ACTOR_JUMP_SPEED), SPRITE_JUMPING animation'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)
		self.actor.physics.setSpeedY(-self.actor.stats.getMaxJumpSpeed())
		self.actor.graphics.currentAnimation = SPRITE_JUMPING


class ActorAttacking(ActorState):
	'''This class creates a generic shot. Shot behaviour must be defined extending this class'''
	def __init__(self, actor, decisor):
		ActorState.__init__(self, actor, decisor)
		shot = self.createShot()
		shot.update(self.actor.stage)
		self.registerShot(shot)#This method is NOT implemented in this file. Each actor must align his shots!
		self.setRecoil()

class ActorShooting(ActorAttacking):
	'''Set ranged recoil, creates Ranged shot, animation = SPRITE_SHOOTING'''
	def __init__(self, actor, decisor, direction):
		self.direction = direction
		ActorAttacking.__init__(self, actor, decisor)
		self.actor.graphics.currentAnimation = SPRITE_SHOOTING
	def setRecoil(self):
		self.actor.stats.setShootRecoil()
	def createShot(self):
		from shot import RangedShot #Circle references avoided!             <----- 
		return RangedShot(self.actor, self.actor.stage, self.direction)         #|
                                                                                #|
class ActorMelee(ActorAttacking):                                               #|
	'''Set melee recoil, creates Melee shot, animation should be different...'''#|
	def __init__(self, actor, decisor):								# -----------|
		ActorAttacking.__init__(self, actor, decisor)				# |
		self.actor.graphics.currentAnimation = SPRITE_MELEEING		# |
	def setRecoil(self):											# |
		self.actor.stats.setMeleeRecoil()				#  ------------
	def createShot(self):						#  -------|
		from shot import MeleeShot #pointer--------|
		return MeleeShot(self.actor)