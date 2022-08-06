from string import whitespace
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
    
    # def make_start(self):
    #     self.colour = ORANGE
    
    def make_end(self):
        self.colour = PURPLE

    def make_path(self):
        self.colour = TURQUOISE
    
    def draw(self, win):
        # parameters = surface, colour, Rect, position (x, y, width, length)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        pass

    # special method overrides behaviour of < operator
    def __lt__(self, other): # comparing nodes
        return False
    
    
