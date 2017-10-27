# -*- coding: utf-8 -*-
import pygame
import actor as Actor
from actorState import *
from ..resources.constants import *
import math
from random import randint


'''NOTE: Before reading this, read state ando actorState documentation and/or incode comments'''
'''jetty. He moves left. I like calling him Timmy. Say hi, Timmy'''
'''DECISOR'''

class JettyDecisor(ActorDecisor):
	def __init__(self, state):
		ActorDecisor.__init__(self, state)
		self.count = 0
		self.howManyShots = 0
		self.dontStopMeNow = 0
		self.lotsOfShots = False
		self.moveHowMuch = 15 #Cuanto se tiene que mover hacia ese lado
		self.moveTo = 1 # 1 se mueve a la derecha, 0 a la izquierda

	def prolog(self,fase):
		ActorDecisor.prolog(self,fase)
		self.count = self.count+1
		self.howManyShots = self.howManyShots -1
		self.moveHowMuch = self.moveHowMuch-1
		#La idea es que se mueva seguido hacia un lado, y cuando se ha movido hacia ese lado el valor
		#del contador, se vuelve a tirar un dado a ver hacia donde se mueve de nuevo
		if (self.moveHowMuch == 0):
			if (randint(1,2)==1):  
				self.moveTo = 0    
			else:
				self.moveTo = 1    
			self.moveHowMuch = 15

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
				norm = max(abs(DPX-CPX),abs(DPY-CPY))
				if (self.dontStopMeNow == 1):
					nState= self.onMoveRight()
					self.onShoot((0,0))
				else:
					nState= self.onMoveLeft()
					self.onShoot((0,0))
			else:
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
			elif (self.count % 300 == 0):
				#En este estado, disparo un montón de veces
				self.lotsOfShots = not self.lotsOfShots
				self.howManyShots = 100
			elif (self.count % 50 == 0 or (self.lotsOfShots and self.howManyShots >= 0)):
				#SI le toca disparar o le toca porque dispara mucho
				#En este estado disparo hacia drin
				norm = max(abs(DPX-CPX),abs(DPY-CPY))
				self.onShoot(((DPX-CPX)/norm,(DPY-CPY)/norm))
			elif (self.moveTo == 1 and self.dontStopMeNow == 0):
				nState = self.onMoveRight()
			elif(self.dontStopMeNow == 0):
				nState = self.onMoveLeft()

		else:
			#ESTÁ FUERA DE LA PANTALLA, VOY A POR DRIN
			self.dontStopMeNow = 0
			if (self.getActor().rect.left<0):
				nState = self.onMoveRight()
			elif(self.getActor().rect.right>ANCHO_PANTALLA):
				nState = self.onMoveLeft()
		
	
		if (randint(1,10)==5):  
			if (randint(1,20)!=1): 
				nState = self.onDown()
			else:
				nState =  self.onJump()
		return nState



	def getMeleeClass(self, actor):
		return JettyMelee(actor, self)

	def getShootingClass(self, actor, direction = None):
		return JettyShooting(actor, self, direction)

'''STATES'''



class JettyInit(ActorInit):
	def __init__(self, actor):
		ActorInit.__init__(self, actor, JettyDecisor(self))

class JettyShooting(ActorShooting):
	def __init__(self, actor, decisor, direction):
		ActorState.__init__(self, actor, decisor)
		shot = self.createShot(direction)
		shot.update(self.actor.stage)
		self.registerShot(shot)#This method is NOT implemented in this file. Each actor must align his shots!
		self.setRecoil()
		self.actor.graphics.currentAnimation = SPRITE_SHOOTING

	def registerShot(self, shot): #Remember, each actor knows if his shot is Ally or not...
		self.actor.stage.registerEnemyShot(shot)
	def createShot(self,direction):
		from shot import JettyRangedShot
		return JettyRangedShot(self.actor, self.actor.stage,direction)  

