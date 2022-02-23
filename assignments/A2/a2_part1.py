"""CSC111 Winter 2021 Assignment 2: Trees, Chess, and Artificial Intelligence (Part 1)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of functions and/or classes you'll define
for Part 1 of this assignment. Please note that in addition to this file, you will
also need to modify a2_game_tree.py by following the instructions on the assignment
handout. You should NOT make any changes to a2_minichess.py.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 Mario Badr, David Liu, and Isaac Waller.
"""
import csv
import random
from typing import Optional

import a2_game_tree
import a2_minichess


################################################################################
# Loading Minichess datasets
################################################################################
def load_game_tree(games_file: str) -> a2_game_tree.GameTree:
    """Create a game tree based on games_file.

    Preconditions:
        - games_file refers to a csv file in the format described on the assignment handout

    Implementation hints:
        - You can review Tutorial 4 for how we read CSV files in Python.

    >>> gt = load_game_tree('data/small_sample.csv')
    >>> [sub.move for sub in gt.get_subtrees()]
    ['a2b3', 'b2c3', 'b2a3', 'c2d3', 'c2b3', 'd2c3']
    >>> gt = gt.find_subtree_by_move('c2d3')
    >>> [sub.move for sub in gt.get_subtrees()]
    ['d4d3']
    >>> gt = gt.get_subtrees()[0]
    >>> len(gt.get_subtrees())
    2
    """
    tree = a2_game_tree.GameTree()

    with open(games_file, 'r', newline='', encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            tree.insert_move_sequence(row)

    return tree


################################################################################
# Minichess AI that uses a GameTree
################################################################################
class RandomTreePlayer(a2_minichess.Player):
    """A Minichess player that plays randomly based on a given GameTree.

    This player uses a game tree to make moves, descending into the tree as the game is played.
    On its turn:

        1. First it updates its game tree to its subtree corresponding to the move made by
           its opponent. If no subtree is found, its game tree is set to None.
        2. Then, if its game tree is not None, it picks its next move randomly from among
           the subtrees of its game tree, and then reassigns its game tree to that subtree.
           But if its game tree is None or has no subtrees, the player picks its next move randomly,
           and then sets its game tree to None.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[a2_game_tree.GameTree]

    def __init__(self, game_tree: a2_game_tree.GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        self._game_tree = game_tree

    def make_move(self, game: a2_minichess.MinichessGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game

        >>> t = a2_game_tree.GameTree()
        >>> t.insert_move_sequence(['c2d3', 'd4d3', 'd2c3'])
        >>> t.insert_move_sequence(['c2d3', 'd4d3', 'b1d3'])
        >>> g = a2_minichess.MinichessGame()
        >>> p = RandomTreePlayer(t)
        >>> p.make_move(g, None)
        'c2d3'
        >>> p._game_tree.move
        'c2d3'
        >>> len(p._game_tree.get_subtrees())
        1
        >>> g.make_move('c2d3')
        >>> g.make_move('d4d3')
        >>> m = p.make_move(g, 'd4d3')
        >>> m in ['d2c3', 'b1d3']
        True
        >>> p._game_tree.move == m
        True
        >>> len(p._game_tree.get_subtrees())
        0
        >>> g.make_move(m)
        >>> m = random.choice(g.get_valid_moves())
        >>> g.make_move(m)
        >>> m = p.make_move(g, m)
        >>> m in g.get_valid_moves()
        True
        >>> p._game_tree is None
        True
        """
        # 1. First it updates its game tree to the subtree corresponding to the move made by its
        #    opponent. If no subtree is found, its game tree is set to None.
        if previous_move and self._game_tree:
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)

        # 2. The player picks its move based on the following conditions:

        # If its game tree is None or is just a leaf with no subtrees, it picks a random move from
        # all valid moves from the game, like RandomPlayer.
        if self._game_tree is None or len(self._game_tree.get_subtrees()) == 0:
            move = random.choice(game.get_valid_moves())

        # Otherwise, it picks a random move from among its game tree’s subtrees.
        else:
            move = random.choice(self._game_tree.get_subtrees()).move

        # Update tree
        if self._game_tree:
            self._game_tree = self._game_tree.find_subtree_by_move(move)

        return move


def part1_runner(games_file: str, n: int, black_random: bool) -> None:
    """Create a game tree from the given file, and run n games where White is a RandomTreePlayer.

    The White player is a RandomTreePlayer whose game tree is the one generated from games_file.
    The Black player is a RandomPlayer if black_random is True, otherwise it is a RandomTreePlayer
    using the SAME game tree as White.

    Preconditions:
        - n >= 1
        - games_file refers to a csv file in the format described on the assignment handout

    Implementation notes:
        - Your implementation MUST correctly call a2_minichess.run_games. You may choose
          the values for the optional arguments passed to the function.
    """
    tree = load_game_tree(games_file)
    white = RandomTreePlayer(tree)
    black = a2_minichess.RandomPlayer() if black_random else RandomTreePlayer(tree)
    a2_minichess.run_games(n, white, black, show_stats=True)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['a2_minichess', 'a2_game_tree', 'random', 'csv'],
        'allowed-io': ['load_game_tree']
    })

    # Sample call to part1_runner (you can change this, just keep it in the main block!)
    part1_runner('data/white_wins.csv', 50, False)
