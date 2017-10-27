# -*- coding: utf-8 -*-
import pygame
import actor as Actor
from actorState import *
from ..resources.constants import *
import math
from random import uniform
from random import randint

	
'''NOTE: Before reading this, read state ando actorState documentation and/or incode comments'''
'''Cactus. He moves left. I like calling him Timmy. Say hi, Timmy'''
'''DECISOR'''

class CactusDecisor(ActorDecisor):
	def __init__(self, state):
		ActorDecisor.__init__(self, state)

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
		cactusPosition = self.getActor().physics.getPosition()
		nState = self.state

		distanciaX =drinPosition[0]-cactusPosition[0]
		distanciaY = drinPosition[1]-cactusPosition[1]
		distancia = math.sqrt(distanciaX**2 + distanciaY**2)

		#Si un disparo le va a dar, salta para esquivarlo
 		for element in stage.getPlayerShots():
			if (element.rect.bottom >= self.getActor().rect.top and element.rect.top <= self.getActor().rect.bottom):
				if (abs(element.physics.getPosition()[0]-cactusPosition[0])*abs(element.physics.getSpeed()[0]) <
					self.getActor().stats.getMaxJumpSpeed()*abs(element.physics.getPosition()[1]*2)):
					if (randint(1,30) <= stage.getLevel()):
						nState = self.onJump()
						

		if (self.getActor().rect.left + stage.scrollx <= 50 or self.getActor().rect.right + stage.scrollx + 50 >= stage.decorado.rect.right) and abs(distanciaX) < RANGED_SCAPE_VISION:
			#En este estado esta atrapado entre el fin d ela pantalla y tu, por lo que te dispara a bocajarro
			nState = self.onIdle()
			#Me pongo mirando hacia el
			if (drinPosition[0]>cactusPosition[0]):
				self.getActor().graphics.direction = RIGHT
			else:	
				self.getActor().graphics.direction = LEFT

			if (randint(1,10) < stage.getLevel() + 4) :
				#Si dispara hacia drin
				nState= self.onShoot()
			else:
				#Si dispara hacia otro lado
				direccionY = uniform(-1, 1)
				if (drinPosition[0]>cactusPosition[0]):
					direccionX = uniform(0.001, 1)
				else:
					direccionX = uniform(-1, 0.01)
				nState= self.onShoot((direccionX,direccionY))

		else:
			if self.getActor().rect.left>=0 and self.getActor().rect.right<=ANCHO_PANTALLA:	
				#SI ESTA EN LA PANTALLA
				if distancia < RANGED_VISION_RANGE*(float(stage.getLevel())/3):
					#SI ESTA DENTRO DE SU RANGO DE VISIÓN
					if (distanciaY < -10 and distanciaY > -50):
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

					if abs(distanciaX) < RANGED_SCAPE_VISION:
						#SI ESTA DEMASIADO CERCA, TIENE QUE ESCAPAR
						if drinPosition[0]>cactusPosition[0]:
							nState = self.moveLeft(nState,stage)
						elif drinPosition[0]<cactusPosition[0]:
							nState = self.moveRight(nState,stage)
					else:
						#ESTA EN EL RANGO DE VISION LISTO PARA MATAR
						nState = self.onIdle()
						#Me pongo mirando hacia el
						if (drinPosition[0]>cactusPosition[0]):
							self.getActor().graphics.direction = RIGHT
						else:	
							self.getActor().graphics.direction = LEFT

						if (randint(1,10) < stage.getLevel() +4) :
							#Si dispara hacia drin
							nState= self.onShoot()
						else:
							#Si dispara hacia otro lado
							direccionY = uniform(-1, 1)
							if (drinPosition[0]>cactusPosition[0]):
								direccionX = uniform(0.001, 1)
							else:
								direccionX = uniform(-1, 0.01)
							nState= self.onShoot((direccionX,direccionY))
				else:
				    #NO TE VE                
				   	nState = self.onIdle()
			else:
				#ESTÁ FUERA DE LA PANTALLA, VOY A POR drin
				#if (self.getActor().rect.left <10 or self.getActor().rect.right() >ANCHO_PANTALLA):
				if (abs(distanciaX) >= RANGED_SCAPE_VISION):
					if (self.getActor().rect.left<0):
						nState = self.moveRight(nState,stage)
					elif(self.getActor().rect.right>ANCHO_PANTALLA):
						nState = self.moveLeft(nState,stage)
				else:
					if (self.getActor().rect.left<0):
						nState = self.moveLeft(nState,stage)
					elif(self.getActor().rect.right>ANCHO_PANTALLA):
						nState = self.moveRight(nState,stage)

		#return self.onMoveLeft()
		return nState

	def getShootingClass(self, actor, direction = None):
		return CactusShooting(actor, self, direction)

'''STATES'''

class CactusInit(ActorInit):
	def __init__(self, actor):
		ActorInit.__init__(self, actor, CactusDecisor(self))

class CactusShooting(ActorShooting):
	'''Set ranged recoil, creates Ranged shot, animation = SPRITE_SHOOTING'''

	def registerShot(self, shot): #Remember, each actor knows if his shot is Ally or not...
		self.actor.stage.registerEnemyShot(shot)
	def createShot(self):
		from shot import CactusRangedShot
		return CactusRangedShot(self.actor, self.actor.stage)  

