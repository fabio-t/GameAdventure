import pygame

from engine.game import Game
from engine.state import NormalNode

if __name__ == '__main__':
	pygame.init()

	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
	#screen = pygame.display.set_mode((0, 0))
	
	pygame.display.set_caption('Game Adventure')
	
	game = Game()
	
	game.run(NormalNode(game, "level0"), screen)
	
	pygame.quit()
