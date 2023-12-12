#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module creates the race object.

Author: Jack Hangen
Created on: 12/11/2023
"""

from src.turtle_racer import TurtleRacer
import pygame
import numpy as np 

class Race:
    """
    A class representing a turtle race.

    Attributes:
        turtles (list): A list of TurtleRacer objects participating in the race.
        winner (bool): A flag to indicate if the race has a winner.

    Methods:
        start(y_max): Starts the race by positioning each turtle at a specific y-coordinate.
        update(surface): Updates the position of each turtle and renders them on the given surface.
        check_winner(x_max): Checks if any of the turtles have crossed the finish line.
        render_turtle(turtle, surface): Renders a turtle on the given surface.
    """

    def __init__(self, turtles = list[TurtleRacer]) -> None:
        """
        Initializes the Race class with a list of TurtleRacer objects.

        Args:
            turtles (list[TurtleRacer]): A list of TurtleRacer objects participating in the race.
        """
        self.turtles = turtles
        self.winner = False

    def start(self, y_max: int = 0):
        """
        Starts the race by setting the initial position of each turtle.

        The turtles are evenly spaced along the y-axis based on y_max and the number of turtles.

        Args:
            y_max (int, optional): The maximum y-coordinate for the starting positions. Defaults to 0.
        """
        for i, turtle in enumerate(self.turtles):
            turtle.start(max((y_max/len(self.turtles))*i+(y_max/len(self.turtles)/2), 0))

    def update(self, surface) -> None:
        """
        Updates the position of each turtle and renders them on the given surface.

        If a winner is not yet determined, each turtle's position is updated. All turtles are then rendered.

        Args:
            surface: The Pygame surface on which the turtles are rendered.
        """
        for turtle in self.turtles:
            if not self.winner:
                    turtle.update(np.random.normal(.5, 2)*0.1)

                    self.render_turtle(turtle, surface)
            else:
                self.render_turtle(turtle, surface)
                
    def check_winner(self, x_max: int = 1280) -> None:
        """
        Checks if any turtle has crossed the finish line to determine the winner.

        If a turtle's x-coordinate is greater than or equal to x_max, it's declared the winner.

        Args:
            x_max (int, optional): The x-coordinate representing the finish line. Defaults to 1280.
        """
        for i, turtle in enumerate(self.turtles):
            if turtle.pos[0] >= x_max:
                self.winner = True

    def render_turtle(self, turtle: TurtleRacer, surface: pygame.Surface) -> None:
        """
        Renders a turtle on the provided surface.

        Draws the turtle's body, head, legs, and a line representing its path.

        Args:
            turtle (TurtleRacer): The TurtleRacer object to be rendered.
            surface: The Pygame surface on which the turtle is rendered.
        """
        pygame.draw.circle(surface, turtle.color, turtle.pos, 10)

        pygame.draw.circle(surface, turtle.color, (turtle.pos[0] + 15, turtle.pos[1]), 5)

        leg_width, leg_height = 2, 5
        pygame.draw.rect(surface, turtle.color, (turtle.pos[0] - 5, turtle.pos[1] - 12, leg_width, leg_height)) 
        pygame.draw.rect(surface, turtle.color, (turtle.pos[0] + 8, turtle.pos[1] - 12, leg_width, leg_height)) 
        pygame.draw.rect(surface, turtle.color, (turtle.pos[0] - 5, turtle.pos[1] + 7, leg_width, leg_height))  
        pygame.draw.rect(surface, turtle.color, (turtle.pos[0] + 8, turtle.pos[1] + 7, leg_width, leg_height)) 

        pygame.draw.line(surface, turtle.color, (10, turtle.pos[1]), (turtle.pos[0], turtle.pos[1]), 2)
