"""
Objective: This file builds the game tree necessary for Othello computer players to run.

This file is Copyright (c) 2021 Chun Yin Yan and Gabriel Pais

"""
from __future__ import annotations

import math
from copy import deepcopy
from typing import Any

import Visualization  # DO NOT REMOVE THIS LINE
from Othello_Game import Othello

# Score given to the Othello board
# Higher scores indicate more valuable positions, while negative scores indicate
# disadvantageous positions
BOARD_SCORE = [[120, -20, 20, 5, 5, 20, -20, 120],
               [-20, -40, -5, -5, -5, -5, -40, -20],
               [20, -5, 15, 3, 3, 15, -5, 20],
               [5, -5, 3, 3, 3, 3, -5, 5],
               [5, -5, 3, 3, 3, 3, -5, 5],
               [20, -5, 15, 3, 3, 15, -5, 20],
               [-20, -40, -5, -5, -5, -5, -40, -20],
               [120, -20, 20, 5, 5, 20, -20, 120]]


class GameTree:
    """
    A decision game tree for Othello


    Instance Attributes:
        - game: the current game state. Note that this game state is after self.move is applied and
                before any move from the subtrees is applied
        - move: the previous move of the game. Default value is ('START', 'START')
                The moves of the subtrees are the moves that are available
        - is_white_move: whether it is white's turn to move (i.e. to choose a move from the
                subtrees)
        - score: score is determined by all the scores of the subtrees. A more positive score
                 indicates a more advantageous move for white; a more negative score indicates a
                 more advantageous move for black
    """
    # _subtrees: the list of subtrees of the root of the GameTree
    game: Othello
    move: tuple
    is_white_move: bool
    score: float
    _subtrees: list[GameTree]

    def __init__(self, game: Othello = Othello(), score: float = 0.0) -> None:
        """
        Initialize a game tree for Othello.

        The default value for game is a new Othello game. Input the current game state as the
        argument to start the tree from this game state.
        The score of this (previous) move.

        Note that self.move == game.previous_move. The default value is ('START', 'START').
        """
        self.game = game
        self.move = game.previous_move
        self.is_white_move = game.is_white_move
        self.score = score
        self._subtrees = []

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: tuple) -> Any:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree

        return None

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree, and recalculate the score of the root of the tree."""
        self._subtrees.append(subtree)
        self.calculate_score()

    def calculate_score(self) -> None:
        """
        Calculate the score for such move based on its subtree.

        Preconditions:
            - each subtree has its own score calculated already.
        """
        special_moves = [('GG', 'GG'), ('START', 'START'), ('', '')]

        # Case 1: calculate the score of a leaf
        if self._subtrees == []:

            w, b = self.game.score()

            # Case 1a: the leaf is the end of the game
            if self.move == ('GG', 'GG'):
                w, b = self.game.score()
                if w > b:
                    self.score = 10000
                elif w < b:
                    self.score = -10000
                else:
                    self.score = 0

            # Case 1b: the leaf is the beginning of the game
            elif self.move == ('START', 'START'):
                self.score = 0

            # Case 1c: the leaf is a pass-your-turn move
            elif self.move == ('', ''):
                if self.is_white_move:
                    self.score = 100
                else:
                    self.score = -100

            # Case 1d: the leaf is a normal move
            if self.move not in special_moves:
                if self.is_white_move:
                    self.score = (w - b) * 0.75 + BOARD_SCORE[self.move[0]][self.move[1]] * -0.25
                else:
                    self.score = (w - b) * 0.75 + BOARD_SCORE[self.move[0]][
                        self.move[1]] * 0.25

        # Case 2: calculate a 'node' in the middle of a tree
        else:
            # Case 2a:
            # if it is white's turn to make a move (to choose any move in the subtrees),
            # the score is the maximum of the scores of all subtrees
            if self.is_white_move:
                self.score = -100000
                for subtree in self._subtrees:
                    if subtree.score > self.score:
                        self.score = subtree.score

            # Case 2b:
            # if it is black's turn to make a move (to choose any move in the subtrees),
            # the score is the minimum of the scores of all subtrees
            else:
                self.score = 100000
                for subtree in self._subtrees:
                    if subtree.score < self.score:
                        self.score = subtree.score

    def generate_moves_full(self, d: int) -> None:
        """
        Generate the full tree, all possible paths up to depth d.

        Note: this function is not inefficient and should not be called with large values of d.
        """
        self.minimax(d)

    def generate_moves_quick(self, d: int) -> None:
        """
        Generate the tree using minimax and alpha-beta pruning, all strategically-viable paths
        up to depth d.

        This algorithm calculates the possible paths up to depth d while building the tree. Using
        minimax and alpha-beta pruning, the maximizer is White Player and minimizer is Black Player;
        alpha-beta pruning is used to calculate whether the possible path calculated for the
        maximizer/minimizer is strategically-viable. "Bad" paths are omitted in this tree.
        """
        self.minimaxab(d)

    def minimax(self, depth: int) -> None:
        """
        Generate the full tree, all possible paths up to depth d.

        Note: this function is not inefficient and should not be called with large values of d.
        """
        # if depth is 0, no subtrees should be generated. Calculate the score of this leaf.
        if depth == 0:
            self.calculate_score()
            return None

        # if depth > 0:
        # There are valid moves
        if self.game.get_valid_moves_now() != []:
            for move in self.game.get_valid_moves_now():
                # First, check if there is existing subtree
                subtree = self.find_subtree_by_move(move)

                # if subtree does not exist
                if subtree is None:
                    # copy the current game state and make the move
                    game_copy = deepcopy(self.game)
                    game_copy.make_move(move[0], move[1])
                    # make a new subtree
                    subtree = GameTree(game_copy)
                    # Recurse into the paths
                    subtree.minimax(depth - 1)
                    subtree.calculate_score()
                    # Add the newly-created subtree to the root
                    self.add_subtree(subtree)
                # If the subtree exists, just recurse into it
                else:
                    # Recurse into the paths
                    subtree.minimax(depth - 1)
                    subtree.calculate_score()

        # There is no valid moves in this turn
        else:
            # Game might have ended
            if self.game.get_valid_moves_white() == set() == self.game.get_valid_moves_black():
                # First, check if there is existing subtree
                move = ('GG', 'GG')
                subtree = self.find_subtree_by_move(move)
                # If subtree does not exist, create a new subtree
                if subtree is None:
                    game_copy = deepcopy(self.game)
                    game_copy.make_move(-1, -1)
                    subtree = GameTree(game_copy)
                    subtree.calculate_score()
                    # Add the newly-created subtree to the root
                    self.add_subtree(subtree)
                # If the subtree exists, do nothing
                else:
                    pass
            else:
                # First, check if there is existing subtree
                move = ('', '')
                subtree = self.find_subtree_by_move(move)
                # If subtree does not exist, create a new subtree
                if subtree is None:
                    game_copy = deepcopy(self.game)
                    game_copy.make_move(-1, -1)
                    subtree = GameTree(game_copy)
                    # Recurse into the paths
                    subtree.minimax(depth - 1)
                    subtree.calculate_score()
                    # Add the newly-created subtree to the root
                    self.add_subtree(subtree)
                # If the subtree exists, just recurse into it
                else:
                    # Recurse into the paths
                    subtree.minimax(depth - 1)
                    subtree.calculate_score()

    def minimaxab(self, depth: int, a: float = -math.inf, b: float = math.inf) -> None:
        """
        Generate the tree using minimax and alpha-beta pruning, all strategically-viable paths
        up to depth d.

        This algorithm calculates the possible paths up to depth d while building the tree. Using
        minimax and alpha-beta pruning, the maximizer is White Player and minimizer is Black Player;
        alpha-beta pruning is used to calculate whether the possible path calculated for the
        maximizer/minimizer is strategically-viable. "Bad" paths are omitted in this tree.
        """
        # Case 1:
        # if depth is 0, no subtrees should be generated. Calculate the score of this leaf.

        if depth == 0:
            self.calculate_score()
            return None

        # if depth > 0.
        # Case 2: there are valid moves
        if self.game.get_valid_moves_now() != []:
            for move in self.game.get_valid_moves_now():

                # First, check if there is existing subtree
                subtree = self.find_subtree_by_move(move)

                # If subtree does not exist, create a new subtree
                if subtree is None:
                    game_copy = deepcopy(self.game)
                    game_copy.make_move(move[0], move[1])
                    subtree = GameTree(game_copy)
                    # Recurse into the paths
                    subtree.minimaxab(depth - 1, a, b)
                    subtree.calculate_score()
                    # Add the newly-created subtree to the root
                    self.add_subtree(subtree)
                # If the subtree exists, just recurse into it
                else:
                    # Recurse into the paths
                    subtree.minimaxab(depth - 1, a, b)
                    subtree.calculate_score()

                # Alpha-beta pruning: determine if we still need to create more subtrees
                # Maximizer: want max score
                if self.is_white_move:
                    a = max(a, self.score)
                    if b <= a:
                        break
                # Minimizer: want min score
                else:
                    b = min(b, self.score)
                    if b <= a:
                        break

        # Case 3: No valid moves
        else:
            # Case 3a: game over (both sides have no valid moves)
            if self.game.get_valid_moves_white() == set() == self.game.get_valid_moves_black():

                # First, check if there is existing subtree
                move = ('GG', 'GG')
                subtree = self.find_subtree_by_move(move)

                # If subtree does not exist, create a new subtree
                if subtree is None:
                    game_copy = deepcopy(self.game)
                    game_copy.make_move(-1, -1)
                    subtree = GameTree(game_copy)
                    subtree.calculate_score()
                    # Add the newly-created subtree to the root
                    self.add_subtree(subtree)
                # If the subtree exists, do nothing
                else:
                    pass
            else:
                # First, check if there is existing subtree
                move = ('', '')
                subtree = self.find_subtree_by_move(move)
                # If subtree does not exist, create a new subtree
                if subtree is None:
                    game_copy = deepcopy(self.game)
                    game_copy.make_move(-1, -1)
                    subtree = GameTree(game_copy)
                    # Recurse into the paths
                    subtree.minimaxab(depth - 1, a, b)
                    subtree.calculate_score()
                    # Add the newly-created subtree to the root
                    self.add_subtree(subtree)

                # If the subtree exists, just recurse into it
                else:
                    # Recurse into the paths
                    subtree.minimaxab(depth - 1, a, b)
                    subtree.calculate_score()

                # Alpha-beta pruning: determine if we still need to create more subtrees
                # Maximizer: want max score
                if self.is_white_move:
                    a = max(a, self.score)
                    if b <= a:
                        return
                # Minimizer: want min score
                else:
                    b = min(b, self.score)
                    if b <= a:
                        return

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_white_move:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"
        move_desc = f'{self.move}: {self.score} -> {turn_desc}\n'
        s = '   ' * depth + move_desc
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def fulltree_to_txt(self) -> None:
        """This function returns a .txt file which contains a full game_tree of depth 5
        based on the current game state.
        """
        self.generate_moves_full(5)
        with open('fulltree_depth_5.txt', 'w') as file:
            # writer = txt.writer(file)
            file.writelines(self.__str__())

    def quicktree_to_txt(self) -> None:
        """This function returns a .txt file which contains a pruned game_tree of depth 5
        based on the current game state.
        """
        self.generate_moves_quick(5)
        with open('prunedtree_depth_5.txt', 'w') as file:
            # writer = txt.writer(file)
            file.writelines(self.__str__())
