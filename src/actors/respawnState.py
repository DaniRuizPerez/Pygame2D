# -*- coding: utf-8 -*-
from ..engines.state import *
from ..resources.constants import *

'''NOTE: Before reading this, read state documentation and/or incode comments'''

'''This simple platform has only the Init state, so it can use the default implementation
of Decisor. All actors that use default physics have, by default, his speed set to (0,0),
so an static platform just need to stay as it is.

Moving platforms may have different states, or movement patterns. That would need a Decisor,
and states to navigate'''

class RespawnState(State):
	def __init__(self, actor, decisor = None):
		State.__init__(self, actor, Decisor(self))
		self.register(self.actor.stage)

'''STATES'''
class SimpleRespawnInit(RespawnState):
	def __init__(self, actor):
		RespawnState.__init__(self, actor)