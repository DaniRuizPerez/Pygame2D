# -*- coding: utf-8 -*-
from ..stats import *

class Upgrade(Stats):
	def __init__(self, stats):
		Stats.__init__(self,0, 0, 0, 0, 0, 0, 0, 0)
		self.stats = stats

	def setStats(self, stats):
		self.stats = stats

	def getStats(self):
		return stats

#MaxHP
	def getMaxHP(self):
		return self.stats.getMaxHP()

	def setMaxHP(self,value):
		self.stats.setMaxHP(value)

	def addMaxHP(self,value):
		self.stats.addMaxHP(value)

#ActualHP
	def getActualHP(self):
		return self.stats.getActualHP()

	def setActualHP(self,value):
		self.stats.setActualHP(value)

	def addActualHP(self,value):
		self.stats.addActualHP(value)

#Damage
	def getDamage(self):
		return self.stats.getDamage()

	def setDamage(self,value):
		self.stats.setDamage(value)

	def addDamage(self,value):
		self.stats.addDamage(value)

#MaxSpeed
	def getMaxRunSpeed(self):
		return self.stats.getMaxRunSpeed()

	def setMaxRunSpeed(self,value):
		self.stats.setMaxRunSpeed(value)

	def addMaxRunSpeed(self,value):
		self.stats.addMaxRunSpeed(value)

#Jump Speed Scalar
	def getMaxJumpSpeed(self):
		return self.stats.getMaxJumpSpeed()

	def setMaxJumpSpeed(self,value):
		self.stats.setMaxJumpSpeed(value)

	def addMaxJumpSpeed(self,value):
		self.stats.addMaxJumpSpeed(value)


#Shoot Speed Scalar
	def getShotSpeed(self):
		return self.stats.getShotSpeed()

	def setShotSpeed(self,value):
		self.stats.setShotSpeed(value)

	def addShotSpeed(self,value):
		self.stats.addShotSpeed(value)


#Melee Speed
	def getMeleeSpeed(self):
		return self.stats.getMeleeSpeed()

	def setMeleeSpeed(self,value):
		self.stats.setMeleeSpeed(value)

	def addMeleeSpeed(self,value):
		self.stats.addMeleeSpeed(value)

#Shot recoil
	def getShotRecoil(self):
		return self.stats.getShootRecoil()

	def setShotRecoil(self,value = None):
		self.stats.setShootRecoil(value)

	def addShotRecoil(self,value):
		self.stats.addShootRecoil(value)

#Shoot recoil
	def getShootRecoil(self):
		return self.stats.getShootRecoil()

	def setShootRecoil(self,value = None):
		self.stats.setShootRecoil(value)

	def addShootRecoil(self,value):
		self.stats.addShootRecoil(value)


#Melee recoil
	def getMeleeRecoil(self):
		return self.stats.getMeleeRecoil()

	def setMeleeRecoil(self,value=None):
		self.stats.setMeleeRecoil(value)

	def addMeleeRecoil(self,value):
		self.stats.addMeleeRecoil(value)

	
#Hurt timer
	def getGhostModeTimer(self):
		return self.stats.getGhostModeTimer()

	def setGhostModeTimer(self,value):
		self.stats.setGhostModeTimer(value)

	def addGhostModeTimer(self,value):
		self.stats.addGhostModeTimer(value)


#Hurt timer max 
	def getMaxGhostModeTimer(self):
		return self.stats.getMaxGhostModeTimer()

	def setMaxGhostModeTimer(self,value):
		self.stats.setMaxGhostModeTimer(value)

	def addMaxGhostModeTimer(self,value):
		self.stats.addMaxGhostModeTimer(value)


#Ghost mode
	def getGhostMode(self):
		return self.stats.getGhostMode()
	def setGhostMode(self, value):
		self.stats.setGhostMode(value)

#meleeAttackDuration
	def getMeleeAttackDuration(self):
		return self.stats.getMeleeAttackDuration()

	def setMeleeAttackDuration(self, value):
		self.stats.setMeleeAttackDuration(value)
