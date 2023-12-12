#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module creates the turtle object.

Author: Jack Hangen
Created on: 12/11/2023
"""


class TurtleRacer:
    """
    A class representing a Turtle Racer in a simple racing game.

    Attributes:
        color (tuple): The RGB color of the turtle, defaulting to black (0, 0, 0).
        pos (tuple): The current position of the turtle, initialized as (0, 0).

    Methods:
        start(y): Sets the initial position of the turtle at the start of the race.
        update(x): Updates the turtle's position along the x-axis.
    """

    def __init__(self, color: tuple = (0, 0, 0)) -> None:
        """
        Constructs all the necessary attributes for the TurtleRacer object.

        Args:
            color (tuple, optional): The RGB color of the turtle. Defaults to (0, 0, 0).
        """
        self.color = color
        self.pos = (0, 0)

    def start(self, y: int = 0) -> None:
        """
        Sets the initial position of the turtle at the start of the race.

        The turtle's x-coordinate is set to 10, and the y-coordinate is set based on the input.

        Args:
            y (int, optional): The starting y-coordinate of the turtle. Defaults to 0.
        """
        self.pos = (10, y)

    def update(self, x: int = 0) -> None:
        """
        Updates the turtle's position along the x-axis.

        The turtle's x-coordinate is increased by the specified amount, keeping the y-coordinate unchanged.

        Args:
            x (int, optional): The amount to move the turtle along the x-axis. Defaults to 0.
        """
        self.pos = (self.pos[0] + x, self.pos[1])
