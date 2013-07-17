'''
Created on 18/ago/2011

@author: koteko
'''

import os, pygame

from utility.config import parseConfigXML
from utility.characters.player import Player
from pygame.locals import MOUSEBUTTONDOWN

class State:
	"""Template Class -- for a state.

	Arguments:
		game -- The state engine.
		value -- I usually pass in a custom value to a state
	
	For all of the template methods, they should return None unless they return 
	a new State to switch the engine to.

	"""
	
	def __init__(self, game, value=None):
		self.game, self.value = game, value

	def init(self): 
		"""Template Method - Initialize the state, called once the first time a state is selected."""
		return

	def paint(self, screen): 
		"""Template Method - Paint the screen.  Called once after the state is selected.
		
		State is responsible for calling pygame.display.flip() or whatever.

		"""
		return
		
	def repaint(self): 
		"""Template Method - Request a repaint of this state."""
		self._paint = 1

	def update(self, screen):
		"""Template Method - Update the screen.
		
		State is responsible for calling pygame.display.update(updates) or whatever.

		"""
		return

	def loop(self):
		"""Template Method - Run a logic loop, called once per frame."""
		return

	def event(self, e):
		"""Template Method - Recieve an event."""
		return


class NormalNode(State):
	"""Template Class -- for a state.

	Arguments:
		game -- The state engine.
		value -- I usually pass in a custom value to a state
	
	For all of the template methods, they should return None unless they return 
	a new State to switch the engine to.

	"""
	
	def __init__(self, game, value, prevState=None):
		self.game, self.value, self.prevState = game, value, prevState

	def init(self):
		"""Template Method - Initialize the state, called once the first time a state is selected."""
		
		# loading config file
		playerConf, hotConf, zoneConf = parseConfigXML(self.value)
		
		bgPath = os.path.join('data', self.value, 'background', 'background.xpm')
		bgMaskPath = os.path.join('data', self.value, 'background', 'background_mask.xpm')
		
		# the visualized background
		self.origBg = pygame.image.load(bgPath)
		self.background = pygame.transform.scale(self.origBg, self.game.screen.get_size())
		
		self.bgW, self.bgH = self.background.get_size()
		
		# the mask for pathfinding and hotspots
		self.origBgMask = pygame.image.load(bgMaskPath)
		self.bgMask = pygame.transform.scale(self.origBgMask, self.game.screen.get_size())
		
		# it works only for 1920x1080!!!
		self.scaleRatio = 18
		self.smallBgMask = pygame.transform.scale(self.bgMask, (self.bgW / self.scaleRatio,
										self.bgH / self.scaleRatio))
		
		#self.scaleRatio = 0.6
		#self.smallBgMask = pygame.transform.rotozoom(self.bgMask, 0, self.scaleRatio)
		
		# loading player
		if self.prevState != None:
			oldHotspot = self.prevState.activeHotspot.rect

			if oldHotspot.topleft[0] == 0:
				# we come from east
				playerConf["side"] = "l"
				playerConf["start_position"] = [self.bgW - (oldHotspot.width + self.prevState.player.rect.width + 1), 
								self.prevState.player.rect.midbottom[1]]
			elif oldHotspot.topleft[1] == 0:
				# we come from south
				playerConf["side"] = self.prevState.player.side
				playerConf["start_position"] = [self.prevState.player.rect.midbottom[0], 
								self.bgH - (oldHotspot.height + 1)]
			elif oldHotspot.bottomright[0] == self.bgW:
				# we come from west
				playerConf["side"] = "r"
				playerConf["start_position"] = [oldHotspot.width + self.prevState.player.rect.width + 1, 
								self.prevState.player.rect.midbottom[1]]
			elif oldHotspot.bottomright[1] == self.bgH:
				# we come from north
				playerConf["side"] = self.prevState.player.side
				playerConf["start_position"] = [self.prevState.player.rect.midbottom[0], 
								oldHotspot.height + self.prevState.player.rect.height + 1]
			
		self.player = Player(playerConf)
				
		# loading hotspots
		self.hotspots = pygame.sprite.Group()
		
		for hs in hotConf:
			if hs[2] == "_":
				hs[2] = self.bgW - int(hs[0])
			if hs[3] == "_":
				hs[3] = self.bgH - int(hs[1])
			
			hotspot = pygame.sprite.Sprite()
			hotspot.rect = pygame.Rect(int(hs[0]), int(hs[1]), int(hs[2]), int(hs[3]))
			hotspot.toGo = hs[4]
			
			self.hotspots.add(hotspot)
		
		self.people = pygame.sprite.RenderUpdates(self.player)
		#self.allsprites = pygame.sprite.LayeredUpdates(self.player, self.hotspot)
		
		# a pixel map
		self.pixelMap = pygame.PixelArray(self.smallBgMask)
		
		return

	def paint(self, screen):
		"""Template Method - Paint the screen.  Called once after the state is selected.
		
		State is responsible for calling pygame.display.flip() or whatever.

		"""
				
		screen.blit(self.background, (0, 0))
		self.people.draw(screen)
		
		pygame.display.flip()
				
		return
	
	def repaint(self):
		"""Template Method - Request a repaint of this state."""
		
		self._paint = 1

	def update(self, screen):
		"""Template Method - Update the screen.
		
		State is responsible for calling pygame.display.update(updates) or whatever.

		"""
		
		self.people.clear(screen, self.background)
		
		#self.people.draw(screen)
		#pygame.display.flip()
		
		pygame.display.update(self.people.draw(screen))
		
		self.repaint()
		
		return

	def loop(self):
		"""Template Method - Run a logic loop, called once per frame."""
		
		self.people.update()
		
		newLevel = pygame.sprite.spritecollideany(self.player, self.hotspots)
		
		if newLevel == None:
			return
		else:
			self.activeHotspot = newLevel
			
			return NormalNode(self.game, newLevel.toGo.lower(), self)
		
	def event(self, e):
		"""Template Method - Receive an event."""
		
		if e.type == MOUSEBUTTONDOWN:
			self.player.walkTo(pygame.mouse.get_pos(), self.pixelMap, self.scaleRatio)
		return

class Quit(State):
	"""A state to quit the state engine."""
	
	def init(self): 
		self.game.quit = 1
