from actor import *
from ..engines.graphics import *
from ..engines.stats import *
from platformState import *

'''Platform is defined as an actor. This is a simple, static platform implementation, without graphics'''

class Platform(Actor):
    def __init__(self, (x, y, l, h), img, stage):
        self.imageFile = img
        Actor.__init__(self, stage)
        # Rect is a parameter, and Actor constructor makes scroll 0, so positions are absolute
        self.rect = pygame.Rect ((x, y, l, h))
        self.physics.fixPosition((self.rect.left, self.rect.bottom))
        if img != None:
            self.image = pygame.transform.scale(self.image, (l, h))


    #Stats, graphics and physics has default behaviour

    def setInitialState(self):
    	'''Simple or sample?'''
        return SimplePlatformInit(self)

    def setStats(self):
        return Stats(None, 0, 0, 0, 0, 0, 0, 0)

    def setGraphics(self):
        return Graphics(self, self.imageFile, colorKey = None)