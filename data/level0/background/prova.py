import os, pygame

bgpath = os.path.join('map_big_1.xpm')

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
		
orig_background = pygame.image.load(bgpath)
		
background = pygame.transform.scale(orig_background, screen.get_size())
	
bgW, bgH = background.get_size()
	
scaleRatio = 18
smallBackground = pygame.transform.scale(background, (bgW / scaleRatio, bgH / scaleRatio))

print pygame.PixelArray(smallBackground)

pygame.quit()


