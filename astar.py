# CHANGE NUMBER OF ROWS. WHY DOES THIS HAPPEN?
# WHY IS START NODE NOT SHOWING


from string import whitespace
from numpy import ndenumerate
import pygame
import math
from queue import PriorityQueue

WIN_WIDTH = 800 # window width
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# colours - RGB colour codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node: # hold location of each node and its colour
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width # eg row 5 * 10px tells us top left corner is 50px across
        self.y = col * width 
        self.colour = WHITE
        self.neighbour = [] # empty set of neighbours
        self.total_rows = total_rows # no of rows & cols on canvas  

    # get state
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self): # if is part of closed set
        return self.colour == RED

    def is_open(self): # if is part of open set
        return self.colour == GREEN
    
    def is_barrier(self): # if is part of user-made barrier
        return self.colour == BLACK
    
    def is_start(self): # if is start node
        return self.colour == ORANGE
    
    def is_end(self): # if is end node
        return self.colour == PURPLE

    # set state
    def reset(self): # if is part of closed set
        self.colour = WHITE
    
    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK
    
    def make_start(self):
        self.colour = ORANGE
    
    def make_end(self):
        self.colour = PURPLE

    def make_path(self):
        self.colour = TURQUOISE
    
    def draw(self, win):
        # parameters = surface, colour, Rect, position (x, y, width, length)
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        pass

    # special method overrides behaviour of < operator
    def __lt__(self, other): # comparing nodes
        return False
    
def h(p1, p2): # heuristic formula - Taxicab Distance
    x1, y1 = p1 # deconstructing the p1 object
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)


def make_grid(rows, width): # make grid with 'rows' rows each with 'rows' columns
    grid = []
    gap = width // rows # note width is same as height, gives width of each node
    for i in range(rows):
        grid.append([]) # append row (empty list)
        for j in range(rows): # note rows == columns
            node = Node(i, j, gap, rows)
            grid[i].append(node) # append Node to row i
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows): # draw rows from x = 0 to x = width
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid: # grid is our 2d array of Node objects
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width) # draw gridlines
    pygame.display.update() # update canvas


def get_clicked_pos(pos, rows, width): # return row and col of Node clicked on
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width) # generate 2d list of Node objs

    start = None
    end = None
    
    run = True
    started = False # whether algorithm run or not

    while run:
        draw(win, grid, ROWS, width) # draw grid with nodes
        for event in pygame.event.get(): # loop thru all possible events
            if event.type == pygame.QUIT: # if 'X' button clicked
                run = False

            if started: # once algorithm started, prevent user from interacting with screen
                continue

            if pygame.mouse.get_pressed()[0]: # if left mouse btn clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col] # clicked node

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            
            elif pygame.mouse.get_pressed()[2]: # if right mouse btn clicked
                pass
    

    pygame.quit()

main(WIN, WIN_WIDTH)



    

