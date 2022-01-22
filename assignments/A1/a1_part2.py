"""CSC111 Winter 2021 Assignment 1: Linked Lists, Part 2

Instructions (READ THIS FIRST!)
===============================

This Python module generates a graphical representation of linked lists.
You need to implement a few functions that visualize different components of
the list as described in the handout, and that make your visualization interactive.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu and Isaac Waller.
"""
import random
from typing import Tuple

import pygame
from pygame.colordict import THECOLORS

from a1_linked_list import LinkedList, _Node

################################################################################
# Graphics constants
################################################################################
# You should not change SCREEN_SIZE or GRID_SIZE, but may add your own constants underneath.
SCREEN_SIZE = (800, 800)  # (width, height)
GRID_SIZE = 8
PADDING_PX = 10

GRID_WIDTH = SCREEN_SIZE[0] // GRID_SIZE
GRID_HEIGHT = SCREEN_SIZE[1] // GRID_SIZE
SIDE_LENGTH = GRID_WIDTH // 2 - PADDING_PX

COLOR = (193, 154, 107)
COLOR2 = (148, 110, 74)
LINE_WIDTH = 2


################################################################################
# Pygame helper functions (don't change these!)
################################################################################
def initialize_screen(screen_size: tuple[int, int], allowed: list) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS['white'])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def draw_text(screen: pygame.Surface, text: str, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', 22)
    text_surface = font.render(text, True, THECOLORS['black'])
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def draw_grid(screen: pygame.Surface) -> None:
    """Draws a square grid on the given surface.

    The drawn grid has GRID_SIZE columns and rows.
    You can use this to help you check whether you are drawing nodes and edges in the right spots.
    """
    color = THECOLORS['grey']
    width, height = screen.get_size()

    for col in range(1, GRID_SIZE):
        x = col * (width // GRID_SIZE)
        pygame.draw.line(screen, color, (x, 0), (x, height))

    for row in range(1, GRID_SIZE):
        y = row * (height // GRID_SIZE)
        pygame.draw.line(screen, color, (0, y), (width, y))


def draw_text_centered(screen: pygame.Surface, text: str, center: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the center of the text.
    """
    font = pygame.font.SysFont('inconsolata', 22)
    text_surface = font.render(text, True, COLOR)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)


################################################################################
# 1. Drawing nodes and links
################################################################################
def draw_node(screen: pygame.Surface, node: _Node, pos: Tuple[int, int]) -> None:
    """Draw a node on the screen at the given position.

    pos represents the coordinates of the *top-left* corner of the node.

    Your drawing of the the node should include:
        - A rectangle split vertically into two halves.
        - The item stored in the node, displayed in the left half.
          You may assume the string representation of item is at most 3 characters
          long. You'll need to use the draw_text function we've provided above.

    NOTE: Do not draw the arrow representing the link to the next node in this function.
    You'll implement that part of the visualization separately in the draw_link function.

    We strongly recommend initializing new constants at the top of this file to represent
    node width, height, and colour.
    """
    x, y = pos
    p, sl = PADDING_PX, SIDE_LENGTH

    # Calculate side length
    xp, yp = x + p, y + p

    # Draw outer border
    pygame.draw.rect(screen, COLOR, (xp, yp, sl, sl), LINE_WIDTH)

    # Draw separation line
    pygame.draw.rect(screen, COLOR, (xp + sl - LINE_WIDTH, yp, sl, sl), LINE_WIDTH)

    # Draw text (centered)
    draw_text_centered(screen, str(node.item), (xp + sl // 2, yp + sl // 2))


def draw_link(screen: pygame.Surface, start: Tuple[int, int], end: Tuple[int, int]) -> None:
    """Draw a line representing a link from `start` to `end`.

    To indicate which end is the "start" of the line, draw a small circle at the starting point
    (like the diagrams we've seen in class).

    The rest of your link can be a simple line; you may, but are not required, to draw an
    arrowhead at the end of the line.
    """
    sx, sy = start
    ex, ey = end

    # Calculate position
    p, sl = PADDING_PX, SIDE_LENGTH
    sx, sy, ex, ey = sx + p, sy + p, ex + p, ey + p
    hsl = sl // 2

    # Line's starting point
    sp = (sx + sl * 1.5 - LINE_WIDTH, sy + hsl)
    ep = (ex, ey + hsl)

    # Draw
    pygame.draw.circle(screen, COLOR2, sp, 5)
    if ex > sx:
        pygame.draw.line(screen, COLOR2, sp, ep)

    # End x is smaller than start x, this happens when the page wraps
    else:
        points = [sp, (sp[0], sp[1] + sl), (ep[0] + hsl, sp[1] + sl), (ep[0] + hsl, ep[1] - hsl)]
        pygame.draw.lines(screen, COLOR2, False, points)


def index_to_pos(i: int) -> Tuple[int, int]:
    """
    Convert list index to on-screen pixel position

    Preconditions:
        - i >= 0
        - i < GRID_SIZE * GRID_SIZE

    :param i: Index
    :return: Position (x, y)
    """
    xi, yi = i % GRID_SIZE, i // GRID_SIZE
    return xi * GRID_WIDTH, yi * GRID_WIDTH

def pos_to_index(pos: Tuple[int, int]) -> int:
    """
    Convert on-screen pixel position to list index

    Preconditions:
        - 0 <= pos[0] < SCREEN_SIZE[0]
        - 0 <= pos[1] < SCREEN_SIZE[1]

    :param pos: Position (x, y)
    :return: Index
    """
    x, y = pos
    x, y = x // GRID_WIDTH, y // GRID_WIDTH
    return y * GRID_SIZE + x


def draw_none(screen: pygame.Surface, i: int) -> None:
    """
    Draw "none" at index i

    Preconditions:
        - i >= 0
        - i < GRID_SIZE * GRID_SIZE
    """
    p, sl = PADDING_PX, SIDE_LENGTH
    x, y = index_to_pos(i)
    x, y = x + p, y + p

    draw_text_centered(screen, "None", (x + sl, y + sl // 2))


def draw_three_nodes(screen_size: Tuple[int, int]) -> None:
    """Draw three nodes on a pygame screen of the given size.

    You may choose the coordinates for the nodes, as long as they do not overlap with each other
    and are separated by at least 10 pixels. Each link must start in the CENTRE of the start node's
    right half, and must end on the border of the end node (not inside the end node).
    This matches the style of node from lecture.

    The third node should link to "None", which you should visualize by calling draw_text.
    """
    screen = initialize_screen(screen_size, [])
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3

    # Draw nodes
    nodes = [node1, node2, node3]
    for i in range(3):
        draw_node(screen, nodes[i], index_to_pos(i))
        draw_link(screen, index_to_pos(i), index_to_pos(i + 1))
    draw_none(screen, 3)

    # Don't change the code below (it simply waits until you close the Pygame window)
    pygame.display.flip()
    pygame.event.wait()
    pygame.display.quit()


################################################################################
# 2. Drawing a full linked list
################################################################################
def draw_list(screen: pygame.Surface, lst: LinkedList, show_grid: bool = False) -> None:
    """Draw the given linked list on the screen.

    The linked list nodes should be drawn in a grid pattern with GRID_SIZE rows and columns.
    See the assignment handout for details and constraints on your drawing.

    If the show_grid parameter is True, the grid is drawn on the board. You can use
    the grid to help you make sure you're drawing nodes in the correct locations.
    By default, show_grid is False.

    Preconditions:
        - len(lst) < GRID_SIZE * GRID_SIZE

    As with draw_node, we strongly recommend initializing new constants at the top of this file
    to store numbers used to position the nodes.

    We have started the linked list traversal pattern for you. Note that we're accessing
    a private LinkedList attribute _first, which is generally not a good practice but we're
    allowing you to do so here to simplify your code a little.
    """
    if show_grid:
        draw_grid(screen)

    curr = lst._first
    curr_index = 0

    while curr is not None:
        draw_node(screen, curr, index_to_pos(curr_index))
        draw_link(screen, index_to_pos(curr_index), index_to_pos(curr_index + 1))

        curr = curr.next
        curr_index = curr_index + 1

    draw_none(screen, curr_index)


################################################################################
# 3. Handling user events
################################################################################
def run_visualization(screen_size: tuple[int, int], ll_class: type,
                      show_grid: bool = False) -> None:
    """Run the linked list visualization.

    Initialize a screen of the given size, and show the grid when show_grid is True.
    ll_class is the type of linked list to use.

    Preconditions:
        - ll_class is LinkedList or issubclass(ll_class, LinkedList)

    This function is provided for you for Part 3, and you *should not change it*.
    Instead, your task is to implement the helper function handle_mouse_click (and
    any other helpers you decide to add).
    """
    # Initialize the Pygame screen, allowing for mouse click events.
    screen = initialize_screen(screen_size, [pygame.MOUSEBUTTONDOWN])

    # Initialize a random linked list of length 50.
    lst = ll_class(random.sample(range(-99, 1000), 50))

    while True:
        # Draw the list (on a white background)
        screen.fill(THECOLORS['white'])
        draw_list(screen, lst, show_grid)
        pygame.display.flip()

        # Wait for an event (either pygame.MOUSEBUTTONDOWN or pygame.QUIT)
        event = pygame.event.wait()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Call our event handling method
            handle_mouse_click(lst, event, screen.get_size())
        elif event.type == pygame.QUIT:
            break

    pygame.display.quit()


def handle_mouse_click(lst: LinkedList, event: pygame.event.Event,
                       screen_size: Tuple[int, int]) -> None:
    """Handle a mouse click event.

    A pygame mouse click event object has two attributes that are important for this method:
        - event.pos: the (x, y) coordinates of the mouse click
        - event.button: an int representing which mouse button was clicked.
                        1: left-click, 3: right-click

    The screen_size is a tuple of (width, height), and should be used together with
    event.pos to determine which cell is being clicked. If a click happens exactly on
    the boundary between two cells, you may decide which cell is selected.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - screen_size[0] >= 200
        - screen_size[1] >= 200
    """
    # Find selected node
    i = pos_to_index(event.pos)

    # Left click - Remove
    if event.button == 1:
        try:
            lst.pop(i)
        except IndexError:
            # When the clicked node doesn't exist, do nothing
            pass

    # Right-click - Search
    if event.button == 3:
        # TODO: Implement this
        pass


if __name__ == '__main__':
    # draw_three_nodes(SCREEN_SIZE)
    run_visualization(SCREEN_SIZE, LinkedList)

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'disable': ['E1136'],
    #     'exclude-protected': ['_first'],
    #     'extra-imports': ['random', 'pygame', 'pygame.colordict', 'a1_linked_list'],
    #     'generated-members': ['pygame.*']
    # })
    #
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()
