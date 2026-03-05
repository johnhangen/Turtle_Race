#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module creates the color picker screen shown before the race.

Author: Jack Hangen
"""

import pygame
from src.constants import (
    SUNSET_PURPLE, SUNSET_ORANGE, TWILIGHT_BLUE, PALE_YELLOW, ROSE_PINK,
    EVENING_SKY, GOLDEN_HUE, DEEP_RED, SOFT_PEACH, DARK_PURPLE
)

PALETTE = [
    SUNSET_PURPLE, SUNSET_ORANGE, TWILIGHT_BLUE, PALE_YELLOW, ROSE_PINK,
    EVENING_SKY, GOLDEN_HUE, DEEP_RED, SOFT_PEACH, DARK_PURPLE,
    (220, 50, 50),    # Red
    (50, 180, 50),    # Green
    (50, 50, 220),    # Blue
    (0, 200, 200),    # Cyan
    (200, 0, 200),    # Magenta
    (230, 230, 0),    # Yellow
    (255, 255, 255),  # White
    (0, 0, 0),        # Black
]

SWATCH_SIZE = 40
SWATCH_PADDING = 8
PALETTE_COLS = 6

TURTLE_ROW_HEIGHT = 60
TURTLE_LIST_X = 60
TURTLE_LIST_START_Y = 80

START_BTN_WIDTH = 200
START_BTN_HEIGHT = 50


class ColorPickerScreen:
    """
    A pre-race screen allowing the user to customize each turtle's color.

    Attributes:
        turtles (list): The TurtleRacer objects whose colors can be changed.
        selected (int or None): Index of the currently selected turtle.
        width (int): Screen width.
        height (int): Screen height.
    """

    def __init__(self, turtles: list, width: int = 1280, height: int = 720) -> None:
        self.turtles = turtles
        self.selected = None
        self.width = width
        self.height = height
        self._font_large = None
        self._font_med = None
        self._font_small = None

    def _ensure_fonts(self):
        if self._font_large is None:
            self._font_large = pygame.font.SysFont(None, 48)
            self._font_med = pygame.font.SysFont(None, 30)
            self._font_small = pygame.font.SysFont(None, 22)

    def _turtle_row_rect(self, index: int) -> pygame.Rect:
        y = TURTLE_LIST_START_Y + index * TURTLE_ROW_HEIGHT
        return pygame.Rect(TURTLE_LIST_X - 10, y - 5, 420, TURTLE_ROW_HEIGHT - 8)

    def _swatch_rect(self, index: int) -> pygame.Rect:
        col = index % PALETTE_COLS
        row = index // PALETTE_COLS
        palette_x = self.width - (PALETTE_COLS * (SWATCH_SIZE + SWATCH_PADDING)) - 40
        palette_y = 120
        x = palette_x + col * (SWATCH_SIZE + SWATCH_PADDING)
        y = palette_y + row * (SWATCH_SIZE + SWATCH_PADDING)
        return pygame.Rect(x, y, SWATCH_SIZE, SWATCH_SIZE)

    def _start_btn_rect(self) -> pygame.Rect:
        x = (self.width - START_BTN_WIDTH) // 2
        y = self.height - START_BTN_HEIGHT - 30
        return pygame.Rect(x, y, START_BTN_WIDTH, START_BTN_HEIGHT)

    def handle_event(self, event) -> str | None:
        """
        Handle a pygame event.

        Returns:
            "start" if the Start Race button was clicked, else None.
        """
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None

        pos = event.pos

        # Check turtle list clicks
        for i in range(len(self.turtles)):
            if self._turtle_row_rect(i).collidepoint(pos):
                self.selected = i
                return None

        # Check color swatch clicks
        if self.selected is not None:
            for i, color in enumerate(PALETTE):
                if self._swatch_rect(i).collidepoint(pos):
                    self.turtles[self.selected].color = color
                    return None

        # Check Start Race button
        if self._start_btn_rect().collidepoint(pos):
            return "start"

        return None

    def render(self, surface: pygame.Surface) -> None:
        """Draw the full color picker UI onto surface."""
        self._ensure_fonts()
        surface.fill((30, 30, 30))

        # Title
        title = self._font_large.render("Customize Turtle Colors", True, (255, 255, 255))
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 20))

        # Turtle list
        list_label = self._font_med.render("Turtles  (click to select)", True, (200, 200, 200))
        surface.blit(list_label, (TURTLE_LIST_X - 10, 55))

        for i, turtle in enumerate(self.turtles):
            row_rect = self._turtle_row_rect(i)
            row_y_center = row_rect.y + row_rect.height // 2

            # Highlight selected turtle
            if i == self.selected:
                pygame.draw.rect(surface, (80, 80, 80), row_rect, border_radius=6)
                pygame.draw.rect(surface, (220, 220, 220), row_rect, width=2, border_radius=6)
            else:
                pygame.draw.rect(surface, (50, 50, 50), row_rect, border_radius=6)

            # Draw mini turtle body
            body_x = TURTLE_LIST_X + 20
            pygame.draw.circle(surface, turtle.color, (body_x, row_y_center), 10)
            pygame.draw.circle(surface, turtle.color, (body_x + 15, row_y_center), 5)
            leg_w, leg_h = 2, 5
            for lx in (body_x - 5, body_x + 8):
                pygame.draw.rect(surface, turtle.color, (lx, row_y_center - 12, leg_w, leg_h))
                pygame.draw.rect(surface, turtle.color, (lx, row_y_center + 7, leg_w, leg_h))

            # Label
            label = self._font_med.render(f"Turtle {i + 1}", True, (230, 230, 230))
            surface.blit(label, (TURTLE_LIST_X + 50, row_y_center - label.get_height() // 2))

        # Palette panel
        palette_label = self._font_med.render("Color Palette", True, (200, 200, 200))
        palette_x = self._swatch_rect(0).x
        surface.blit(palette_label, (palette_x, 85))

        for i, color in enumerate(PALETTE):
            rect = self._swatch_rect(i)
            pygame.draw.rect(surface, color, rect, border_radius=5)

            # Outline selected turtle's current color
            if self.selected is not None and self.turtles[self.selected].color == color:
                pygame.draw.rect(surface, (255, 255, 255), rect, width=3, border_radius=5)
            else:
                pygame.draw.rect(surface, (100, 100, 100), rect, width=1, border_radius=5)

        # Palette hint
        if self.selected is None:
            hint = self._font_small.render("Select a turtle on the left, then pick a color.", True, (160, 160, 160))
        else:
            hint = self._font_small.render(f"Turtle {self.selected + 1} selected — click a swatch to change its color.", True, (160, 210, 160))
        surface.blit(hint, (palette_x, self._swatch_rect(len(PALETTE) - 1).bottom + 14))

        # Start Race button
        btn_rect = self._start_btn_rect()
        pygame.draw.rect(surface, (60, 160, 60), btn_rect, border_radius=8)
        btn_label = self._font_large.render("Start Race", True, (255, 255, 255))
        surface.blit(btn_label, (btn_rect.centerx - btn_label.get_width() // 2,
                                  btn_rect.centery - btn_label.get_height() // 2))
