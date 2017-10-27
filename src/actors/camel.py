from enemy import *
from ..engines.stats import *
from ..engines.graphics import *
from camelState import *


class Camel(Enemy):
    #Just a simple implementation. Actor and Drin have more info
    def __init__(self, stage):
        Enemy.__init__(self, stage)

    def setStats(self):

        multiplierSimple = float(self.stage.getLevel())/10
        multiplierDouble = float(self.stage.getLevel())/5
        #           (          maxHP,              damage,          speed,      jumpSpeed,         shotSpeed,      shootSpeed,       meleeSpeed, meleeAttackDuration)
        return Stats(1000*multiplierDouble,25*multiplierDouble,1*multiplierDouble,0.35,0.5*multiplierDouble,30/multiplierDouble,         0,         0)

    def setGraphics(self):
        return Graphics(self, 'weedelSprites.gif' , 'coordWeedel.txt', 5)

    def setInitialState(self):
        return CamelInit(self)
