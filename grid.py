import secrets
from typing import Self

import pygame

from cell import Cell


class MineManager:
    """Manager for mine placement and counting around cells.

    This class handles the placement of mines on the grid, ensuring that a specified
    cell is safe (does not contain a mine) and that the number of mines placed matches
    the specified count. It also counts the number of mines around each cell after
    mines are placed.
    """

    def __init__(self: Self, grid: "Grid") -> None:
        self.grid: Grid = grid
        self.cells: list[list[Cell]] = grid.cells

    def place_mines(self: Self, safe_x: int, safe_y: int) -> None:
        """Place mines on the grid, ensuring that the cell at (safe_x, safe_y) is safe.

        This method places mines randomly on the grid, avoiding the cell at (safe_x,
        safe_y) and its adjacent cells. It ensures that the number of mines placed
        equals the specified mines_count in the grid.

        Args:
            safe_x (int): The x-coordinate of the cell that should not contain a mine.
            safe_y (int): The y-coordinate of the cell that should not contain a mine.
        """
        forbidden: set[tuple[int, int]] = {
            (pos_x, pos_y)
            for pos_x in range(safe_x - 1, safe_x + 2)
            for pos_y in range(safe_y - 1, safe_y + 2)
            if 0 <= pos_x < self.grid.cell_num and 0 <= pos_y < self.grid.cell_num
        }
        candidates: list[tuple[int, int]] = [
            (pos_x, pos_y)
            for pos_x in range(self.grid.cell_num)
            for pos_y in range(self.grid.cell_num)
            if (pos_x, pos_y) not in forbidden
        ]
        for pos_x, pos_y in secrets.SystemRandom().sample(
            candidates, self.grid.mines_count
        ):
            self.cells[pos_x][pos_y].is_mine = True
        for pos_x in range(self.grid.cell_num):
            for pos_y in range(self.grid.cell_num):
                self.cells[pos_x][pos_y].mines_around = self.count_mines_around(
                    pos_x, pos_y
                )

    def count_mines_around(self: Self, pos_x: int, pos_y: int) -> int:
        """Count the number of mines around a given cell.

        This method counts the number of mines in the adjacent cells of the cell at
        (pos_x, pos_y). It checks all eight surrounding cells and returns the count.

        Args:
            pos_x (int): The x-coordinate of the cell to check.
            pos_y (int): The y-coordinate of the cell to check.

        Returns:
            int: The number of mines around the cell at (pos_x, pos_y).
        """
        return sum(
            self.cells[nx][ny].is_mine
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if 0 <= (nx := pos_x + dx) < self.grid.cell_num
            and 0 <= (ny := pos_y + dy) < self.grid.cell_num
        )


class RevealManager:
    def __init__(self: Self, grid: "Grid") -> None:
        self.grid = grid
        self.cells = grid.cells

    def reveal_cell(self: Self, pos_x: int, pos_y: int) -> bool:
        if not self.grid.mines_placed:
            self.grid.mines.place_mines(pos_x, pos_y)
            self.grid.mines_placed = True
        if self.cells[pos_x][pos_y].reveal():
            return True  # Hit a mine
        if self.cells[pos_x][pos_y].mines_around == 0:
            self.reveal_adjacent(pos_x, pos_y)
        return False

    def reveal_adjacent(self: Self, pos_x: int, pos_y: int) -> None:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = pos_x + dx, pos_y + dy
                if self._can_reveal(nx, ny):
                    self._reveal_cell(nx, ny)

    def check_win_condition(self: Self) -> bool:
        for row in self.grid.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def reveal_all_mines(self: Self) -> None:
        for row in self.grid.cells:
            for cell in row:
                if cell.is_mine:
                    cell.reveal()

    def _can_reveal(self: Self, pos_x: int, pos_y: int) -> bool:
        in_bounds_x = 0 <= pos_x < self.grid.cell_num
        in_bounds_y = 0 <= pos_y < self.grid.cell_num
        if not (in_bounds_x and in_bounds_y):
            return False

        cell: Cell = self.grid.cells[pos_x][pos_y]
        return not cell.is_revealed and not cell.is_mine

    def _reveal_cell(self: Self, pos_x: int, pos_y: int) -> None:
        cell: Cell = self.grid.cells[pos_x][pos_y]
        cell.reveal()
        if not cell.mines_around:
            self.reveal_adjacent(pos_x, pos_y)


class Grid:
    def __init__(
        self: Self, cell_size: int, cell_num: int, mines_count: int, shift: float
    ) -> None:
        self._cell_size = cell_size
        self.cell_num = cell_num
        self.mines_count = mines_count
        self._shift = shift
        self.cells = [
            [
                Cell(pos_x, pos_y, self._cell_size, self._shift)
                for pos_y in range(self.cell_num)
            ]
            for pos_x in range(self.cell_num)
        ]
        self.mines_placed = False

        # Gestionnaires séparés
        self.mines = MineManager(self)
        self.reveal = RevealManager(self)

    def draw(self: Self, screen: pygame.Surface) -> None:
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
