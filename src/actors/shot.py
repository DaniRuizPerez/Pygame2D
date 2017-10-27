import actor
from ..engines.physics import *
from ..engines.graphics import *
from ..engines.stats import *
from shotState import *
from drinShotMoving import *

'''Shot are a simple actors that can move and collide. By default, each shot has 
the attack of his creator, and their movement speed is defined by creator.stats.shotSpeed

Melee attacks are defined by a shot type whose position is "attached" to creator's position
Also, when colliding, melee attacks won't be destroyed'''

class Shot(actor.Actor):
    def __init__(self, image, coord, scroll, shotSpeed, dir, stage, damage):
        actor.Actor.__init__(self, stage)
        '''At this point, we have all attributes intialized, so we will configure them'''
        self.graphics.direction = dir #same direction as creator has
        self.graphics.changeImage(image) #own graphics
        self.physics.setScroll(scroll) #same scroll as creator has
        self.physics.fixPosition(coord) #position is relative to creator's (depends on each type of shot)
        self.stats.setDamage(damage) #same damage as creator
        self.physics.speed = shotSpeed #initial speed. May change depending on each shot class

    #def setPhysics(self): #We needn't it, as we inherit Actor.setPhysics()
        #return Physics((0,0), (0,0), (0,0), self)

class MeleeShot(Shot):
	#Melee attacks are modeled as shots that are attached to their creator. Initial position and speed is given by the constructor, but the "sticky"
    #functionality is fixed by ShotAttached states
    def __init__(self, actor):
        self.creator = actor
        Shot.__init__(self, 'melee.png', actor.physics.position, actor.physics.scroll, (0,0), actor.graphics.direction, actor.stage, actor.stats.getDamage())
    def setInitialState(self):
        return ShotAttachedInit(self)
        
class RangedShot(Shot):
	#A simple shot. It can be varied by inheritance
    def __init__(self, actor, stage, direction = None):
        if (direction == None):
            shotDir = actor.graphics.direction
            shotSpeed = (actor.graphics.direction* actor.stats.getShotSpeed(),0)
        else:
            shotDir = direction[0]
            shotSpeed = (direction[0] * actor.stats.getShotSpeed(), direction[1] * actor.stats.getShotSpeed())
        Shot.__init__(self, 'disparo.png', actor.physics.position, actor.physics.scroll, shotSpeed, shotDir, stage, actor.stats.getDamage())
    def setInitialState(self):
        return ShotMovingInit(self)

class DrinRangedShot(Shot):
    #A simple shot. It can be varied by inheritance
    def __init__(self, actor, stage):
        shotDir = actor.graphics.direction
        shotSpeed = (actor.graphics.direction* actor.stats.getShotSpeed(),0)
        Shot.__init__(self, 'disparo.png', actor.physics.position, actor.physics.scroll, shotSpeed, shotDir, stage, actor.stats.getDamage())
        self.physics.position = (self.physics.position[0]+12, self.physics.position[1]-21)
        
    def setGraphics(self):
        '''Default image, coords file and animation cooldown'''
        return Graphics(self, 'drinSprites.gif' , 'coordLaser.txt', 5)

    def setInitialState(self):
        return DrinShotMovingInit(self)

class DrinMeleeShot(Shot):
    def __init__(self, actor):
        self.creator = actor
        Shot.__init__(self, 'melee.png', actor.physics.position, actor.physics.scroll, (0,0), actor.graphics.direction, actor.stage, actor.stats.getDamage())
    def setInitialState(self):
        return ShotAttachedInit(self)


class CactusRangedShot(Shot):
    #A simple shot. It can be varied by inheritance 
    def __init__(self, actor, stage):
        shotDir = actor.graphics.direction
        shotSpeed = (actor.graphics.direction* actor.stats.getShotSpeed(),0)
        Shot.__init__(self, 'disparo.png', actor.physics.position, actor.physics.scroll, shotSpeed, shotDir, stage, actor.stats.getDamage())
        self.physics.position = (self.physics.position[0]+12, self.physics.position[1]-5)
        
    def setGraphics(self):
        '''Default image, coords file and animation cooldown'''
        return Graphics(self, 'cactusSprites.gif' , 'coordCactusShot.txt', 5)

    def setInitialState(self):
        return ShotMovingInit(self)


class SnowmanRangedShot(Shot):
    #A simple shot. It can be varied by inheritance
    def __init__(self, actor, stage, direction = None):
        if (direction == None):
            shotDir = actor.graphics.direction
            shotSpeed = (actor.graphics.direction* actor.stats.getShotSpeed(),0)
        else:
            shotDir = direction[0]
            shotSpeed = (direction[0] * actor.stats.getShotSpeed(), direction[1] * actor.stats.getShotSpeed())
        Shot.__init__(self, 'melee.png', actor.physics.position, actor.physics.scroll, shotSpeed, shotDir, stage, actor.stats.getDamage())
        self.physics.position = (self.physics.position[0]+12, self.physics.position[1]-20)
        self.graphics = Graphics(self, 'snowmanSprites.gif' , 'coordSnowmanShot.txt', 5)
    def setGraphics(self):
        '''Default image, coords file and animation cooldown'''
        return Graphics(self, 'snowmanSprites.gif' , 'coordSnowmanShot.txt', 5)

    def setInitialState(self):
        return ShotMovingInit(self)

class JettyRangedShot(Shot):
    def __init__(self, actor, stage, direction = None):
        if (direction == None):
            shotDir = actor.graphics.direction
            shotSpeed = (actor.graphics.direction* actor.stats.getShotSpeed(),0)
        else:
            shotDir = direction[0]
            shotSpeed = (direction[0] * actor.stats.getShotSpeed(), direction[1] * actor.stats.getShotSpeed())
        Shot.__init__(self, 'disparo.png', actor.physics.position, actor.physics.scroll, shotSpeed, shotDir, stage, actor.stats.getDamage())
        self.graphics = Graphics(self, 'jettySprites.gif' , 'coordJettyShot.txt', 5)
    def setGraphics(self):
        '''Default image, coords file and animation cooldown'''
        return Graphics(self, 'jettySprites.gif' , 'coordJettyShot.txt', 5)

    def setInitialState(self):
        return DrinShotMovingInit(self)

class CamelRangedShot(Shot):
    #A simple shot. It can be varied by inheritance
    def __init__(self, actor, stage, direction = None):
        if (direction == None):
            shotDir = actor.graphics.direction
            shotSpeed = (actor.graphics.direction* actor.stats.getShotSpeed(),0)
        else:
            shotDir = direction[0]
            shotSpeed = (direction[0] * actor.stats.getShotSpeed(), direction[1] * actor.stats.getShotSpeed())
        Shot.__init__(self, 'disparo.png', actor.physics.position, actor.physics.scroll, shotSpeed, shotDir, stage, actor.stats.getDamage())
        self.physics.position = (self.physics.position[0]+12, self.physics.position[1]-20)
        self.graphics = Graphics(self, 'weedelSprites.gif' , 'coordWeedelShot.txt', 5)
    def setGraphics(self):
        '''Default image, coords file and animation cooldown'''
        return Graphics(self, 'weedelSprites.gif' , 'coordWeedelShot.txt', 5)

    def setInitialState(self):
        return DrinShotMovingInit(self)
