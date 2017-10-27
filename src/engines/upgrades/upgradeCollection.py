# -*- coding: utf-8 -*-
from ..stats import *
from upgrade import *

class HPUpgrade(Upgrade):
	def __init__(self, stats,hpIncrement):
		self.stats = stats
		self.setMaxHP(hpIncrement)
	def getMaxHP(self):
		return self.stats.getMaxHP() + self.getMaxHP()