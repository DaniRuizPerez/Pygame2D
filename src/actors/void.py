from ..actors.platform import *

class Void(Platform):
    def __init__(self, length, stage):
    	rect = pygame.Rect(0, ALTO_PANTALLA + 60, length, 200)
        Platform.__init__(self, rect, None, stage)

  	self.stats = Stats(None, sys.maxint, 0, 0, 0, 0, 0, 0)

	def setStats(self):
		return Stats(None, sys.maxint, 0, 0, 0, 0, 0, 0)