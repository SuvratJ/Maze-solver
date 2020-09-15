"""Module implements functions using pygame to create common ui sprites.

The module includes functions to facilitate UI creation and IO operations for the A*
GUI Project.

Author: Suvrat Jain <suvrat_jain@outlook.com>
"""
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def display_button(screen, text, position, dimension, button_colour, action=None):
    """Make and render a button on screen which executes action when pressed.

    Keyword arguments:
    screen -- pygame display
    text -- The text for the button
    position -- (x, y) coordinates of top left corner of the button
    dimension -- (width, height) dimensions of the button
    button_color -- color of the button
    action -- function to be executed on buton press (defaut : None)
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x, y = position
    w, h = dimension
    ic = button_colour
    ac=(ic[0]+15, ic[1]+15, ic[2])

    # Draw sprites and text
    # On mouse hover
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        fontobject = pygame.font.Font("segoeui.ttf", 22)
        screen.blit(fontobject.render(text, 1, (25, 25, 25)), (x+15, y+10))
        if click[0] == 1 and action is not None:
            action()
    # Without mouse hover
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
        fontobject = pygame.font.Font("segoeui.ttf", 22)
        screen.blit(fontobject.render(text, 1, (25, 25, 25)), (x+15, y+10))

def get_key():
    """Utility function to get keypress"""
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key

def display_message_box(screen, message, xposition=None, yposition=None):
    """Function to display a message box"""
    fontobject = pygame.font.Font("segoeui.ttf", 28)
    # Set position if not provided in arguments
    if(xposition is None and yposition is None):
        xposition, yposition = (screen.get_width() / 2) - 200, (screen.get_height() / 2) - 40,
    # Draw sprites and text
    pygame.draw.rect(screen, (0, 0, 0), (xposition, yposition, 400, 60), 0)
    pygame.draw.rect(screen, (255, 255, 255), (xposition+8, yposition+8, 384, 44), 1)
    if message:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)), (xposition+15, yposition+10))
    pygame.display.flip()

def display_prompt(screen, question):
    """Function to display an input prompt and return the input string"""
    pygame.font.init()
    current_string = []
    display_message_box(screen, question + ": " + "".join(str(e) for e in current_string))
    # 
    while True:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
            display_message_box(screen, question + ": " + "".join(str(e) for e in current_string))
        elif inkey == K_RETURN:
            break
        elif inkey <= 127 and len(current_string)<=7:
            current_string.append(chr(inkey))
            display_message_box(screen, question + ": " + "".join(str(e) for e in current_string))
    return "".join(str(e) for e in current_string)
