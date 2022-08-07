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
        self.neighbours = [] # empty set of neighbours
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

    def update_neighbours(self, grid): # list of neighbours of each node
        self.neighbours = []

        # first check we are not on the last playable row (as row indexing begins from 0)
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): # down a row same col
            self.neighbours.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): # up a row same col
            self.neighbours.append(grid[self.row-1][self.col])
        
        if self.col < self.total_rows -1 and not grid[self.row][self.col+1].is_barrier(): # col to the right
            self.neighbours.append(grid[self.row][self.col+1])
        
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): # col to the left
            self.neighbours.append(grid[self.row][self.col-1])

    # special method overrides behaviour of < operator
    def __lt__(self, other): # comparing nodes
        return False
    
def h(p1, p2): # heuristic formula - Taxicab Distance
    x1, y1 = p1 # deconstructing the p1 object
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw): # initally current = end node
    while current in came_from: # new current is whatever node we came from
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    # the argument passed into 'draw' is a lambda function
    count = 0
    open_set = PriorityQueue() # data struct designed to return lowest f value (aka lowest distance to end node)
    open_set.put((0, count, start)) # g(x), count (order node added), start node
    came_from = {} # set of previous node that created path

    # convert 2d array into 1d dict with node: gscore
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # as start is 0 distance from itself

    f_score = {node: float("inf") for row in grid for node in row} # set each node with f_score of infinity
    f_score[start] = h(start.get_pos(), end.get_pos()) # get Taxicab distance from start to end node

    open_set_hash = {start} # tells us which items are and are not in priority queue - as the PQ structre cant to this itself

    while not open_set.empty(): # allow user to exit when algorithm running
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2] # get just the node of the lowest val f_score from set
        open_set_hash.remove(current) # synch with open set hash

        if current == end: # if we have reached the end node, call make path function
            reconstruct_path(came_from, end, draw) # call make path function with last node before end
            end.make_end() # so it doesnt get coloured over.
            start.make_start() # colour over the 'path' colour
            return True
        
        for neighbour in current.neighbours: # for each neighbour of the curr node
            temp_g_score = g_score[current]+1 # as 1 more node away from start node
            
            if temp_g_score < g_score[neighbour]: # if new path less than infinity (or old path) for neighbour node
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score # update value of better path
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos()) # g_score + h_score
                if neighbour not in open_set_hash:
                    count +=1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open() # so we know we are considering it
        
        draw()
 
        if current != start: # if node we just considered is not start node, close it - as it has been fully explored now
            current.make_closed()
    
    return False


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
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    
                    # calling draw function in lambda argument
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)


                if event.key == pygame.K_c: # reset grid if 'c' pressed
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIN_WIDTH)



    

