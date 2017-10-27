from enemy import *
from ..engines.stats import *
from ..engines.graphics import *
from penguinState import *


class Penguin(Enemy):
    #Just a simple implementation. Actor and Drin have more info
    def __init__(self, stage):
        Enemy.__init__(self, stage)

    def setStats(self):

        multiplierSimple = float(self.stage.getLevel())/10
        multiplierDouble = float(self.stage.getLevel())/5
        #           (          maxHP,              damage,          speed,           jumpSpeed,   shotSpeed   shootSpeed,     meleeSpeed,     meleeAttackDuration)
        return Stats(100*multiplierDouble,25*multiplierDouble,0.2*multiplierDouble,       0.35,      0,        0,        10*multiplierDouble,     15)

    def setGraphics(self):
        return Graphics(self, 'penguinSprites.gif' , 'coordPenguin.txt', 5)

    def setInitialState(self):
        return PenguinInit(self)
