# -*- coding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *
from ..game_logic.escena import *
from ..engines.state import *
from playerState import *
from ..engines.stats import *
from ..engines.graphics import *
from actor import *

KEY_CODE = [K_UP, K_DOWN, K_LEFT, K_RIGHT,K_z, K_x] #Default inputs are z to melee attack, x to shot and up to jump

'''Drin is the playable actor. Some methods has little changes to reflect this'''

class DRIN(Actor):
    def __init__(self, stage):
        '''Actor constructor MUST be called AFTER keys settings, because playerState needs keys and keyCode to 
       	be created (Actor constructor calls self.setInitialState())'''
        self.keys = None
        self.keyCode = KEY_CODE
        Actor.__init__(self, stage)

    def setStage (self, stage):
        self.stage = stage

    def getStage (self):
        return self.stage

    def setKeys(self, pressedKeys):
    	'''Each frame, this method will be called, so DRIN has always the keys player pressed'''
        self.keys = pressedKeys

    def setKeyCode(self,keyCode):
    	'''keyCode can "decipher" key setted by the previous method'''
        self.keyCode = keyCode

    def getActualHP (self):
        return self.stats.getActualHP()

    def completlyHeal(self):
        self.stats.completlyHeal()

    def setStats(self):
    	'''Different DRIN models may have different stats'''
        #           (maxHP, damage, speed, jumpSpeed, shotSpeed,shootSpeed, meleeSpeed, meleeAttackDuration)
        return Stats(100  , 25   ,   0.3,       0.35,         1,   30,         10,         15)

    def setGraphics(self):
    	'''Default image, coords file and animation cooldown'''
        return Graphics(self, 'drinSprites.gif' , 'coordDrin.txt', 5)

    def setInitialState(self):
    	'''playerState.py has more information. Promised'''
        return PlayerInit(self)

    def hurt(self, amount):
    	'''Hurt calls an awesome method which allows ghost mode'''
        Actor.hurt(self, amount)
        self.timeToBeInvencibleBecauseIHaveBeenHurt()

    def checkDeath(self):
    	'''If Drin dies, gameOver is activated'''
        HP = self.stats.getActualHP()
        if  HP <= 0 and HP != None:
            self.stage.gameOver()
       
    def timeToBeInvencibleBecauseIHaveBeenHurt(self):
        #Short name, short method
        self.state.activateGhostMode(True)
