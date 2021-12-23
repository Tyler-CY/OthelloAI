"""
Objective: This file contains the AI's players and also it is used to test to how well the AIs play
           against one another, note that these AI's are as described in the main.py, and have the
           following difficulty levels:
           - Beginner
           - Intermediate
           - Professional
           - Expert
           - Impossible

This file is Copyright (c) 2021 Chun Yin Yan and Gabriel Pais
Player AI and (testing) game engine
"""

import random
from copy import deepcopy

import Visualization    # DO NOT REMOVE THIS LINE
from GameTree_Game import GameTree
from Othello_Game import Othello


####################################################################################
# Computer Players/AI
####################################################################################
class Player:
    """
    An AI player class.

    Instance attributes:
        - color: which color this player plays
        - normal_depth: the depth of the GameTree generated before the cutoff
        - cutoff: the number of pieces on the board required to switch from normal_depth to
                    cutoff_depth, which changes the depth of the GameTree
        - rnd: the chance that the player will move randomly
        - gametree: the GameTree of the Player
    """
    color: int
    normal_depth: int
    cutoff: int
    cutoff_depth: int
    rnd: float
    gametree: GameTree

    def __init__(self, color: int, normal_depth: int, cutoff: int,
                 cutoff_depth: int, rnd: float) -> None:
        self.color = color
        self.normal_depth = normal_depth
        self.cutoff = cutoff
        self.cutoff_depth = cutoff_depth
        self.rnd = rnd

    def initialize_gametree(self, game: Othello):
        """
        Initialize the GameTree for this player.
        """
        raise NotImplementedError

    def cpu_make_move(self, game: Othello) -> tuple:
        """
        Return a valid move according to the current state of self.game.
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """
    A subclass of Player.

    An AI player which moves randomly.

    Instance attributes:
    - color: which color this player plays
    - normal_depth: the depth of the GameTree generated before the cutoff
    - cutoff: the number of pieces on the board required to switch from normal_depth to
                cutoff_depth, which changes the depth of the GameTree
    - rnd: the chance that the player will move randomly
    - gametree: the GameTree of the Player
    """
    color: int
    normal_depth: int
    cutoff: int
    cutoff_depth: int
    rnd: float
    gametree: GameTree

    def __init__(self, color: int, normal_depth: int = 0, cutoff: int = 0,
                 cutoff_depth: int = 0, rnd: float = 0) -> None:
        self.color = color
        self.normal_depth = normal_depth
        self.cutoff = cutoff
        self.cutoff_depth = cutoff_depth
        self.rnd = rnd

    def initialize_gametree(self, game: Othello):
        """
        Initialize the GameTree for this player.
        """
        self.gametree = GameTree(game=game)
        self.gametree.generate_moves_quick(self.normal_depth)

    def cpu_make_move(self, game: Othello) -> tuple:
        """
        Return a valid move according to the current state of self.game.
        """
        choices = list(game.get_valid_moves_now())
        if choices != []:
            choice = random.choice(choices)
            return choice
        else:
            return ('', '')


class SmartPlayerv2(Player):
    """
    A subclass of Player.

    An AI player which moves according to the current game state and its GameTree.

    Instance attributes:
    - color: which color this player plays
    - normal_depth: the depth of the GameTree generated before the cutoff
    - cutoff: the number of pieces on the board required to switch from normal_depth to
                cutoff_depth, which changes the depth of the GameTree
    - rnd: the chance that the player will move randomly
    - gametree: the GameTree of the Player
    """
    color: int
    normal_depth: int
    cutoff: int
    cutoff_depth: int
    rnd: float
    gametree: GameTree

    def __init__(self, color: int, normal_depth: int, cutoff: int,
                 cutoff_depth: int, rnd: float) -> None:
        self.color = color
        self.normal_depth = normal_depth
        self.cutoff = cutoff
        self.cutoff_depth = cutoff_depth
        self.rnd = rnd

    def initialize_gametree(self, game: Othello):
        """
        Initialize the GameTree for this player.
        """
        self.gametree = GameTree(game)
        self.gametree.generate_moves_quick(self.normal_depth)

    def cpu_make_move(self, game: Othello) -> tuple:
        """
        Return a valid move according to the current state of self.game.
        """
        # Step 1: Update self.gametree based on the current game state and the previous move.
        prev_move = game.previous_move
        # If this player starts first, then prev_move will be None
        if prev_move == ('START', 'START'):
            pass
        # Else, the other player will have played a move before
        # Note that the current game tree should have a root which contains
        # the move (the second last move of the game, in fact) made by THIS player;
        # the subtrees should contain the possible moves of the other player's last turn,
        # but it might NOT contain the previous move since the path may be pruned.
        else:
            # check if any of the subtrees has the previous move
            prev_tree = self.gametree.find_subtree_by_move(prev_move)

            # if found, then prev_tree is not None
            # The subtree will become self.gametree
            if prev_tree is not None:
                self.gametree = prev_tree

            # if not found, then create a new tree
            # game should be the current state of the game
            else:
                self.gametree = GameTree(game=game)

        # Step 2: Extend the Gametree
        # Check if cutoff is reached.
        if sum(game.score()) < self.cutoff:
            self.gametree.generate_moves_quick(self.normal_depth)
        else:
            self.gametree.generate_moves_quick(self.cutoff_depth)

        assert self.gametree.get_subtrees() != []

        # Step 3: Choose the best possible moves using self.gametree
        # If the Player is playing white:
        if self.color == 1:
            # If we choose a move from the gametree, choose the best possible move (highest score).
            if random.uniform(0, 1) > self.rnd:
                max_score = -100000
                for subtree in self.gametree.get_subtrees():
                    if subtree.score > max_score:
                        max_score = subtree.score
                        self.gametree = subtree

                assert self.gametree.is_white_move is False
                return self.gametree.move
            # If we choose a random move, choose a random move.
            else:
                valid_moves = self.gametree.game.get_valid_moves_now()
                if valid_moves != []:
                    move = random.choice(valid_moves)
                    wanted_tree = self.gametree.find_subtree_by_move(move)
                    if wanted_tree is not None:
                        self.gametree = wanted_tree
                    else:
                        game_copy = deepcopy(game)
                        game_copy.make_move(move[0], move[1])
                        self.gametree = GameTree(game=game_copy)
                else:
                    move = ('', '')
                    game_copy = deepcopy(game)
                    game_copy.make_move(move[0], move[1])
                    self.gametree = GameTree(game=game_copy)
                return move

        # If the Player is playing black:
        else:
            # If we choose a move from the gametree, choose the best possible move (highest score).
            if random.uniform(0, 1) > self.rnd:
                min_score = 100000
                for subtree in self.gametree.get_subtrees():
                    if subtree.score < min_score:
                        min_score = subtree.score

                        self.gametree = subtree
                        assert self.gametree.is_white_move is True

                assert self.gametree.is_white_move is True
                return self.gametree.move
            # If we choose a random move, choose a random move.
            else:
                valid_moves = self.gametree.game.get_valid_moves_now()
                if valid_moves != []:
                    move = random.choice(valid_moves)
                    wanted_tree = self.gametree.find_subtree_by_move(move)
                    if wanted_tree is not None:
                        self.gametree = wanted_tree
                    else:
                        game_copy = deepcopy(game)
                        game_copy.make_move(move[0], move[1])
                        self.gametree = GameTree(game=game_copy)
                else:
                    move = ('', '')
                    game_copy = deepcopy(game)
                    game_copy.make_move(move[0], move[1])
                    self.gametree = GameTree(game=game_copy)
                return move


####################################################################################
# Game Engine
####################################################################################
class GameEngine:
    """
    The simulator/game engine which simulates Othello games between two computer players.

    Instance Attributes:
        - white: The White Player
        - black: The Black Player
    """
    white: Player
    black: Player

    def __init__(self, white: Player, black: Player):
        self.white = white
        self.black = black

    def play(self) -> int:
        """
        Play a game of Othello
        """
        # Initialize the game, and the players
        game = Othello()
        self.white.initialize_gametree(game)
        self.black.initialize_gametree(game)

        # While the game is not finished (No winners yet)
        while game.get_winner() == -100:

            # Print the current score, and the difference in pieces
            # (Number of white pieces - Number of black pieces)
            white, black = game.score()[0], game.score()[1]
            print(f'{sum(game.score())}: {white}: {black}; Diff: {white - black}')

            # Make a move
            if not game.is_white_move:
                move = self.black.cpu_make_move(game)
                game.make_move(move[0], move[1])
            else:
                move = self.white.cpu_make_move(game)
                result = game.make_move(move[0], move[1])
                assert result is not False

        white, black = game.score()[0], game.score()[1]
        print(f'{sum(game.score())}: {white}: {black}; Diff: {white - black}')

        return game.get_winner()

    def play_many_games(self) -> dict:
        """
        Play 100 games of Othello between two computer players
        """
        win_count = {'WHITE': 0, 'BLACK': 0, 'DRAW': 0}

        for _ in range(0, 100):
            match = self.play()
            if match == 1:
                win_count['WHITE'] += 1
            elif match == -1:
                win_count['BLACK'] += 1
            else:
                win_count['DRAW'] += 1

            print(win_count)

        return win_count


# Testing
if __name__ == '__main__':
    b = RandomPlayer(-1)
    # b = SmartPlayerv2(-1, 2, 57, 7, 0.5)
    w = SmartPlayerv2(1, 4, 57, 4, 0)
    # w = ImpossiblePlayer(1, 2, 56, 3)

    Engine = GameEngine(white=w, black=b)
    Engine.play_many_games()
