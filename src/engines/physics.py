# -*- coding: utf-8 -*-
class Physics():
	def __init__(self,pos, spd, scroll, actor):
		self.position = pos
		self.speed = spd
		self.scroll = scroll
		self.actor = actor

#Position
	def getPosition(self):
		return self.position

	def setPosition(self,value):
		self.position = value

	def addPosition(self,value):
		self.position += value

#Speed
	def getSpeed(self):
		return self.speed

	def setSpeed(self,value):
		self.speed = value

	def setSpeedX(self, value):
		self.speed = (value, self.speed[1])

	def setSpeedY(self, value):
		self.speed = (self.speed[0], value)

	def addSpeed(self,value):
		self.speed += value

	def addSpeedX(self,value):
		self.speed = (self.speed[0], self.speed[1]+value)

	def addSpeedY(self,value):
		self.speed = (self.speed[0] , value + self.speed[1])
		
#Scroll
	def getScroll(self):
		return self.scroll

	def setScroll(self,value):
		self.scroll = value

	def addScroll(self,value):
		self.scroll += value

	def fixPosition(self, position):
		self.position = position
		self.actor.rect.left = self.position[0] - self.scroll[0]
		self.actor.rect.bottom = self.position[1] - self.scroll[1]

	def fixScreenPosition(self, backgroundScroll):
		self.scroll = backgroundScroll
		(scrollx, scrolly) = self.scroll
		(posx, posy) = self.position
		self.actor.rect.left = posx - scrollx
		self.actor.rect.bottom = posy - scrolly

	def incrementPosition(self, increment):
		(posx, posy) = self.position
		(incrementx, incrementy) = increment
		self.fixPosition((posx+incrementx, posy+incrementy))

	def updateMovement(self):
		incrementx = self.speed[0]*self.actor.stage.time
		incrementy = self.speed[1]*self.actor.stage.time
		self.incrementPosition((incrementx, incrementy))
