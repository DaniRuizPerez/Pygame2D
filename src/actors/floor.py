from ..actors.platform import *

class Floor(Platform):
    def __init__(self, begin, length, fill, image, stage):
    	if (fill):
    		rect = (begin, 565, length, 35)
    	else:
    		rect = (begin, 550, length, 15)
        Platform.__init__(self, rect, image, stage)