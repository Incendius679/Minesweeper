import pygame

from Game.game import Game


def main(
    Width: float = 500,
    Height: float = 625,
    Title: str = "Minesweeper",
    difficulty: str = "Easy",
) -> None:
    """main Initializes and runs the Minesweeper game.

    This function sets up the game window, handles display settings, and
    creates a game instance based on the provided parameters.

    Parameters
    ----------
    Width : float, optional
        The width of the game window in pixels, by default 500
    Height : float, optional
        The height of the game window in pixels, by default 625
    Title : str, optional
        The title displayed on the game window, by default "Minesweeper"
    difficulty : str, optional
        The game difficulty, wich determines the size of the grid, the number
        of mines, and the number of flags. Valid options are "Easy", "Medium",
        and "Hard", by default "Easy"
    """
    difficulties: dict[str, tuple[int, int, int]] = {
        "Easy": (9, 10, 10),
        "Medium": (16, 40, 40),
        "Hard": (30, 160, 160),
    }
    size: int
    mine: int
    number_of_flags: int
    # Breaking the long line into multiple lines for better readability
    size, mine, number_of_flags = difficulties.get(
        difficulty, difficulties["Easy"]
    )
    pygame.display.set_mode(size=(Width, Height))
    pygame.display.set_caption(title=Title)
    Minesweeper = Game(size, mine, num_flags=number_of_flags)
    Minesweeper.run()


if __name__ == "__main__":
    main(difficulty="Hard")  # Change "Easy" to "Medium" or "Hard" as needed
