"""
Objective: This file creates our Pygame UI for the game, which allows humans to play against CPU of
           different difficulties. It also has a feedback system which tells the player how good
           their move was. And as a last item we have a hint button, which gives the player one
           possible best move.

This file is Copyright (c) 2021 Chun Yin Yan and Gabriel Pais
"""
import math
import random
from typing import Any

import pygame

import GameEngine_AI
from GameTree_Game import GameTree
from Othello_Game import Othello

# Initialize pygame
pygame.init()

# Initialize fonts
font_big = pygame.font.SysFont("monospace", 50)
font_small = pygame.font.SysFont("monospace", 25)
font_tiny = pygame.font.SysFont("monospace", 25)

# Pygame Display Settings
SWIDTH, SLENGTH = 1600, 900
FPS = 300

# If the player/move is 1, it means white is the Player who should move
IS_WHITE_MOVE = {1: True, -1: False}


def initialize_screen(screen_size: tuple[int, int], color: tuple[int, int, int]) -> pygame.Surface:
    """
    Initialize pygame display window.
    """
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption('Othello')
    screen = pygame.display.set_mode(screen_size)
    screen.fill(color)

    return screen


def main_menu(player_color: int) -> None:
    """
    Othello Game

    player_color: choose the player color 1 = white -1 = black 0 = random
    """

    # Initialize screen
    screen = initialize_screen((SWIDTH, SLENGTH), (200, 0, 0))
    clock = pygame.time.Clock()
    running = True

    # Get mouse_position
    pos = pygame.mouse.get_pos()

    # Game-Setup
    # Initialize player and computer colors
    if player_color == 1:
        cpu_color = -1
    elif player_color == -1:
        cpu_color = 1
    else:
        seed = random.uniform(0, 1)
        if seed < 0.5:
            player_color = 1
            cpu_color = -1
        else:
            player_color = -1
            cpu_color = 1

    # Initialize game
    game = Othello()
    past_moves = []
    start = 0

    # Initialize Computer Player (Default Settings)
    cpu = GameEngine_AI.SmartPlayerv2(cpu_color, 4, 57, 7, 0.5)
    cpu.initialize_gametree(game)
    # print(cpu.gametree)

    # Initialize buttons
    drawing = Drawing(screen, (100, 100, 600, 600))

    # Button 1: Grid_buttons
    grid_buttons = list(drawing.draw_grid_buttons(game.make_move).values())
    grid = ('START', 'START')

    # Draw game state
    game.draw_game_state(screen, (100, 100, 600, 600))

    # Button 2: CPU difficulty button
    text = font_big.render('AI Difficulty', True, (0, 0, 0))
    screen.blit(text, (10, 25))
    cpu_button = Button(screen, (255, 255, 255), (425, 15, 250, 75), None, None,
                        text=['Impossible', 'Expert', 'Professional', 'Intermediate', 'Beginner'],
                        text_cycle=1)
    cpu_button.draw()

    # Button 3: Hint button
    wanted_move = None
    hint_button = Button(screen, (255, 255, 255), (800, 15, 250, 75), None, None,
                         text=['HINT', str(wanted_move)], text_cycle=2)

    # Button 4: Color button
    color_cycle = 1 if cpu_color == 1 else 0
    color_button = Button(screen, (255, 255, 255), (1100, 15, 285, 75), None, None,
                          text=['CPU: BLACK', 'CPU: WHITE', 'CPU: RANDOM'], text_cycle=color_cycle)
    color_button.draw()

    # Begin Application
    while running:

        ############################################################################################
        # Update player and computer color according to color_button
        ############################################################################################
        if color_button.text_cycle % 3 == 0:
            wanted_player = 1
        elif color_button.text_cycle % 3 == 1:
            wanted_player = -1
        else:
            wanted_player = 0

        ############################################################################################
        # Find the best move (so we can give hints to the player using hint_button
        ############################################################################################
        if player_color == 1:
            best = -math.inf
        else:
            best = math.inf

        ############################################################################################
        # Update the following buttons: hint_button, restart_button, cpu_button
        ############################################################################################
        # Update hint_button (if hovered)
        hint_button.text = ['HINT', str(wanted_move)]
        if hint_button.hover(pos):
            hint_button.text_cycle = 1
            hint_button.draw()
        else:
            hint_button.text_cycle = 0
            hint_button.draw()

        # Update restart_button (if clicked)
        restart_button = Button(screen, (255, 255, 255), (1475, 0, 125, 40), main_menu,
                                wanted_player,
                                text=['RESTART'], text_cycle=1)
        restart_button.draw()

        ############################################################################################
        # Update the current player, game score, and winner
        ############################################################################################
        # Update the current player and game score
        if game.is_white_move:
            player = 'White'
        else:
            player = 'Black'
        text1 = font_big.render(f'Current Player: {player}', True, (0, 0, 0))
        text2 = font_big.render(f'White: {game.score()[0]} Black: {game.score()[1]}', True,
                                (0, 0, 0))
        screen.fill((200, 0, 0), (100, 725, 650, 200))
        screen.blit(text1, (100, 725))
        screen.blit(text2, (100, 775))

        ############################################################################################
        # Computer makes the first move if it is black
        ############################################################################################
        if not game.is_white_move and cpu_color == -1 and start == 0:
            pygame.display.flip()
            pygame.time.wait(1000)
            move = cpu.cpu_make_move(game)
            start = 1
            first_blood = game.make_move(move[0], move[1])
            w, b = game.score()
            past_moves.append((move, first_blood, w, b, 1))
            game.draw_game_state(screen, (100, 100, 600, 600))

        # Check winner and update if game is over
        if game.get_valid_moves_black() == set() == game.get_valid_moves_white():
            if game.get_winner() != -100:
                if game.get_winner() == 1:
                    text3 = font_big.render(f'WHITE WINS!', True,
                                            (255, 255, 255))
                elif game.get_winner() == -1:
                    text3 = font_big.render(f'BLACK WINS!', True,
                                            (255, 255, 255))
                else:
                    text3 = font_big.render(f'DRAW!', True,
                                            (255, 255, 255))

                screen.blit(text3, (100, 825))

        if game.get_winner() != -100:
            if game.get_winner() == 1:
                text3 = font_big.render(f'WHITE WINS!', True,
                                        (255, 255, 255))
            elif game.get_winner() == -1:
                text3 = font_big.render(f'BLACK WINS!', True,
                                        (255, 255, 255))
            else:
                text3 = font_big.render(f'DRAW!', True,
                                        (255, 255, 255))

            screen.blit(text3, (100, 825))

        ############################################################################################
        # Update strategic feedback system
        ############################################################################################
        drawing.draw_strategy_system()
        text = font_small.render(f'Your Previous Move: {grid}', True, (0, 0, 0))
        screen.blit(text, (850 - 50, 125))
        text = font_small.render(f'Best Move: {0, 0}', True, (0, 0, 0))
        screen.blit(text, (850 - 50, 160))
        text = font_small.render('Move', True, (0, 0, 0))
        screen.blit(text, (860 - 50, 200))
        text = font_small.render('Score', True, (0, 0, 0))
        screen.blit(text, (960 - 50, 200))
        text = font_small.render('Accuracy', True, (0, 0, 0))
        screen.blit(text, (1070 - 50, 200))
        text = font_small.render('Move', True, (0, 0, 0))
        screen.blit(text, (1250 - 50, 200))
        text = font_small.render('Score', True, (0, 0, 0))
        screen.blit(text, (1360 - 50, 200))
        text = font_small.render('Accuracy', True, (0, 0, 0))
        screen.blit(text, (1480 - 50, 200))

        for i in range(0, len(past_moves)):
            pm = past_moves
            text = font_tiny.render(
                f'{i + 1:}:{pm[i][0]}',
                True, (0, 0, 0))
            screen.blit(text, (800 - 50 + 400 * math.floor(i // 30), 225 + (i % 30) * 20))
            text = font_tiny.render(
                f'           {pm[i][2]}: {pm[i][3]}   {pm[i][4]}',
                True, (0, 0, 0))
            screen.blit(text, (800 - 50 + 400 * math.floor(i // 30), 225 + (i % 30) * 20))

        ############################################################################################
        # Check any input events
        ############################################################################################
        # run through every single event
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # events
            if event.type == pygame.QUIT:
                running = 0
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Update cpu_button, restart_button, color_button
                if len(past_moves) < 3:
                    if cpu_button.hover(pos):
                        cpu_button.text_cycle = cpu_button.execute1()
                        cpu_button.draw()

                        # Update computer difficulty
                        if cpu_button.text_cycle % 5 == 0:
                            cpu = GameEngine_AI.SmartPlayerv2(cpu_color, 4, 57, 7, 0.0)
                            cpu.initialize_gametree(game)
                        elif cpu_button.text_cycle % 5 == 1:
                            cpu = GameEngine_AI.SmartPlayerv2(cpu_color, 4, 57, 7, 0.2)
                            cpu.initialize_gametree(game)
                        elif cpu_button.text_cycle % 5 == 2:
                            cpu = GameEngine_AI.SmartPlayerv2(cpu_color, 3, 55, 5, 0.5)
                            cpu.initialize_gametree(game)
                        elif cpu_button.text_cycle % 5 == 3:
                            cpu = GameEngine_AI.SmartPlayerv2(cpu_color, 3, 55, 5, 0.7)
                            cpu.initialize_gametree(game)
                        elif cpu_button.text_cycle % 5 == 4:
                            cpu = GameEngine_AI.RandomPlayer(cpu_color, 0, 0, 0, 0)
                            cpu.initialize_gametree(game)

                if restart_button.hover(pos):
                    restart_button.execute1()
                if color_button.hover(pos):
                    color_button.text_cycle = color_button.execute1()
                    color_button.draw()

                # Update grid_button (according to which grid on the board is clicked)
                for i in range(0, len(grid_buttons)):
                    # If it is the human player's move ...
                    if grid_buttons[i].hover(pos) and IS_WHITE_MOVE[player_color] == \
                            game.is_white_move and game.get_winner() == -100:

                        # First, make a game tree to help determine move accuracy
                        # move accuracy determines how good the move made by the player is
                        gametree = GameTree(game)
                        gametree.generate_moves_quick(2)
                        scores = [s.score for s in gametree.get_subtrees()]
                        scores.sort()
                        # print(scores)

                        # Second, calculate possible accuracy range
                        max_score = 0
                        min_score = 0
                        if gametree.get_subtrees() != []:
                            max_score = max(s.score for s in gametree.get_subtrees())
                            min_score = min(s.score for s in gametree.get_subtrees())
                            maxmindiff = abs(max_score - min_score)
                        else:
                            maxmindiff = 0

                        # Press the grid and turn is the coordinate of that grid
                        turn = grid_buttons[i].execute()
                        # print(turn)
                        # turn[0] == 0 means if the grid clicked is a valid move
                        if turn[0] == 0 or turn[0] == -99:
                            # If we have no move, make_move return -99
                            if turn[0] == -99:
                                turn[0] = 0  # if we have no move, we capture 0 pieces
                            grid = turn[1]  # grid is a tuple = move
                            captures = turn[2]
                            w, b = game.score()

                            # Calculate accuracy of the move made
                            if maxmindiff == 0:
                                accuracy = 1
                            else:
                                move_tree = gametree.find_subtree_by_move(grid)
                                if move_tree is None:
                                    accuracy = 0.00
                                else:
                                    if player_color == 1:
                                        accuracy = abs(move_tree.score - min_score) / maxmindiff
                                    else:
                                        accuracy = abs(move_tree.score - max_score) / maxmindiff

                            # Play the move
                            past_moves.append((grid, captures, w, b, round(accuracy, 2)))

                            # Update the game board after human player moves
                            game.draw_game_state(screen, (100, 100, 600, 600))

                            # Calculate possible accuracy range of computer player
                            cpu_max_score = 0
                            cpu_min_score = 0
                            if cpu.gametree.get_subtrees() != []:
                                cpu_max_score = max(s.score for s in gametree.get_subtrees())
                                cpu_min_score = min(s.score for s in gametree.get_subtrees())
                                cpu_maxmindiff = abs(cpu_max_score - cpu_min_score)
                            else:
                                cpu_maxmindiff = 0
                            # print(cpu_maxmindiff)

                            # Update the current player
                            if cpu_color == -1:
                                current_color = 'Black'
                            else:
                                current_color = 'White'
                            text = font_big.render(f'Current Player: {current_color}',
                                                   True, (0, 0, 0))
                            screen.fill((200, 0, 0), (100, 725, 650, 200))
                            screen.blit(text, (100, 725))

                            # Computer calculates the best move and return that move
                            cpu_move = cpu.cpu_make_move(game)

                            # Calculate accuracy of the move made by computer
                            if cpu_maxmindiff == 0:
                                cpu_accuracy = 1
                            else:
                                move_tree = gametree.find_subtree_by_move(cpu_move)
                                if move_tree is None:
                                    cpu_accuracy = 0.00
                                else:
                                    if cpu_color == 1:
                                        cpu_accuracy = abs(
                                            move_tree.score - cpu_min_score) / cpu_maxmindiff
                                    else:
                                        cpu_accuracy = abs(
                                            move_tree.score - cpu_max_score) / cpu_maxmindiff

                            cpu_captures = game.make_move(cpu_move[0], cpu_move[1])
                            w, b = game.score()
                            past_moves.append(
                                (cpu_move, cpu_captures, w, b, round(cpu_accuracy, 2)))

                            # Find the current best move so we can give a hint to the player
                            for s in cpu.gametree.get_subtrees():
                                if player_color == 1:
                                    if s.score > best:
                                        wanted_move = s.move
                                else:
                                    if s.score < best:
                                        wanted_move = s.move

                            # update Surface
                            pygame.display.flip()
                            game.draw_game_state(screen, (100, 100, 600, 600))

        # update Surface
        if running:
            pygame.display.update()
            clock.tick(FPS)


####################################################################################
# helper functions/classes (Drawing Othello Gameboard)
####################################################################################
class Drawing:
    """
    All the functions related to drawing the Othello board on pygame.Surface
    Use together with Othello.draw_board

    Instance Attributes:
        - screen: pygame.Surface (the application window)
        - color: the commonly used color: [BLACK, WHITE, GREEN]
        - pos_size: the position of the button (A tuple)
                    (top-left-x-location, top-left-y-location, width, length)
    """
    screen: pygame.Surface
    color: list
    pos_size: tuple

    def __init__(self, screen: pygame.Surface, pos_size: tuple) -> None:
        self.color = [(0, 0, 0), (255, 255, 255), (0, 150, 0)]
        self.pos_size = pos_size
        self.screen = screen

    def draw_board(self, pos_size: tuple):
        """
        Draw a gameboard for Othello, no pieces
        """
        # Make background
        pygame.draw.rect(surface=self.screen, color=self.color[2], rect=pos_size)

        # Make Grid
        left, top, width, length = \
            self.pos_size[0], self.pos_size[1], self.pos_size[2] / 8, self.pos_size[3] / 8
        for i in range(0, 9):
            pygame.draw.line(surface=self.screen, color=self.color[0],
                             start_pos=(left + i * width, top),
                             end_pos=(left + i * width, top + length * 8),
                             width=4)
        for i in range(0, 8):
            text = font_small.render(str(i), True, (0, 0, 0))
            self.screen.blit(text, (left + i * width, top))
        for i in range(0, 9):
            pygame.draw.line(surface=self.screen, color=self.color[0],
                             start_pos=(left, top + i * length),
                             end_pos=(left + width * 8, top + i * length),
                             width=4)
        for i in range(0, 8):
            text = font_small.render(str(i), True, (0, 0, 0))
            self.screen.blit(text, (left, top + i * length))

    def draw_square(self, grid_yx: tuple):
        """
        Highlight the previous move with a square.
        """
        left, top, width, length = \
            self.pos_size[0], self.pos_size[1], self.pos_size[2] / 8, self.pos_size[3] / 8

        x, y = grid_yx[1], grid_yx[0]
        pygame.draw.line(surface=self.screen, color=(255, 0, 0),
                         start_pos=(left + x * width, top + y * length),
                         end_pos=(left + (x + 1) * width, top + y * length),
                         width=3)
        pygame.draw.line(surface=self.screen, color=(255, 0, 0),
                         start_pos=(left + x * width, top + y * length),
                         end_pos=(left + x * width, top + (y + 1) * length),
                         width=3)
        pygame.draw.line(surface=self.screen, color=(255, 0, 0),
                         start_pos=(left + (x + 1) * width, top + y * length),
                         end_pos=(left + (x + 1) * width, top + (y + 1) * length),
                         width=3)

        pygame.draw.line(surface=self.screen, color=(255, 0, 0),
                         start_pos=(left + x * width, top + (y + 1) * length),
                         end_pos=(left + (x + 1) * width, top + (y + 1) * length),
                         width=3)

    def draw_piece(self, color, grid_yx: tuple):
        """
        Draw a piece on the board
        """
        left, top, width, length = \
            self.pos_size[0], self.pos_size[1], self.pos_size[2] / 8, self.pos_size[3] / 8

        x, y = grid_yx[1], grid_yx[0]
        pygame.draw.circle(surface=self.screen, color=color,
                           center=(left + (x + 0.5) * width, top + (y + 0.5) * length),
                           radius=width * 0.4)
        pygame.draw.circle(surface=self.screen, color=(0, 0, 0),
                           center=(left + (x + 0.5) * width, top + (y + 0.5) * length),
                           radius=width * 0.45, width=3)

    def draw_grid_buttons(self, func) -> dict:
        """
        Draw a button on the Othello game board
        """
        left, top, width, length = \
            self.pos_size[0], self.pos_size[1], self.pos_size[2] / 8, self.pos_size[3] / 8

        buttons = {}

        for i in range(0, 8):
            for j in range(0, 8):
                grid_button = Button(screen=self.screen, color=(0, 0, 0),
                                     position=(left + i * width, top + j * length, width, length),
                                     func=func, args=(j, i), text=[], text_cycle=0)
                grid_button.draw()
                buttons['button{0}'.format((j, i))] = grid_button

        return buttons

    def draw_strategy_system(self) -> None:
        """
        Draw the background of the Strategy Feedback System
        """
        topx = self.pos_size[0] * 2 + self.pos_size[2] - 50
        topy = self.pos_size[1]
        width = SWIDTH - 25 - topx
        length = SLENGTH - 50 - topy
        pygame.draw.rect(self.screen, color=(0, 125, 255), rect=(topx, topy, width, length))


####################################################################################
# helper functions/classes (pygame)
####################################################################################
class Button:
    """
    Create a button. Note that button take only 1 function name and only 1 corresponding input

    Instance attributes:
    color: The color of the button
    position: the position and size of the button, represented in a list
            [pos_x, pos_y, width, length]
    func: name of function; this function will execute when the button is pressed
    args: the arguments of the function; the arguments will be passed to the function when the
            button is pressed
    text: a list of possible text showing on the button
    text_cycle: responsible for choosing which string from text is shown,
            decided by text[text_cycle]

    >>> test_button = Button(color=(0,0,0), position=(0,0,100,100), \
                        func=func, args=args, text=['text'], text_cycle=3)
    """
    screen: pygame.Surface
    color: tuple
    position: tuple
    func: Any
    args: Any
    text: list
    text_cycle: int

    def __init__(self, screen: pygame.Surface, color: tuple, position: tuple, func: Any, args: Any,
                 text: list, text_cycle: int):
        self.screen = screen
        self.color = color
        self.position = position
        self.func = func
        self.args = args
        self.text = text
        self.text_cycle = text_cycle

        self.draw()

    def draw(self) -> None:
        """
        Draw the button
        """
        pygame.draw.rect(self.screen, self.color, self.position)

        if self.text != []:
            current_text = self.text[self.text_cycle % len(self.text)]
            if self.text != '':
                font = pygame.font.SysFont('', int(self.position[3] * 0.75))
                text = font.render(current_text, True, (0, 0, 0))
                text_loc = (self.position[0] + (self.position[2] / 2 - text.get_width() / 2),
                            self.position[1] + (self.position[3] / 2 - text.get_height() / 2))
                self.screen.blit(text, text_loc)

    def hover(self, pos) -> bool:
        """
        Determine whether the mouse is on top of the button
        """
        if self.position[0] < pos[0] < self.position[0] + self.position[2] \
                and self.position[1] < pos[1] < self.position[1] + self.position[3]:
            return True
        return False

    def execute(self) -> Any:
        """
        This function is used exclusively with game.make_move, where
        self.func = game.make_move,
        self.args = (move[0], move[1]), where move is a valid move
        """
        success = self.func(self.args[0], self.args[1])

        if not success:
            return (1, self.args, success)
        else:
            return (0, self.args, success)

    def execute1(self) -> Any:
        """
        args will be passed to func, and the function will execute if the button is pressed
        """
        if self.func is None:
            pass
            return self.text_cycle + 1
        elif self.args is None:
            self.func()
            return self.text_cycle + 1
        else:
            self.func(self.args)
            return self.text_cycle + 1


# Testing
if __name__ == '__main__':
    main_menu(-1)
