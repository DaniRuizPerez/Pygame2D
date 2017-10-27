# -*- coding: utf-8 -*-

'''State is an adapted implementation of the state pattern, called state-decisor.

Each actor behaviour is modeled like an automaton. Each concrete state class is one of the
nodes of the graph, and defines one action (for example, "moving", or "jumping").

To iterate through the graph/automaton, states will ask Decisor. Decisor is the "controller",
the class which knows all edges. When state summons self.askDecisor method, Decisor.newState is
called, and it will choose between 2 posibilities: don't change anything (so actor.state = decisor.state), or
to create a new state (so actor.state = new state). New states in the same automaton will have the same
Decisor

So to sum up:
	Actor: has a state
	State: has a decisor
	Decisor: can change actor.state to the same state, or to a new one

Actor will call state.action(self.stage) each frame. Then, in State.action method,
Decisor.newState is called

By convention, initial state must be called actornameInit'''

class State():
	'''Check example implementations for more info'''
	def __init__(self, actor, decisor = None):
		'''We want state to know his actor and decisor'''
		self.actor = actor
		if decisor == None: #If decisor is None, we will use the default one
			self.decisor = Decisor(self)
		else:
			self.decisor = decisor

	def action(self, fase):
		'''Action is called every frame'''
		self.decisor.prolog(fase) #Fixed actions all states must execute in the same graph
		self.actor.state = self.askDecisor(fase) #Can fix a new state,

	def askDecisor(self, fase):
		return self.decisor.newState(fase)

	def register(self, stage):
		'''This method can add programatically-created actors to stage groups'''


class Decisor():
	'''Decisor is the class all controllers must extend. Also, offers
	a pretty simple implementation for a simple automaton'''
	def __init__(self, state):
		self.state = state

	def newState(self, fase):
		#Default decisor considers single-state graphs
		#IA and player input should be managed there
		return self.state 

	def prolog(self,fase):
		'''Extend this and insert there all actions that all states should execute'''

	def getActor(self):
		#Well... this is shorter than self.state.actor :D
		return self.state.actor

