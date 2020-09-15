"""Module implements grid class as well as a* pathfinding algorithm for the A* GUI Project

Author: Suvrat Jain <suvrat_jain@outlook.com>
"""
import random
from exceptions import *

class SquareGrid:
    """Class for a 2 dimensional grid with auxilliary functions for implentation of
    A* algorithm
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.path = []
        self.weights = {}

    def make_random_walls(self, num):
        """Generate num random obstacles in the grid and store them in walls array"""
        if num > self.width * self.height:
            raise TooManyObstaclesError()
        self.walls = []
        random.seed(0)
        while num > 0:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if (x, y) in self.walls:
                continue # Run iteration again if obstacle already exists
            else:
                self.walls.append((x, y))
                num = num-1

    def in_bounds(self, idx):
        """Check if given coordinates are within bounds of the grid and return True if so
        else return False
        """
        (x, y) = idx
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, idx):
        """Check if given coordinates are not obstacles and return True if so else return 
        False
        """
        return idx not in self.walls
    
    def neighbors(self, idx):
        """Calculate and return array of valid neighbours of given coordinate"""
        (x, y) = idx
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
    
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)
    
def a_star_search(grid, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for next_cell in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(current, next_cell)
            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + manhattan_dist(goal, next_cell)
                frontier.put(next_cell, priority)
                came_from[next_cell] = current
    
    try:
        grid.path = reconstruct_path(came_from, start, goal)
    except KeyError:
        pass
    except ValueError:
        pass


    

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def manhattan_dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

