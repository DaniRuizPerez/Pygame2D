# -*- coding: utf-8 -*-
import pygame
from ..resources.gestorRecursos import *
from ..resources.constants import *

class Graphics():
	def __init__(self, actor, imgName=None , conf=None, animCD = None, colorKey = -1):
		self.imgName = imgName
		self.sourceImg = None
		self.conf = conf
		self.animCD = animCD
		self.animCDCounter = 0
		self.actor = actor
		self.direction = RIGHT
		self.currentAnimation = SPRITE_IDLE
		self.playingAnimation = SPRITE_IDLE
		self.currentFrame = 0
		self.sheetCoord = []
		self.setGraphics(colorKey)
		self.animationOnGoing = False
		self.blink = False
		self.isText = False

	def changeImage(self, image, colorKey = -1):
		self.actor.image = GestorRecursos.CargarImagen(image,colorKey)
		self.actor.image = self.actor.image.convert_alpha()
		self.actor.rect = self.actor.image.get_rect()


	def setGraphics(self, colorKey = -1):
		if (self.imgName == None):
			self.actor.image = pygame.Surface((0, 0))
			self.actor.rect = self.actor.image.get_rect()
			return

		self.sourceImg = GestorRecursos.CargarImagen(self.imgName,colorKey)
		self.sourceImg = self.sourceImg.convert_alpha()

		#By default, we consider source as a sprite sheet
		# Se carga la sourceImg
		if (self.conf == None):
			self.actor.image = self.sourceImg
			self.actor.rect = self.actor.image.get_rect()
			return

		# Leemos las coordenadas de un archivo de texto
		data = GestorRecursos.CargarArchivoCoordenadas(self.conf)
		data = data.split('\n\n\n')

		animFrameCount = map(int, data[0].split())
		animFrames = data[1].split('\n\n')

		animFrames = [[map(int, c.split()) for c in line] for line in (x.split('\n') for x in animFrames)]

		for anim in range(len(animFrameCount)):
			self.sheetCoord.append([])
			tmp = self.sheetCoord[anim]
			for sprite in range(animFrameCount[anim]):
				frame = animFrames[anim][sprite]
				tmp.append(pygame.Rect(frame[0], frame[1], frame[2], frame[3]))

		self.actor.rect = pygame.Rect(100,100,self.sheetCoord[self.currentAnimation][self.currentFrame][2],self.sheetCoord[self.currentAnimation][self.currentFrame][3])
		self.currentAnimation = SPRITE_IDLE



	def updateAnimation(self):
		if (self.animCD == None or self.conf == None):
			return

		if self.canChangeAnimation() and self.currentAnimation != self.playingAnimation:
			self.playingAnimation = self.currentAnimation
			self.currentFrame = 0
		self.animCDCounter -= 1
		#Si está activado el parpadeo, salimos
		if (self.blink and self.animCDCounter%5 in [0,1,2]):
			self.actor.image = pygame.Surface((0, 0))
			return
		# Miramos si ha pasado el retardo para dibujar una nueva postura
		if (self.animCDCounter < 0):
			self.animCDCounter = self.animCD
			# Si ha pasado, actualizamos la postura
			self.currentFrame += 1



			if self.currentFrame >= len(self.sheetCoord[self.playingAnimation]):
				self.currentFrame = 0
				self.animationOnGoing = False
			else:
				self.animationOnGoing = True

			self.actor.image = self.sourceImg.subsurface(self.sheetCoord[self.playingAnimation][self.currentFrame])

			# Si esta mirando a la derecha, cogemos la porcion de la sourceImg
			if self.direction == RIGHT:
				self.actor.image = self.sourceImg.subsurface(self.sheetCoord[self.playingAnimation][self.currentFrame])
			#  Si no, si mira a la izquierda, invertimos esa imagen
			elif self.direction == LEFT:
				self.actor.image = pygame.transform.flip(self.sourceImg.subsurface(self.sheetCoord[self.playingAnimation][self.currentFrame]), 1, 0)

	def isAnimationOnGoing(self):
		return self.animationOnGoing

	def isBlockingAnimation(self):
		return (self.playingAnimation == SPRITE_SHOOTING or self.playingAnimation == SPRITE_MELEEING)

	def canChangeAnimation(self):
		if self.isAnimationOnGoing():
			return not self.isBlockingAnimation()
		else:
			return True


	def setBlink(self, value):
		self.blink = value