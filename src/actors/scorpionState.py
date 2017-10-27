# -*- coding: utf-8 -*-
import pygame
import actor as Actor
from actorState import *
from ..resources.constants import *
import math	
from random import randint



class ScorpionDecisor(ActorDecisor):
	def __init__(self, state):
		ActorDecisor.__init__(self, state)
		self.moveHowMuch = 15 #Cuanto se tiene que mover hacia ese lado
		self.moveTo = 1 # 1 se mueve a la derecha, 0 a la izquierda

	def prolog(self,fase):
		ActorDecisor.prolog(self,fase)
		self.moveHowMuch = self.moveHowMuch-1
		#La idea es que se mueva seguido hacia un lado, y cuando se ha movido hacia ese lado el valor
		#del contador, se vuelve a tirar un dado a ver hacia donde se mueve de nuevo
		if (self.moveHowMuch == 0):
			if (randint(1,2)==1):  
				self.moveTo = 0    
			else:
				self.moveTo = 1    
			self.moveHowMuch = 15

	def moveRight(self,nState,stage):
		#La idea de este, y de moveLeft es que se mueva hacia ese lado, y comprobar si la plataforma de suelo 
		#sobre la que esta acaba donde va a estar en el siguiente instante de tiempo
		pixelsToMove = abs(self.getActor().physics.getSpeed()[0]*stage.time)
		IMustJump = False
		nState = self.onMoveRight()
		for platform in stage.grupoFloor:
			if (abs(platform.rect.right - self.getActor().rect.left) <= pixelsToMove and abs(platform.rect.top -self.getActor().rect.bottom) < 20):
				#Si no le sale bien la tirada, se cae a proposito, por manco
				if (randint(1,10) <= stage.getLevel()*2):
					nState = self.onJump()
				return nState

		for trap in stage.grupoTraps:
			if (abs(trap.rect.left - self.getActor().rect.right) <= pixelsToMove +20 and abs(trap.rect.bottom -self.getActor().rect.bottom) < 30):
				#Si no le sale bien la tirada, se cae a proposito, por manco
				if (randint(1,20) <= stage.getLevel()*2*10):
					nState = self.onJump()
				return nState

		return nState

	def moveLeft(self,nState,stage):
		pixelsToMove = abs(self.getActor().physics.getSpeed()[0]*stage.time)
		IMustJump = False
		nState = self.onMoveLeft()
		for platform in stage.grupoFloor:
			if (abs(platform.rect.left - self.getActor().rect.right) <= pixelsToMove and abs(platform.rect.top -self.getActor().rect.bottom) < 20):
				if (randint(1,10) <= stage.getLevel()*2):
					nState = self.onJump()
				return nState

		for trap in stage.grupoTraps:
			if (abs(trap.rect.right - self.getActor().rect.left) <= pixelsToMove +20 and abs(trap.rect.bottom -self.getActor().rect.bottom) < 30):
				if (randint(1,20) <= stage.getLevel()*2):
					nState = self.onJump()
				return nState

		return nState


	def newState(self, stage):
		drinPosition = stage.drin.physics.getPosition()
		scorpionPosition = self.getActor().physics.getPosition()
		nState = self.state


		#Si un disparo le va a dar, salta para esquivarlo
		#Para cada disparo, si va dirigido a mi cuerpo, salto cuando me vaya a dar teniendo en cuenta la velocidad
		# del mismo y mi velocidad de salto enfuncion de la distancia que le queda por recorrer hasta darme
 		for element in stage.getPlayerShots():
			if (element.rect.bottom >= self.getActor().rect.top and element.rect.top <= self.getActor().rect.bottom):
				if (abs(element.physics.getPosition()[0]-scorpionPosition[0])*element.physics.getSpeed()[0] <
					self.getActor().stats.getMaxJumpSpeed()*abs(self.getActor().rect.top-self.getActor().rect.bottom)):
					if (randint(1,30) <= stage.getLevel()):
						nState = self.onJump()
						


		if self.getActor().rect.left>=0 and self.getActor().rect.right<=ANCHO_PANTALLA:			
			#SI ESTA EN LA PANTALLA
			distanciaX =drinPosition[0]-scorpionPosition[0]
			distanciaY = drinPosition[1]-scorpionPosition[1]
			distancia = math.sqrt(abs(distanciaX) + abs(distanciaY))
			if distancia < MELEE_VISION_RANGE*(float(stage.getLevel())/3):
				#SI ESTA DENTRO DE SU RANGO DE VISIÓN, VA A POR DRIN
				if (distanciaY < -10):
					#Si esta arriba, salto a por el
					nState = self.onJump()	
				if (distanciaY > 10):
					#Si debajo hay una plataforma normal, puede bajar
					for platform in stage.grupoPlatforms:#
						if (platform.rect.left <= self.getActor().rect.left and platform.rect.right >= self.getActor().rect.right 
							and  platform.rect.top > self.getActor().rect.bottom):
							nState = self.onDown()
						
					#Si hay una plataforma de suelo abajo, puede bajar
					for platform in stage.grupoFloor:
						if (platform.rect.left <= self.getActor().rect.left and platform.rect.right >= self.getActor().rect.right and platform not in stage.grupoVoid):
							nState = self.onDown()

				#PERSIGO A DRIN
				if drinPosition[0]>scorpionPosition[0]:
					nState = self.moveRight(nState,stage)
				elif drinPosition[0]<scorpionPosition[0]:
					nState = self.moveLeft(nState,stage)

				#SI ESTA EN MI RANGO DE ATAQUE, LE ZURRO
				if (distancia < MELEE_ATTACK_RANGE):
					nState = self.onMelee()

			else:
				#NO TE VE, SE MUEVE ALEATORIAMENTE
				if self.moveTo == 1:
					nState = self.moveRight(nState,stage)
				else:
					nState = self.moveLeft(nState,stage)

		else:
			#ESTÁ FUERA DE LA PANTALLA, VOY A POR DRIN
			if (self.getActor().rect.left<0):
				nState = self.moveRight(nState,stage)
			elif(self.getActor().rect.right>ANCHO_PANTALLA):
				nState = self.moveLeft(nState,stage)

	
		return nState


	def getMeleeClass(self, actor):
		return ScorpionMelee(actor, self)


'''STATES'''



class ScorpionInit(ActorInit):
	def __init__(self, actor):
		ActorInit.__init__(self, actor, ScorpionDecisor(self))

class ScorpionMelee(ActorMelee):
	def registerShot(self, shot):
		self.actor.stage.registerEnemyHit(shot)


