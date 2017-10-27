# -*- coding: utf-8 -*-
import pygame
from ..engines.state import *
from playerState import *
from ..resources.gestorRecursos import *
from ..engines.physics import *
from ..engines.stats import *
from ..resources.constants import *
from ..engines.graphics import *
from ..engines.upgrades.upgrade import *
from ..engines.upgrades.upgradeCollection import *
from ..engines.textGraphics import *


'''Actor is one of the main classes of this project. All platforms, attacks, npcs and players are subclasses of Actor

Actor abstract class extends pygame.sprite.Sprite, so it has rect and image as main attributes by inheritance.

Also, it has 4 "engines", or main attributes. They define actor's behaviour, appeareance, controller...

Stats: ingame attributes, like HP or Attack (more info at engines/stats)
Graphics: how it looks. Self.graphics modifies self.image (engines/grahics)
Physics: how it moves. Self.physics modifes self.rect (engines/physics)
State: actor's behaviour. Depending on orders (via IA or player input), each actor will
iterate by different states. State interface is defined in engines/states, and each state implementation
can be found in actors folder

Also, each actor has a reference to the stage it's at

'''

class Actor(pygame.sprite.Sprite):
    def __init__(self, stage):
    	'''Main attributes are assigned with methods, so a subclass can override them to change defaults.
    	All of them must be defined somewhere in the inheritance tree, or actor will crash when calling
    	this constructor
    	'''
        pygame.sprite.Sprite.__init__(self)
        self.stage = stage
        self.stats = self.setStats()
        self.graphics = self.setGraphics()
        self.physics = self.setPhysics()
        self.state = self.setInitialState()

    def update(self, stage):
    	'''Update is called each frame. This method has 4 tasks:
    		- Check if actor died
    		- Update the state (iterate over the state machine that defines actor behaviour)
    		- Update graphics (change to another animation, or show next frame of the current one)
    		- Update phisics (move actor's rect over the screen)
    	'''
    	#
        self.checkDeath()     
        #Calculate new actions actor will perform
        self.state.action(stage)
        #Update graphics
        self.graphics.updateAnimation()
        #Update physics
        self.physics.updateMovement()

    def setStats(self):
        '''By default, HP to None, in order to make platforms immune'''
        return Stats(None, 0, 0, 0, 0, 0, 0, 0)

    def setGraphics(self):
        '''This constructor creates an empty surface'''
        return Graphics(self)

    def setPhysics(self):
    	'''By default, all sprites will start being idleing at absolute position (0,0),
    	with (0,0) scroll'''
        return Physics((0,0), (0,0), (0,0), self)

    def setUpgrade(self, upgrade):
        oldStats = self.stats
        self.stats = upgrade
        self.stats.setStats(oldStats)

    def checkDeath(self):
    	'''By default, only checks if actor HP is 0 or lower. When this condition is true,
    	actor is killed, and drop function is called.'''
        HP = self.stats.getActualHP()
        if  HP <= 0 and HP != None:
            self.drop()
            self.kill()
            self.remove()

    def hurt(self, amount):
    	'''I warned you not to touch the edge of my sword'''
        self.stats.addActualHP(-amount)

    def drop(self):
        '''This function must be overriden by each enemy, in order to create a drop system.
        Drops are all items enemys "drop" when they die. They should create a new/s actor/s
        in the same position as this actor. 

        By default, this method has no implementation'''

    def ghostMode(self, value):
        '''Some actors (player, some enemies) can't be hurted twice in a short time. When they
        take damage, "ghost mode" is activated. While in ghost mode, actor's sprite will blink,
        and he's inmune to collisions. 

        This method has no implementation, so ghost mode is not activated by default'''

