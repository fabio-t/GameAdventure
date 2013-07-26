GameAdventure
=============

A small proof of concept from many years ago, where I played a bit with Python and Pygame.

I will get back to it one day.

Anyway, at this point it features a 2D background image with the possibility to draw "walls" the character will avoid.

When you click with the mouse at one point on the screen, the character sprite "moves" (I have a few sprites for different body positions which in sequence give the impression of movement). A pathfinding algorithm takes care of finding the shortest way while avoiding obstacles.

When I get back to it, there are a few unfinished things I had started and I'm going to take care of:

* "level" switching (when you touch the border of the current scene, which is as big as the screen, if there is an hotspot you are moved of scene)
* using "mask" background image for hotspots, while showing a nice, normal image during the game (it needed a bugfix I think)
* change in size of the character when going "further", like in Monkey Island, to give impression of depth
