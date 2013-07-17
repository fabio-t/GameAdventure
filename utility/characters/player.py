'''
Created on 13/ago/2011

@author: koteko
'''

import pygame
import os

from pygame.locals import *

from utility.pathfinding import aStar

class Player(pygame.sprite.Sprite):
	'''
	Class -- The Player

	Arguments:
		playerConf -- a list with parameters
			
	This class handles the Player and inherit from Sprite

	'''

	def __init__(self, playerConf):
		
		pygame.sprite.Sprite.__init__(self)

		self.side = playerConf["side"]
		self.scaleRatio = float(playerConf["ratio"])
		
		self.step = 0
		self.stop = True
		
		self.toMove = []
		self.images = {}
			
		for s in ["l", "r"]:
			for ss in range(0, 5):			
				fullname = os.path.join('data', 'player_normal', "%s%d.png" % (s, ss))

				try:
					self.image = pygame.image.load(fullname)
					
					self.image = pygame.transform.rotozoom(self.image, 0, self.scaleRatio)
				
					if self.image.get_alpha() is None:
						self.image = self.image.convert()
					else:
						self.image = self.image.convert_alpha()
				except pygame.error, message:
					print 'Cannot load image: ', fullname
				
					raise SystemExit, message
					
				self.images[s + str(ss)] = self.image
				
		# default position of the character
		
		self.image = self.images[self.side + str(self.step)];
		self.rect = self.image.get_rect()
		
		self.rect.move_ip(	int(playerConf["start_position"][0]) - (self.rect.width / 2), 
					int(playerConf["start_position"][1]) - self.rect.height)

	def _walk(self):
		oldX, oldY = self.rect.midbottom
		newX, newY = self.toMove.pop()
		
		offX = newX - oldX
		offY = newY - oldY
		
		# no movement
		if offX == 0 and offY == 0:
			self.stop = True
			self.step = 0

			return
		
		# horizontal movement
		if offX > 0:
			self.side = "r"
		elif offX < 0:
			self.side = "l"
		
		# we have four position of the legs, plus the "stand" position, 0.
		if self.step == 4:
			self.step = 1
		else:
			self.step = self.step + 1
		
		# this has been the last step
		if len(self.toMove) == 0:
			self.stop = True
			self.step = 0

		self.image = self.images[self.side + str(self.step)]
		self.rect.move_ip(offX, offY)

	def walkTo(self, newXY, pixelMap, scaleRatio):
		del(self.toMove)

		self.toMove = aStar(scaleRatio, self.rect.midbottom, newXY, pixelMap)
		
		if len(self.toMove) > 1:
			self.stop = False
			
		else:
			self.stop = True
			
			return

	def update(self):
		if not self.stop:
			self._walk()
		
