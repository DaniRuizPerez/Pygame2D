from ..actors.platform import *

class Trap(Platform):
    def __init__(self, x, y, image, stage):
    	rect = (x, y-15, 50, 15)
        Platform.__init__(self, rect, image, stage)
        self.stats = Stats(None, 30, 0, 0, 0, 0, 0, 0)

	def setStats(self):
		return Stats(None, 30, 0, 0, 0, 0, 0, 0)

    def setGraphics(self):
        return Graphics(self, self.imageFile, colorKey = -1)