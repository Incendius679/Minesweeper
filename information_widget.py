"""Create and handle the top bar of the Minesweeper game.

This module defines the `TopBar` class, which is responsible for displaying
the game score, elapsed time, number of flags, wins, and losses. It also
provides methods to update and draw the top bar, reset the game state, and
track wins and losses.
"""

from dataclasses import dataclass
from typing import Self

import pygame
from pygame.font import Font

from colors import BLACK, GRAY

Coordinate = tuple[float, float]


@dataclass
class UIPositions:
    """Positions for UI elements in the top bar.

    This dataclass holds the relative positions of the score, time,
    flags, wins, and losses in the top bar. Each position is defined as a
    tuple of floats representing the relative x and y coordinates.

    Attributes:
        score (Coordinate): Position of the score text.
        time (Coordinate): Position of the time text.
        flags (Coordinate): Position of the flags text.
        wins (Coordinate): Position of the wins text.
        losses (Coordinate): Position of the losses text.
    """

    score: Coordinate
    time: Coordinate
    flags: Coordinate
    wins: Coordinate
    losses: Coordinate


@dataclass
class GameStats:
    """Statistics for the Minesweeper game.

    This dataclass holds the game statistics such as score, wins, losses,
    and the number of flags. It is used to track the player's performance
    throughout the game. Those statistics can be updated as the game
    progresses, and will be displayed in the top bar.

    Attributes:
        score (int): The current score of the player.
        wins (int): The number of games won by the player.
        losses (int): The number of games lost by the player.
        num_flags (int): The number of flags available to the player.
        start_num_flags (int): The initial number of flags available to the player.
    """

    score: int
    wins: int
    losses: int
    num_flags: int
    start_num_flags: int


@dataclass
class GameTimer:
    """Timer for the Minesweeper game.

    This dataclass holds the start ticks and elapsed time for the game.
    It is used to track how long the player has been playing, which is
    displayed in the top bar. The timer starts when the game begins and
    updates as the game progresses.

    Attributes:
        start_ticks (int): The time when the game started, in milliseconds.
        elapsed_time (int): The total time elapsed since the game started, in seconds.
        is_paused (bool): Indicates whether the game is paused.
    """

    start_ticks: int
    elapsed_time: int
    is_paused: bool


class TopBar(pygame.Surface):
    """Manage the top bar of the Minesweeper game.

    This class inherits from `pygame.Surface` and is responsible for
    displaying the game score, elapsed time, number of flags, wins, and losses.

    Args:
        pygame (pygame): The Pygame module used for creating the game window.

    Attributes:
        _width (int): The width of the top bar.
        _height (float): The height of the top bar.
        _font_size (int): The size of the font used for displaying text.
        _font (Font): The Pygame font object used for rendering text.
        _start_num_flags (int): The initial number of flags available to the player.
        _positions (UIPositions): The positions of UI elements in the top bar.
        stats (GameStats): The game statistics being tracked.
        timer (GameTimer): The game timer tracking elapsed time.
    """

    def __init__(self: Self, width: int, height: float, num_flags: int) -> None:
        super().__init__((width, height))
        self._width: int = width
        self._height: float = height
        self._font_size: int = 36
        self._font: Font = pygame.font.SysFont(None, self._font_size)
        self._start_num_flags: int = num_flags
        self._positions: UIPositions = UIPositions(
            (0.1, 0.1),
            (0.1, 0.3),
            (0.1, 0.5),
            (0.1, 0.7),
            (0.5, 0.7),
        )
        self.stats: GameStats = GameStats(0, 0, 0, num_flags, num_flags)
        self.timer = GameTimer(
            pygame.time.get_ticks(),
            0,
            False,
        )

    def update(self: Self) -> None:
        """Update the top bar with the current game state.

        This method updates the elapsed time and redraws the top bar with
        the current game statistics. It should be called regularly to keep
        the top bar up to date with the game's progress.
        """

        if not self.timer.is_paused:
            current_time: int = pygame.time.get_ticks()
            self.timer.elapsed_time = (current_time - self.timer.start_ticks) // 1000

        self.draw()

    def draw(self: Self) -> None:
        """Draw the top bar with current statistics.

        This method fills the top bar with a gray background and draws the
        current game statistics such as score, elapsed time, number of flags,
        wins, and losses. It uses the Pygame font to render the text and
        positions the text according to the defined UI positions.
        """
        self.fill(GRAY)
        for label, value_label, pos in (
            ("Score", self.stats.score, self._positions.score),
            ("Time", self.timer.elapsed_time, self._positions.time),
            ("Flags", self.stats.num_flags, self._positions.flags),
            ("Wins", self.stats.wins, self._positions.wins),
            ("Losses", self.stats.losses, self._positions.losses),
        ):
            self.blit(
                self._font.render(f"{label}: {value_label}", True, BLACK),
                (pos[0] * self._width, pos[1] * self._height),
            )

    def reset(self: Self) -> None:
        """Reset the game state.

        This method resets the game statistics and timer to their initial
        values. It should be called when starting a new game or resetting the
        current game.
        """
        self.stats.num_flags = self._start_num_flags
        self.stats.score = 0
        self.timer.elapsed_time = 0
        self.timer.start_ticks = pygame.time.get_ticks()

    def add_win(self: Self) -> None:
        """Add a win to the game statistics.

        This method increments the number of wins in the game statistics.
        """
        self.stats.wins += 1

    def add_loss(self: Self) -> None:
        """Add a loss to the game statistics.

        This method increments the number of losses in the game statistics.
        """
        self.stats.losses += 1
