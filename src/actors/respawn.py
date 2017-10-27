from actor import *
from respawnState import *
from random import randint


class Respawn(Actor):
	def __init__(self, large, stage):
	 	Actor.__init__(self, stage)
	 	self.large = large
	 	self.enemies= {}	# (mq, q, ma, a, mw, w) => (maximoEnemigos, enemigosQueQuedan, maximosActivosALaVez, activosAhoraMismo, minimoAEsperarEntreRespawn, tiempoDesdeUltimoRespawn)

	def add(self, enemyType, quantity, maxActive, minWait):
	 	self.enemies[enemyType] = (quantity, quantity, maxActive, 0, minWait * 60, 0)

	def enemyKilled(self, enemyType):
	 	if enemyType in self.enemies:
	 		(mq, q, ma, a, mw, w) = self.enemies[enemyType]
	 		self.enemies[enemyType] = (mq, q, ma, a-1, mw, w)

	def createEnemy(self, enemyType):
	 	x = (randint(1, 3) * (self.large - 100) / 3) + 50
	 	y = (randint(1, 2) * (ALTO_PANTALLA - 100)/ 3) + 25
	 	pos = (x, y)

	 	self.stage.createEnemy(enemyType, pos)

	def updateEnemies (self):
	 	for t, (mq, q, ma, a, mw, w) in self.enemies.iteritems():
	 		if w == 0:
	 			if q > 0 and a < ma:
	 				self.createEnemy(t)
	 				self.enemies[t] = (mq, q-1, ma, a+1, mw, mw)
	 		else:
	 			self.enemies[t] = (mq, q, ma, a, mw, w - 1)

	def enemiesRemaining(self):
	 	result = 0
	 	for t, (mq, q, ma, a, mw, w) in self.enemies.iteritems():
	 		result = result + q + a
	 	return result

	def setInitialState(self):
 		'''Simple or sample?'''
   		return SimpleRespawnInit(self)
