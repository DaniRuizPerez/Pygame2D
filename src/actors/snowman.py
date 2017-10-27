from enemy import *
from ..engines.stats import *
from ..engines.graphics import *
from snowmanState import *


class Snowman(Enemy):
    #Just a simple implementation. Actor and Drin have more info
    def __init__(self, stage):
        Enemy.__init__(self, stage)

    def setStats(self):
        multiplierSimple = float(self.stage.getLevel())/10
        multiplierDouble = float(self.stage.getLevel())/5
        #           (          maxHP,              damage,          speed,      jumpSpeed,         shotSpeed,      shootSpeed,       meleeSpeed, meleeAttackDuration)
        return Stats(100*multiplierDouble,25*multiplierDouble,0.2*multiplierDouble,0.35,0.5*multiplierDouble,30/multiplierDouble,         0,         0)

    def setGraphics(self):
        return Graphics(self, 'snowmanSprites.gif' , 'coordSnowman.txt', 5)

    def setInitialState(self):
        return SnowmanInit(self)
