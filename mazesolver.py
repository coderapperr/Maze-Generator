import pygame
import random
from time import sleep

class Cell:
	'''
		Cell class represents one cell in the grid
	'''
	def __init__(self, i, j):
		self.i = i
		self.j = j
		# TOP RIGHT BOTTOM LEFT
		self.walls = [True, True, True, True]
		self.visited = False

	def draw_cell(self, SCREEN, CELL_WIDTH):
		x = self.i*CELL_WIDTH
		y = self.j*CELL_WIDTH
		# pygame.draw.rect(SCREEN, (255, 255, 255), [x, y, CELL_WIDTH, CELL_WIDTH], 1)

		if self.visited:
			pygame.draw.rect(SCREEN, (0, 0, 255), [x, y, CELL_WIDTH, CELL_WIDTH])

		#top
		if self.walls[0]:
			pygame.draw.line(SCREEN, (0, 0, 0), (x           ,            y), (x+CELL_WIDTH,            y))
		#right
		if self.walls[1]:
			pygame.draw.line(SCREEN, (0, 0, 0), (x+CELL_WIDTH,            y), (x+CELL_WIDTH, y+CELL_WIDTH))
		#bottom
		if self.walls[2]:
			pygame.draw.line(SCREEN, (0, 0, 0), (x+CELL_WIDTH, y+CELL_WIDTH), (x           , y+CELL_WIDTH))
		#left
		if self.walls[3]:
			pygame.draw.line(SCREEN, (0, 0, 0), (x			 , y+CELL_WIDTH), (x		   ,            y))

		


	def highlight(self, SCREEN, CELL_WIDTH):
		x = self.i*CELL_WIDTH
		y = self.j*CELL_WIDTH

		pygame.draw.rect(SCREEN, (255, 255, 0), [x, y, CELL_WIDTH, CELL_WIDTH])

	@staticmethod
	def index(i, j, cols, rows):
		if i<1 or j<1 or i>rows or j>cols:
			return -1
		return j + (i-1) * cols

	def check_neighbours(self, cols, rows, grid):
		neighbours = []
		
		index = self.index(self.i, self.j-1, cols, rows)
		if index != -1:
			top = grid[index-1]
			if not top.visited:
				neighbours.append(top)

		index = self.index(self.i+1, self.j, cols, rows)
		if index != -1:
			right = grid[index-1]
			if not right.visited:
				neighbours.append(right)
		
		index = self.index(self.i, self.j+1, cols, rows)
		if index != -1:
			bottom = grid[index-1]
			if not bottom.visited:
				neighbours.append(bottom)
		
		index = self.index(self.i-1, self.j, cols, rows)
		if index != -1:
			left = grid[index-1]
			if not left.visited:
				neighbours.append(left)

		if len(neighbours) > 0:
			cell = random.choice(neighbours)
			return cell

		return None


class GridWindow:
	'''
		GridWindow class represents the entire grid
	'''
	def __init__(self, SCREEN, WINDOW, CELL_WIDTH):
		self.SCREEN = SCREEN
		self.WINDOW = WINDOW
		self.CELL_WIDTH = CELL_WIDTH
		self.grid = []
		self.current = None
		self.rows = self.WINDOW//self.CELL_WIDTH
		self.cols = self.WINDOW//self.CELL_WIDTH
		self.stack = []

	def generate_grid(self):
		'''
			generate_grid method to generate grid
		'''

		for i in range(1,self.rows+1):
			for j in range(1,self.cols+1):
				cell = Cell(i, j)
				self.grid.append(cell)

		self.current = self.grid[0]

	def draw_grid(self):

		for cell in self.grid:
			cell.draw_cell(self.SCREEN, self.CELL_WIDTH)

	def remove_walls(self, a, b):
		x = a.i - b.i
		y = a.j - b.j

		if x == 1:
			a.walls[3] = False
			b.walls[1] = False

		elif x == -1:
			a.walls[1] = False
			b.walls[3] = False

		if y == 1:
			a.walls[0] = False
			b.walls[2] = False

		elif y == -1:
			a.walls[2] = False
			b.walls[0] = False

	def algo(self):

		self.generate_grid()
		self.draw_grid()
		pygame.display.update()

		sleep(0.4)

		self.current.visited = True


		while self.current:

			self.draw_grid()
			pygame.display.update()
			sleep(0.4)

			neighbour = self.current.check_neighbours(self.cols, self.rows, self.grid)

			if neighbour:
				neighbour.highlight(self.SCREEN, self.CELL_WIDTH)

				neighbour.visited = True
				self.stack.append(self.current)
				self.remove_walls(self.current, neighbour)
				self.current = neighbour

			elif len(self.stack)>0:
				self.current = self.stack.pop()

			else:
				break

			self.current.highlight(self.SCREEN, self.CELL_WIDTH)
			pygame.display.update()
			sleep(0.4)

			





def main():
	# WHITE = (255, 255, 255)
	# GREEN = (0, 255, 0,)
	# BLUE = (0, 0, 255)
	# YELLOW = (255 ,255 ,0)

	# initalise Pygame
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((480, 480))
	pygame.display.set_caption("Python Maze Generator")
	clock = pygame.time.Clock()
	screen.fill((255, 255, 255))
	gw  = GridWindow(screen, 400, 40)
	gw.algo()
	pygame.display.update()

	running = True
	while running:
	    # keep running at the at the right speed
	    clock.tick(30)
	    # process input (events)
	    for event in pygame.event.get():
	        # check for closing the window
	        if event.type == pygame.QUIT:
	            running = False

	     

	   

if __name__ == '__main__':
	main()