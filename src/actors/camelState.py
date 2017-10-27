# -*- coding: utf-8 -*-
import pygame
import actor as Actor
from actorState import *
from ..resources.constants import *
import math
from random import randint


'''NOTE: Before reading this, read state ando actorState documentation and/or incode comments'''
'''camel. He moves left. I like calling him Timmy. Say hi, Timmy'''
'''DECISOR'''

class CamelDecisor(ActorDecisor):
	def __init__(self, state):
		ActorDecisor.__init__(self, state)
		self.count = 0
		self.dontStopMeNow = 0

	def prolog(self,fase):
		ActorDecisor.prolog(self,fase)
		self.count = self.count+1


	def newState(self, stage):
		DPX = stage.drin.physics.getPosition()[0]
		DPY = stage.drin.physics.getPosition()[1]
		CPX = self.getActor().physics.getPosition()[0]
		CPY = self.getActor().physics.getPosition()[1]
		nState = self.state

		if self.getActor().rect.left>=0 and self.getActor().rect.right<=ANCHO_PANTALLA:			
			#SI ESTA EN LA PANTALLA
			if (self.dontStopMeNow != 0):
				#Si tengo que correr hacia un lado
				if (self.dontStopMeNow == 1):
					nState= self.onMoveRight()
				else:
					nState= self.onMoveLeft()
			else:
				nState = self.onIdle()

				if DPX>CPX:
					self.getActor().graphics.direction = RIGHT
				else:
					self.getActor().graphics.direction = LEFT

			if (self.count % 500 == 0):
				#En este estado, corro hacia drin a tope
				if DPX>CPX:
					self.dontStopMeNow = 1
				else:
					self.dontStopMeNow = 2
			elif (self.count % 200 == 0):
				#En este estado disparo una ráfaga de babas
				if DPX>CPX:
					p = 1
				else:
					p=-1
				listOfShots = [(p*1,p*1),(p*1,-p*1),(p*1,0)]
				if (stage.getLevel() >= 4):
					listOfShots += [(p*1,p*0.5),(p*1,-p*0.5)]
				if (stage.getLevel() >= 6):
					listOfShots += [(p*1,p*0.25),(p*1,-p*0.25)]
				if (stage.getLevel() >= 8):
					listOfShots += [(p*1,p*0.75),(p*1,-p*0.75)]
				nState = self.onShoot(listOfShots)
			elif (self.count % 50 == 0):
				#En este estado disparo babas hacia drin
				norm = max(abs(DPX-CPX),abs(DPY-CPY))
				self.onShoot([((DPX-CPX)/norm,(DPY-CPY)/norm)])

		else:
			#ESTÁ FUERA DE LA PANTALLA, VOY A POR DRIN
			self.dontStopMeNow = 0
			if (self.getActor().rect.left<0):
				nState = self.onMoveRight()
			elif(self.getActor().rect.right>ANCHO_PANTALLA):
				nState = self.onMoveLeft()
						
		return nState




	def getMeleeClass(self, actor):
		return CamelMelee(actor, self)

	def getShootingClass(self, actor, direction = None):
		return CamelShooting(actor, self, direction)

'''STATES'''



class CamelInit(ActorInit):
	def __init__(self, actor):
		ActorInit.__init__(self, actor, CamelDecisor(self))

class CamelShooting(ActorShooting):
	def __init__(self, actor, decisor, direction):
		ActorState.__init__(self, actor, decisor)
		self.actor.graphics.currentAnimation = SPRITE_SHOOTING
		shots = self.createShots(direction)
		for shot in shots:
			shot.update(self.actor.stage)
			self.registerShot(shot)#This method is NOT implemented in this file. Each actor must align his shots!
			self.setRecoil()

	def createShots(self,direction):
		#devuelvo un array de rangedshots
		from shot import CamelRangedShot
		rangedShotsArray = []
		for dir in direction:
			rangedShotsArray += [CamelRangedShot(self.actor, self.actor.stage, dir)]
		return rangedShotsArray 

	def registerShot(self, shot): #Remember, each actor knows if his shot is Ally or not...
		self.actor.stage.registerEnemyShot(shot)


