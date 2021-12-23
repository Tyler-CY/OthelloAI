"""
Objective: This file is used to initialize the gaming board for Othello, and update the state of the
           game,such as checking if the move is legal, to get the score and flip either black pieces
           or white ones, to draw the state of the game and other functions that represent
           rules of the game.

This file is Copyright (c) 2021 Chun Yin Yan and Gabriel Pais
"""
import pygame
from typing import Any

import Visualization


class Othello:
    """
    All the functions related to Othello.

    Note that the gameboard is define by a 8x8 list.
    to access a grid, we can write gameboard[row][col] or gameboard[i][j] or gameboard[y][x]

    Instance Attributes:
        - gameboard: the current state of the gameboard
        - is_white_move: whether it is white's turn to move
        - previous_move: the previous move of the game. Default value is ('START', 'START').

    """
    gameboard: list
    is_white_move: bool
    previous_move: tuple

    def __init__(self) -> None:
        self.gameboard = [[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, -1, 0, 0, 0],
                          [0, 0, 0, -1, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]]

        self.is_white_move = False
        self.previous_move = ('START', 'START')

    def draw_game_state(self, screen: pygame.Surface, pos_size: tuple) -> None:
        """
        Draw the current state of the game board.
        """
        # Get all valid moves
        valid_moves = self.get_valid_moves_now()

        # Draw the gameboard, using pygame
        board = Visualization.Drawing(screen, pos_size)
        board.draw_board(pos_size)
        for i in range(0, 8):
            for j in range(0, 8):
                if (i, j) == self.previous_move:
                    board.draw_square((i, j))
                if (i, j) in valid_moves and self.gameboard[i][j] == 0:
                    board.draw_piece((255, 0, 0), (i, j))
                    pass
                elif self.gameboard[i][j] == 0:
                    pass
                elif self.gameboard[i][j] == 1:
                    board.draw_piece(board.color[1], (i, j))
                else:
                    board.draw_piece(board.color[0], (i, j))

    def get_valid_moves_now(self) -> list:
        """
        Return all valid moves for the current player.
        """

        if self.is_white_move:
            return list(self.get_valid_moves_white())
        else:
            return list(self.get_valid_moves_black())

    def pass_turn(self) -> None:
        """
        If there are no valid moves for current player, pass turn to other player.
        """
        if self.get_valid_moves_now() == []:
            self.is_white_move = not self.is_white_move

    def make_move(self, y: Any, x: Any) -> Any:
        """
        Make move for the current color, and return the position of pieces captured
        """
        # If the current player has no valid moves AND no one is a winner,
        # pass the turn.
        if self.get_valid_moves_now() == [] or self.get_winner() != -100:
            self.is_white_move = not self.is_white_move
            self.previous_move = ('', '')
            return -99
        # If the current player is white
        elif self.is_white_move:
            # Only valid moves will be played
            if (y, x) in self.get_valid_moves_white():
                self.gameboard[y][x] = 1
                flips = self.flip_white(y, x)
                self.is_white_move = not self.is_white_move
                self.previous_move = (y, x)
                return flips
            # If move is not valid, gameboard will not change.
            else:
                return False
        else:
            # Only valid moves will be played
            if (y, x) in self.get_valid_moves_black():
                self.gameboard[y][x] = -1
                flips = self.flip_black(y, x)
                self.is_white_move = not self.is_white_move
                self.previous_move = (y, x)
                return flips
            # If move is not valid, gameboard will not change.
            else:
                return False

    def score(self) -> tuple:
        """
        Return the current score in a tuple: (Number of White pieces: Number of Black pieces)
        """
        white_count = 0
        black_count = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if self.gameboard[i][j] == 0:
                    pass
                elif self.gameboard[i][j] == 1:
                    white_count += 1
                else:
                    black_count += 1
        return (white_count, black_count)

    def get_winner(self) -> int:
        """
        Return the winner of the game as a number

        if value returned is 1, it means white wins.
        if value returned is -1, it means black wins.
        if value returned is 0, it means it is a draw.
        If value returned is -100, it means no winner is declared yet.
        """
        if self.full() or (self.get_valid_moves_white() == set() == self.get_valid_moves_black()):
            w, b = self.score()
            if w == b:
                return 0
            elif w > b:
                return 1
            else:
                return -1
        else:
            return -100

    def full(self) -> bool:
        """
        Check if the board has been fully filled.
        """
        for i in range(0, 8):
            for j in range(0, 8):
                if self.gameboard[i][j] == 0:
                    return False

        return True

    def print(self) -> Any:
        """
        Print the current state of the board in the console using pprint.
        """
        import pprint
        pprint.pprint(self.gameboard)

    #####################################################################
    # Helper functions 1
    #####################################################################
    def get_valid_moves_white(self) -> set:
        """
        Get valid moves for white
        """
        possible_moves = set()
        for i in range(0, 8):
            for j in range(0, 8):
                possible_moves = possible_moves.union(self.possible_move_white(i, j))

        return possible_moves

    def get_valid_moves_black(self) -> set:
        """
        Get valid moves for black
        """
        possible_moves = set()
        for i in range(0, 8):
            for j in range(0, 8):
                possible_moves = possible_moves.union(self.possible_move_black(i, j))

        return possible_moves

    #####################################################################
    # Helper functions 2
    #####################################################################
    def possible_move_white(self, y: int, x: int) -> set:
        """
        Return a list of possible moves for a specific grid self.gameboard[y = row][x = column]
        """
        possible_so_far = set()

        if self.gameboard[y][x] == 1:
            # check squares on same row
            # squares on the same row on the left
            for i in range(0, x):
                if self.gameboard[y][i] == 0 and \
                        all(self.gameboard[y][j] == -1 for j in range(i + 1, x)) and \
                        any(self.gameboard[y][j] == -1 for j in range(i + 1, x)):
                    possible_so_far = possible_so_far.union({(y, i)})

            # squares on the same row on the right
            for i in range(x + 1, 8):
                if self.gameboard[y][i] == 0 and \
                        all(self.gameboard[y][j] == -1 for j in range(x + 1, i)) and \
                        any(self.gameboard[y][j] == -1 for j in range(x + 1, i)):
                    possible_so_far = possible_so_far.union({(y, i)})

            # check squares on same column
            # squares on the same column on the top
            for i in range(0, y):
                if self.gameboard[i][x] == 0 and \
                        all(self.gameboard[j][x] == -1 for j in range(i + 1, y)) and \
                        any(self.gameboard[j][x] == -1 for j in range(i + 1, y)):
                    possible_so_far = possible_so_far.union({(i, x)})

            # squares on the same column on the bottom
            for i in range(y + 1, 8):
                if self.gameboard[i][x] == 0 and \
                        all(self.gameboard[j][x] == -1 for j in range(y + 1, i)) and \
                        any(self.gameboard[j][x] == -1 for j in range(y + 1, i)):
                    possible_so_far = possible_so_far.union({(i, x)})

            # check squares on first diagonal '\'
            # check squares on the left and on the top
            for i in range(1, min(x, y) + 1):
                if self.gameboard[y - i][x - i] == 0 and \
                        all(self.gameboard[y - j][x - j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x - j] == -1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y - i, x - i)})

            # check squares on the right and on the bottom
            for i in range(1, min(7 - x, 7 - y) + 1):
                if self.gameboard[y + i][x + i] == 0 and \
                        all(self.gameboard[y + j][x + j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x + j] == -1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y + i, x + i)})

            # check squares on first diagonal '/'
            # check squares on the left and on the bottom
            for i in range(1, min(7 - y, x) + 1):
                if self.gameboard[y + i][x - i] == 0 and \
                        all(self.gameboard[y + j][x - j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x - j] == -1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y + i, x - i)})

            # check squares on the right and on the top
            for i in range(1, min(y, 7 - x) + 1):
                if self.gameboard[y - i][x + i] == 0 and \
                        all(self.gameboard[y - j][x + j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x + j] == -1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y - i, x + i)})

        return possible_so_far

    def possible_move_black(self, y: int, x: int) -> set:
        """
        Return a list of possible moves for a specific grid self.gameboard[y = row][x = column]
        """
        possible_so_far = set()

        if self.gameboard[y][x] == -1:
            # check squares on same row
            # squares on the same row on the left
            for i in range(0, x):
                if self.gameboard[y][i] == 0 and \
                        all(self.gameboard[y][j] == 1 for j in range(i + 1, x)) and \
                        any(self.gameboard[y][j] == 1 for j in range(i + 1, x)):
                    possible_so_far = possible_so_far.union({(y, i)})
            # squares on the same row on the right
            for i in range(x + 1, 8):
                if self.gameboard[y][i] == 0 and \
                        all(self.gameboard[y][j] == 1 for j in range(x + 1, i)) and \
                        any(self.gameboard[y][j] == 1 for j in range(x + 1, i)):
                    possible_so_far = possible_so_far.union({(y, i)})

            # check squares on same column
            # squares on the same column on the top
            for i in range(0, y):
                if self.gameboard[i][x] == 0 and \
                        all(self.gameboard[j][x] == 1 for j in range(i + 1, y)) and \
                        any(self.gameboard[j][x] == 1 for j in range(i + 1, y)):
                    possible_so_far = possible_so_far.union({(i, x)})
            # squares on the same column on the bottom
            for i in range(y + 1, 8):
                if self.gameboard[i][x] == 0 and \
                        all(self.gameboard[j][x] == 1 for j in range(y + 1, i)) and \
                        any(self.gameboard[j][x] == 1 for j in range(y + 1, i)):
                    possible_so_far = possible_so_far.union({(i, x)})

            # check squares on first diagonal '\'
            # check squares on the left and on the top
            for i in range(1, min(x, y) + 1):
                if self.gameboard[y - i][x - i] == 0 and \
                        all(self.gameboard[y - j][x - j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x - j] == 1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y - i, x - i)})
            # check squares on the right and on the bottom
            for i in range(1, min(7 - x, 7 - y) + 1):
                if self.gameboard[y + i][x + i] == 0 and \
                        all(self.gameboard[y + j][x + j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x + j] == 1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y + i, x + i)})

            # check squares on first diagonal '/'
            # check squares on the left and on the bottom
            for i in range(1, min(7 - y, x) + 1):
                if self.gameboard[y + i][x - i] == 0 and \
                        all(self.gameboard[y + j][x - j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x - j] == 1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y + i, x - i)})
            # check squares on the right and on the top
            for i in range(1, min(y, 7 - x) + 1):
                if self.gameboard[y - i][x + i] == 0 and \
                        all(self.gameboard[y - j][x + j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x + j] == 1 for j in range(1, i)):
                    possible_so_far = possible_so_far.union({(y - i, x + i)})

        return possible_so_far

    def flip_white(self, y: int, x: int) -> int:
        """
        Only call flip with make_move
        flip the color of the pieces captured
        return how many opponent pieces are flipped
        """
        flips = 0

        if self.gameboard[y][x] == 1:
            # check squares on same row
            for i in range(0, x):
                if self.gameboard[y][i] == 1 and \
                        all(self.gameboard[y][j] == -1 for j in range(i + 1, x)) and \
                        any(self.gameboard[y][j] == -1 for j in range(i + 1, x)):
                    for j in range(i + 1, x):
                        self.gameboard[y][j] = 1
                        flips += 1
            for i in range(x + 1, 8):
                if self.gameboard[y][i] == 1 and \
                        all(self.gameboard[y][j] == -1 for j in range(x + 1, i)) and \
                        any(self.gameboard[y][j] == -1 for j in range(x + 1, i)):
                    for j in range(x + 1, i):
                        self.gameboard[y][j] = 1
                        flips += 1

            # check squares on same column
            for i in range(0, y):
                if self.gameboard[i][x] == 1 and \
                        all(self.gameboard[j][x] == -1 for j in range(i + 1, y)) and \
                        any(self.gameboard[j][x] == -1 for j in range(i + 1, y)):
                    for j in range(i + 1, y):
                        self.gameboard[j][x] = 1
                        flips += 1
            for i in range(y + 1, 8):
                if self.gameboard[i][x] == 1 and \
                        all(self.gameboard[j][x] == -1 for j in range(y + 1, i)) and \
                        any(self.gameboard[j][x] == -1 for j in range(y + 1, i)):
                    for j in range(y + 1, i):
                        self.gameboard[j][x] = 1
                        flips += 1

            # check squares on first diagonal '\'
            # check squares on the left and on the top
            for i in range(1, min(x, y) + 1):
                if self.gameboard[y - i][x - i] == 1 and \
                        all(self.gameboard[y - j][x - j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x - j] == -1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y - j][x - j] = 1
                        flips += 1
            # check squares on the right and on the bottom
            for i in range(1, min(7 - x, 7 - y) + 1):
                if self.gameboard[y + i][x + i] == 1 and \
                        all(self.gameboard[y + j][x + j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x + j] == -1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y + j][x + j] = 1
                        flips += 1

            # check squares on first diagonal '/'
            # check squares on the left and on the bottom
            for i in range(1, min(7 - y, x) + 1):
                if self.gameboard[y + i][x - i] == 1 and \
                        all(self.gameboard[y + j][x - j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x - j] == -1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y + j][x - j] = 1
                        flips += 1
            # check squares on the right and on the top
            for i in range(1, min(y, 7 - x) + 1):
                if self.gameboard[y - i][x + i] == 1 and \
                        all(self.gameboard[y - j][x + j] == -1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x + j] == -1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y - j][x + j] = 1
                        flips += 1

        return flips

    def flip_black(self, y: int, x: int) -> int:
        """
        Only call flip with make_move
        flip the color of the pieces captured
        return how many opponent pieces are flipped
        """
        flips = 0
        if self.gameboard[y][x] == -1:
            # check squares on same row
            for i in range(0, x):
                if self.gameboard[y][i] == -1 and \
                        all(self.gameboard[y][j] == 1 for j in range(i + 1, x)) and \
                        any(self.gameboard[y][j] == 1 for j in range(i + 1, x)):
                    for j in range(i + 1, x):
                        self.gameboard[y][j] = -1
                        flips += 1
            for i in range(x + 1, 8):
                if self.gameboard[y][i] == -1 and \
                        all(self.gameboard[y][j] == 1 for j in range(x + 1, i)) and \
                        any(self.gameboard[y][j] == 1 for j in range(x + 1, i)):
                    for j in range(x + 1, i):
                        self.gameboard[y][j] = -1
                        flips += 1

            # check squares on same column
            for i in range(0, y):
                if self.gameboard[i][x] == -1 and \
                        all(self.gameboard[j][x] == 1 for j in range(i + 1, y)) and \
                        any(self.gameboard[j][x] == 1 for j in range(i + 1, y)):
                    for j in range(i + 1, y):
                        self.gameboard[j][x] = -1
                        flips += 1
            for i in range(y + 1, 8):
                if self.gameboard[i][x] == -1 and \
                        all(self.gameboard[j][x] == 1 for j in range(y + 1, i)) and \
                        any(self.gameboard[j][x] == 1 for j in range(y + 1, i)):
                    for j in range(y + 1, i):
                        self.gameboard[j][x] = -1
                        flips += 1

            # check squares on first diagonal '\'
            # check squares on the left and on the top
            for i in range(1, min(x, y) + 1):
                if self.gameboard[y - i][x - i] == -1 and \
                        all(self.gameboard[y - j][x - j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x - j] == 1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y - j][x - j] = -1
                        flips += 1
            # check squares on the right and on the bottom
            for i in range(1, min(7 - x, 7 - y) + 1):
                if self.gameboard[y + i][x + i] == -1 and \
                        all(self.gameboard[y + j][x + j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x + j] == 1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y + j][x + j] = -1
                        flips += 1

            # check squares on first diagonal '/'
            # check squares on the left and on the bottom
            for i in range(1, min(7 - y, x) + 1):
                if self.gameboard[y + i][x - i] == -1 and \
                        all(self.gameboard[y + j][x - j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y + j][x - j] == 1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y + j][x - j] = -1
                        flips += 1
            # check squares on the right and on the top
            for i in range(1, min(y, 7 - x) + 1):
                if self.gameboard[y - i][x + i] == -1 and \
                        all(self.gameboard[y - j][x + j] == 1 for j in range(1, i)) and \
                        any(self.gameboard[y - j][x + j] == 1 for j in range(1, i)):
                    for j in range(1, i):
                        self.gameboard[y - j][x + j] = -1
                        flips += 1
        return flips


# Testing
if __name__ == '__main__':
    gg = Othello()
