# -*- coding: utf-8 -*-
import pygame
from ..resources.gestorRecursos import *
from ..resources.constants import *
from graphics import *

class HPCounterGraphics(Graphics):
	def __init__(self, actor, color):
		font = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
		self.actor = actor
		self.color = color
		self.actor.image = font.render(str(self.actor.stats.getActualHP()), True, color)
		self.actor.rect = self.actor.image.get_rect()

	def updateAnimation(self):
		self.actor.image = font.render(str(self.actor.stats.getActualHP()), True, color)

