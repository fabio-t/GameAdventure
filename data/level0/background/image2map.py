import pygame, os

from pygame.locals import *

pygame.init()

bgpath = os.path.join('map_big_1_hot.xpm')

background = pygame.image.load(bgpath)

bgSize = (bgW, bgH) = background.get_size()

array = pygame.PixelArray(background)

# l'array e' una lista di bgW liste, ognuna delle quali ha bgH elementi, che sono pixel

i = 0
while i < bgW:
	j = 0
	while j < bgH:
#		if array[i][j] == background.map_rgb((0,0,0)):
#			print "nero: " + str(i) + " " + str(j) + ", color = " + str(array[i][j])
		print array[i][j]
		j = j + 1
	i = i + 1

pygame.quit()

