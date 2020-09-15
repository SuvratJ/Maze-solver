import pygame
from random import randint
from implementation import *
import UI
from exceptions import *

def pause():
    """Pause the program until mouse or key press"""
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN or
                    event.type == pygame.MOUSEBUTTONDOWN):
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

def input_dimensions():
    """Prompt user to input width and height"""
    global prod_floor
    try:
        prod_floor.width, prod_floor.height, prod_floor.walls = (
            int(UI.display_prompt(disp, "Width ")), int(UI.display_prompt(disp, "Height ")), [])
    except ValueError:
        UI.display_message_box(disp, "Enter valid value")
        pause()
    disp.blit(bg, (0, 0))

def input_obstacles():
    """Prompt user to input number of obstacles"""
    global prod_floor
    try:
        obstacle_number = int(UI.display_prompt(disp, "No. of obstacles "))
        prod_floor.make_random_walls(obstacle_number)
    except ValueError:
        UI.display_message_box(disp, "Enter valid value")
        pause()
    except TooManyObstaclesError:
        UI.display_message_box(disp, "Obstacles more than grid size")
        pause()
    disp.blit(bg, (0, 0))

def input_coordinates():
    """Prompt user to enter the start and end coordinates"""
    global start
    global goal
    try:
        start = tuple(int(e) for e in UI.display_prompt(disp, "Start coordinates x, y ").split(","))
        goal = tuple(int(e) for e in UI.display_prompt(disp, "End coordinates x, y ").split(","))
        # Check if coordinates are valid
        if (len(start) != 2 or len(goal) != 2 or
            not (0 <= start[0] < prod_floor.width
                 and 0 <= start[1] < prod_floor.height
                 and 0 <= goal[0] < prod_floor.width
                 and 0 <= goal[1] < prod_floor.height)):
            raise InvalidCoordinateError()
    # Handle ValueError and InvalidCoordinateError
    except Error:
        UI.display_message_box(disp, "Enter valid coordinates")
        start = (0, 0)
        goal = (0, 0)
        pause()
    disp.blit(bg, (0, 0))

def setup_grid():
    global prod_floor
    # Setup position and size of grid
    try:
        size = min([50, 1080//prod_floor.width, 500//prod_floor.height])
    except ZeroDivisionError:
        UI.display_message_box(disp, "Input parameters first")
        pause()
        return
    posx, posy = max([100, (1280-size*prod_floor.width)//2]), 170
    return size, (posx, posy+10)

def show_grid(size, posx, posy):
    # Draw the grid
    for i in range(0, prod_floor.height):
        for z in range(0, prod_floor.width):
            pygame.draw.rect(disp, black, [posx+size*z, posy+size*i, size, size], 1)
    pygame.draw.rect(disp, black,
                     [posx-1, posy-1, prod_floor.width*size+2, prod_floor.height*size+2], 1)

    # Draw the obstacles
    for (x, y) in prod_floor.walls:
        pygame.draw.rect(disp, red, [posx+size*x+1, posy+size*y+1, size-2, size-2])
        pygame.display.update()

    # Draw the path
    for (x, y) in prod_floor.path:
        pygame.draw.rect(disp, (10, 200, 10), [posx+size*x+1, posy+size*y+1, size-2, size-2])
        pygame.display.update()

def run_a_star():
    a_star_search(prod_floor, start, goal)
    size, (posx, posy) = setup_grid()
    show_grid(size, posx, posy)

if __name__ == "__main__":
    pygame.init()
    # set color variables
    white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
    #set display
    disp = pygame.display.set_mode((1280, 720))
    #caption
    pygame.display.set_caption("A* Pathfinding")
    #beginning of logic
    prod_floor = SquareGrid(50, 30)
    prod_floor.make_random_walls(400)
    clock = pygame.time.Clock()
    bg = pygame.image.load("bg.jpg")
    disp.blit(bg, (0, 0))
    start = (0, 0)
    goal = (49, 29)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        UI.display_button(disp,"Input Dimensions",(100,50),(195,50),(150,140,100), input_dimensions)
        UI.display_button(disp,str(prod_floor.width)+"x"+str(prod_floor.height),(100,100),(195,50),(120,110,90))
        UI.display_button(disp,"Generate Obstacles",(400,50),(215,50),(150,140,100), input_obstacles)
        UI.display_button(disp,str(len(prod_floor.walls)),(400,100),(215,50),(120,110,90))
        UI.display_button(disp,"Input Coordinates",(750,50),(200,50),(150,140,100), input_coordinates)
        UI.display_button(disp,str(start)+str(goal),(750,100),(200,50),(120,110,90))
        UI.display_button(disp,"Run A*",(1080,50),(100,50),(150,140,100), run_a_star)

        pygame.display.update()
        clock.tick(15)