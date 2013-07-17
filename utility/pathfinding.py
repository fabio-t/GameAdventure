'''
Created on 13/ago/2011

@author: PGU
'''

# The manhattan distance metric
def manhattanDistance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])
	
class node:
	def __init__(self, prev, pos, dest, dist):
		self.prev, self.pos, self.dest = prev, pos, dest
		
		if self.prev == None:
			self.g = 0
		else:
			self.g = self.prev.g + 1
		
		self.h = dist(pos, dest)
		self.f = self.g + self.h


def aStar(ratio, start, end, layer, dist=manhattanDistance):
	"""Uses the a* algorithm to find a path, and returns a list of positions 
	from start to end.

	Arguments:
		start -- start position
		end -- end position
		layer -- a grid where zero cells are open and non-zero cells are walls
		dist -- a distance function dist(a,b) - manhattan distance is used 
			by default
		step -- 1 means every point found is put in the path, 2 means that 1 point is put in the path, 1 not, etc.
	
	"""
	
	x, y = start
	
	x = x / ratio
	y = y / ratio
	
	start = (x, y)
	
	x, y = end
	
	x = x / ratio
	y = y / ratio
	
	end = (x, y)
	
	h, w = len(layer[0]), len(layer)
	
	if start[0] < 0 or start[1] < 0 or start[0] >= w or start[1] >= h: 
		return [] #start outside of layer
	if end[0] < 0 or end[1] < 0 or end[0] >= w or end[1] >= h:
		return [] #end outside of layer

	if layer[start[0]][start[1]]:
		return [] #start is blocked
	if layer[end[0]][end[1]]:
		return [] #end is blocked

	openSet = {}
	opens = []
	closedSet = {}
	
	cur = node(None, start, end, dist)
	
	openSet[cur.pos] = cur
	opens.append(cur)
	
	while len(opens):
		cur = opens.pop(0)
		
		if cur.pos not in openSet:
			continue

		del openSet[cur.pos]
		closedSet[cur.pos] = cur
		
		if cur.pos == end:
			break

		for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:#(-1,-1),(1,-1),(-1,1),(1,1)]:
			pos = cur.pos[0] + dx, cur.pos[1] + dy
			
			# Check if the point lies in the grid
			if (pos[0] < 0 or pos[1] < 0 or pos[0] >= w or pos[1] >= h or layer[pos[0]][pos[1]]):
				continue

			#check for blocks of diagonals
			if layer[cur.pos[0]][cur.pos[1] + dy]: continue
			if layer[cur.pos[0] + dx][cur.pos[1]]: continue

			new = node(cur, pos, end, dist)
			
			if pos in openSet and new.f >= openSet[pos].f: continue
			if pos in closedSet and new.f >= closedSet[pos].f: continue

			if pos in openSet: del openSet[pos]
			if pos in closedSet: del closedSet[pos]
			
			openSet[pos] = new
			
			lo = 0
			hi = len(opens)
			
			while lo < hi:
				mid = (lo + hi) / 2
				
				if new.f < opens[mid].f:
					hi = mid
				else:
					lo = mid + 1
			
			opens.insert(lo, new)
	
	if cur.pos != end:
		return []
					
	path = []
	
	while cur.prev != None:
		posX, posY = cur.pos
		
		path.append((posX * ratio, posY * ratio))
		
		cur = cur.prev
	
	return path
