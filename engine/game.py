'''
Created on 18/ago/2011

@author: koteko
'''

import pygame

from pygame.locals import QUIT, K_ESCAPE, KEYDOWN 
from engine.state import Quit

class Game:
	"""Template Class - The state engine."""

	def fnc(self, f, v=None):
		s = self.state
		
		if not hasattr(s, f):
			return 0
		
		f = getattr(s, f)
		
		if v != None:
			r = f(v)
		
		else:
			r = f()
		
		if r != None:
			self.state = r
			self.state._paint = 1
			
			return 1
		
		return 0
		
	def run(self, state, screen=None):
		"""Run the state engine, this is a infinite loop (until a quit occurs).
		
		Arguments:
			state -- the initial state
			screen -- the screen

		"""
		self.quit = 0
		self.state = state
		
		if screen != None:
			self.screen = screen
		
		self.init()
		
		while not self.quit:
			self.loop()

	def loop(self):
		s = self.state
		
		if not hasattr(s, '_init') or s._init:
			s._init = 0
			
			if self.fnc('init'):
				return
		else: 
			if self.fnc('loop'):
				return
		
		if not hasattr(s, '_paint') or s._paint:
			s._paint = 0
			
			if self.fnc('paint', self.screen):
				return
		else: 
			if self.fnc('update', self.screen):
				return
		
		for e in pygame.event.get():
			#NOTE: this might break API?
			#if self.event(e): return
			if not self.event(e):
				if self.fnc('event', e):
					return
		
		self.tick()
		
		return
			
	def init(self):
		"""Template Method - called at the beginning of State.run() to initialize things."""
		
		return
		
	def tick(self):
		"""Template Method - called once per frame, usually for timer purposes."""
		pygame.time.wait(100)
	
	def event(self, e):
		"""Template Method - called with each event, so the engine can capture special events.
		
		Return a True value if the event is captured and does not need to be passed onto the current
		state

		"""
		if e.type is QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): 
			self.state = Quit(self, None)
			
			return 1
