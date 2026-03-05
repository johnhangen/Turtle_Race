#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module creates the loop object.

Author: Jack Hangen
Created on: 12/11/2023
"""

from src.turtle_racer import TurtleRacer
from src.race import Race
from src.color_picker import ColorPickerScreen
from src.constants import *
import pygame


class Loop:
    """
    A class that encapsulates the main event loop for a Turtle Racer.

    This class manages the game's main loop, handling initialization, events, updating game state,
    rendering, and cleanup.

    Attributes:
        _display_surf (pygame.Surface): The main display surface for the game.
        _running (bool): Flag to keep the game running.
        _clock (pygame.time.Clock): Clock object for managing frame rate.
        size (tuple): The size of the window, specified as (width, height).
        racer (Race): Instance of the Race class to manage the turtle racers.
        state (str): Current game state — "color_picker" or "racing".
        color_picker (ColorPickerScreen): The pre-race color selection screen.
    """

    def __init__(self) -> None:
        """
        Initializes the Loop class with default values.
        """
        self._display_surf = None
        self._running = None
        self._clock = None
        self.size = self.width, self.height = 1280, 720

    def on_init(self) -> None:
        """
        Initializes the Pygame environment, display surface, game clock, and the turtle racers.

        Sets up the game window and creates instances of the Race and TurtleRacer classes.
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Turtle Racer")
        self._clock = pygame.time.Clock()
        self._running = True

        COLORS = [SUNSET_PURPLE, SUNSET_ORANGE, TWILIGHT_BLUE, PALE_YELLOW, ROSE_PINK, EVENING_SKY, GOLDEN_HUE, DEEP_RED, SOFT_PEACH, DARK_PURPLE]

        turtles = [TurtleRacer(color) for color in COLORS]
        self.racer = Race(turtles)
        self.color_picker = ColorPickerScreen(turtles, self.width, self.height)
        self.state = "color_picker"

    def on_event(self, event) -> None:
        """
        Handles events like quitting the game and restarting the race.

        Args:
            event (pygame.Event): The event to be processed.
        """
        if event.type == pygame.QUIT:
            self._running = False
        elif self.state == "color_picker":
            result = self.color_picker.handle_event(event)
            if result == "start":
                self.racer.start(self.height)
                self.racer.winner = False
                self.state = "racing"
        elif self.state == "racing":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.state = "color_picker"
                self.racer.winner = False

    def on_loop(self) -> None:
        """
        Contains the logic to be executed in each iteration of the game loop,
        like checking for a winner.
        """
        if self.state == "racing":
            self.racer.check_winner(self.width)

    def on_render(self) -> None:
        """
        Renders the current game state to the display surface and updates the display.
        """
        if self.state == "color_picker":
            self.color_picker.render(self._display_surf)
        else:
            self._display_surf.fill((255, 255, 255))
            self.racer.update(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self) -> None:
        """
        Cleans up the Pygame environment when the game is closing.
        """
        pygame.quit()

    def on_execute(self) -> None:
        """
        The main execution method for the game loop.

        This method sets up the game and then runs the main loop until the game is exited.
        """
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()
