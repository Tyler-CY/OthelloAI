"""
Final Project Title: Othello board game

Objective: This file initializes the Game Application, and lets the user select the AI's difficulty,
           and also to test how well two AI's play against each other by running ai_test function.
           Run this file to access Othello Game Application and Othello Computer Comparison Test,
           and generate the GameTree text files.

By: Chun Yin Yan and Gabriel Pais

This file is Copyright (c) 2021 Chun Yin Yan and Gabriel Pais
"""
from Visualization import main_menu
from GameEngine_AI import SmartPlayerv2, GameEngine
from GameTree_Game import GameTree


# Available White CPU Players
Impossible_W = SmartPlayerv2(1, 4, 57, 7, 0.01)
Expert_W = SmartPlayerv2(1, 4, 57, 7, 0.15)
Professional_W = SmartPlayerv2(1, 3, 55, 5, 0.23)
Intermediate_W = SmartPlayerv2(1, 3, 55, 5, 0.30)
Beginner_W = SmartPlayerv2(1, 1, 1, 1, 1)

# Available Black CPU Players
Impossible_B = SmartPlayerv2(-1, 4, 57, 7, 0.1)
Expert_B = SmartPlayerv2(-1, 4, 57, 7, 0.15)
Professional_B = SmartPlayerv2(-1, 3, 55, 5, 0.23)
Intermediate_B = SmartPlayerv2(-1, 3, 55, 5, 0.30)
Beginner_B = SmartPlayerv2(-1, 1, 1, 1, 1)


def interactive() -> None:
    """
    Start the Othello Application where human can play against the computer of different
    difficulties.
    """
    main_menu(-1)


def ai_test(white_player: SmartPlayerv2, black_player: SmartPlayerv2) -> dict:
    """
    This is test shows the differences in "cleverness" of the AIs.

    Choose the players from the Available White/Black CPU Players on the top of this file.
    """
    engine = GameEngine(white_player, black_player)
    return engine.play_many_games()


if __name__ == '__main__':
    game = GameTree()
    game.fulltree_to_txt()
    game.quicktree_to_txt()
    interactive()
