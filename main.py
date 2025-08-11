"""Main entry point for the Minesweeper game.

Initializes the game with specified dimensions, title, and difficulty.
"""

from typing import Literal

import pygame

from game import Game


def main(
    width: float,
    height: float,
    title: str,
    difficulty: Literal["Easy", "Medium", "Hard"],
) -> None:
    """The main function to start the Minesweeper game.

    This function initializes the game window, sets the title, sets the
    difficulty and starts the game.

    Args:
        width (float): Determines the width of the game window.
        height (float): Determines the height of the game window.
        title (str): Determines the title of the game window.
        difficulty (Literal["Easy", "Medium", "Hard"]): Determines the
            difficulty level of the game.
    """
    difficulties: dict[str, tuple[int, int, int]] = {
        "Easy": (9, 10, 10),
        "Medium": (16, 40, 40),
        "Hard": (30, 160, 160),
    }
    size: int
    mine: int
    number_of_flags: int
    size, mine, number_of_flags = difficulties.get(difficulty, difficulties["Easy"])
    pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    minesweeper: Game = Game(size, mine, number_of_flags)
    minesweeper.run()


SIZE_RATIO: tuple[Literal[4], Literal[5]] = (4, 5)
SIZE_MULTIPLIER: float = 125.0

if __name__ == "__main__":
    main(
        SIZE_RATIO[0] * SIZE_MULTIPLIER,
        SIZE_RATIO[1] * SIZE_MULTIPLIER,
        "Minesweeper",
        "Hard",
    )
