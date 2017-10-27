import actor
from ..engines.stats import *
from ..engines.graphics import *
from simpleEnemyState import *

class Enemy(actor.Actor):
    '''Enemies have this simple class to inherit, so future methods can be applied to Enemy abstract class'''
    def __init__(self, stage):
        self.image = pygame.Surface((0,0))
        actor.Actor.__init__(self, stage)
        self.enemyType = self.__class__.__name__.lower()
        if stage.hdModeActivated():
            self.graphics =  self.setHdGraphics()

    def checkDeath(self):
        '''By default, only checks if actor HP is 0 or lower. When this condition is true,
        actor is killed, and drop function is called.'''
        HP = self.stats.getActualHP()
        if  HP <= 0 and HP != None or self.physics.position[1] > 2000:
            self.stage.enemyKilled(self.enemyType)
            self.drop()
            self.kill()
            self.remove()

    def setHdGraphics(self):
        return Graphics(self, 'hd.png')


