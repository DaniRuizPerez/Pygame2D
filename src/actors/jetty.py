from enemy import *
from ..engines.stats import *
from ..engines.graphics import *
from jettyState import *


class Jetty(Enemy):
    #Just a simple implementation. Actor and Drin have more info
    def __init__(self, stage):
        Enemy.__init__(self, stage)

    def setStats(self):

        multiplierSimple = float(self.stage.getLevel())/10
        multiplierDouble = float(self.stage.getLevel())/5
        #           (          maxHP,              damage,          speed,      jumpSpeed,         shotSpeed,      shootSpeed,       meleeSpeed, meleeAttackDuration)
        return Stats(1000*multiplierDouble,0*25*multiplierDouble,0.2*multiplierDouble,0.35,0.3*multiplierDouble,20/multiplierDouble,         0,         0)

    def setGraphics(self):
        return Graphics(self, 'jettySprites.gif' , 'coordJetty.txt', 5)

    def setInitialState(self):
        return JettyInit(self)
