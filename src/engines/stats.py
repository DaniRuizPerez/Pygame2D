class Stats():
	def __init__(self,maxHP, damage, speed, jumpSpeed, shotSpeed, shootSpeed, meleeSpeed, meleeAttackDuration):
		self.maxHP = maxHP
		self.actualHP = maxHP
		self.damage = damage
		self.maxSpeed = speed
		self.maxJumpSpeed = jumpSpeed
		self.shotSpeed = shotSpeed
		self.shootSpeed = shootSpeed
		self.meleeSpeed = meleeSpeed
		self.meleeAttackDuration = meleeAttackDuration
		self.maxGhostModeTimer = 100

		#Counter
		self.shootRecoil = 0
		self.meleeRecoil = 0
		self.ghostModeTimer = 0
		self.ghostMode = False	
	
#Restaurar salud total
	def completlyHeal(self):
		self.actualHP = self.maxHP

#MaxHP
	def getMaxHP(self):
		return self.maxHP

	def setMaxHP(self,value):
		self.maxHP = value

	def addMaxHP(self,value):
		self.maxHP += value

#ActualHP
	def getActualHP(self):
		return self.actualHP

	def setActualHP(self,value):
		self.actualHP = value

	def addActualHP(self,value):
		self.actualHP += value

#Damage
	def getDamage(self):
		return self.damage

	def setDamage(self,value):
		self.damage = value

	def addDamage(self,value):
		self.damage += value

#MaxSpeed
	def getMaxRunSpeed(self):
		return self.maxSpeed

	def setMaxRunSpeed(self,value):
		self.maxSpeed = value

	def addMaxRunSpeed(self,value):
		self.maxSpeed += value

#MaxJumpSpeed
	def getMaxJumpSpeed(self):
		return self.maxJumpSpeed

	def setMaxJumpSpeed(self,value):
		self.maxJumpSpeed = value

	def addMaxJumpSpeed(self,value):
		self.maxJumpSpeed += value

#Melee Speed
	def getMeleeSpeed(self):
		return self.meleeSpeed

	def setMeleeSpeed(self,value):
		self.meleeSpeed = value

	def addMeleeSpeed(self,value):
		self.meleeSpeed += value

#Shot Speed
	def getShotSpeed(self):
		return self.shotSpeed

	def setShotSpeed(self,value):
		self.shotSpeed = value

	def addShotSpeed(self,value):
		self.shotSpeed += value

#Shoot recoil
	def getShootRecoil(self):
		return self.shootRecoil 
	def setShootRecoil(self, value = None):
		if value == None:
			self.shootRecoil = self.shootSpeed
		else:
			self.shootRecoil = value
	def addShootRecoil(self, value):
		self.shootRecoil += value

#Melee recoil
	def getMeleeRecoil(self):
		return self.meleeRecoil 
	def setMeleeRecoil(self, value = None):
		if value == None:
			self.meleeRecoil = self.meleeSpeed
		else:
			self.meleeRecoil = value
	def addMeleeRecoil(self, value):
		self.meleeRecoil += value
	
#Hurt timer
	def getGhostModeTimer(self):
		return self.ghostModeTimer
	def setGhostModeTimer(self, value):
		self.ghostModeTimer = value
	def addGhostModeTimer(self, value):
		self.ghostModeTimer += value

#Hurt timer max 
	def getMaxGhostModeTimer(self):
		return self.maxGhostModeTimer
	def setMaxGhostModeTimer(self, value):
		self.maxGhostModeTimer = value
	def addMaxGhostModeTimer(self, value):
		self.maxGhostModeTimer += value

#Ghost mode
	def getGhostMode(self):
		return self.ghostMode
	def setGhostMode(self, value):
		self.ghostMode = value

#meleeAttackDuration
	def getMeleeAttackDuration(self):
		return self.meleeAttackDuration

	def setMeleeAttackDuration(self, value):
		self.meleeAttackDuration = value
