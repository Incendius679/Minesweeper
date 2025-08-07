import secrets
from typing import Any, Self

from cell import Cell


class Grid:
    def __init__(
            self: Self,
            cell_size: int,
            cell_num: int,
            mines_count: int,
            shift: float
            ) -> None:
        self._cell_size = cell_size
        self.cell_num = cell_num
        self._mines_count = mines_count
        self._shift = shift
        self.cells = [[
            Cell(pos_x, pos_y, self._cell_size, self._shift)
            for pos_y in range(0, self.cell_num)
            ] for pos_x in range(0, self.cell_num)]
        self._mines_placed = False

    def place_mines(self: Self, safe_x: int, safe_y: int) -> None:
        forbidden = {
            (safe_x + dx, safe_y + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if 0 <= safe_x + dx < self.cell_num
            and 0 <= safe_y + dy < self.cell_num
        }

        mines_to_place = self._mines_count
        while mines_to_place > 0:
            pos_x = secrets.randbelow(self.cell_num)
            pos_y = secrets.randbelow(self.cell_num)
            if (pos_x, pos_y) not in forbidden \
                    and not self.cells[pos_x][pos_y].is_mine:
                self.cells[pos_x][pos_y].is_mine = True
                mines_to_place -= 1

        # Update the mines around count
        for pos_x in range(self.cell_num):
            for pos_y in range(self.cell_num):
                self.cells[pos_x][pos_y].mines_around = (
                    self.count_mines_around(pos_x, pos_y)
                    )

    def count_mines_around(self: Self, pos_x: int, pos_y: int) -> int:
        neighbor_coords = [
            (pos_x + dx, pos_y + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
        ]

        count = sum(
            1
            for nx, ny in neighbor_coords
            if 0 <= nx < self.cell_num
            and 0 <= ny < self.cell_num and self.cells[nx][ny].is_mine
        )
        return count

    def reveal_cell(self, x: int, y: int) -> bool:
        if not self._mines_placed:
            self.place_mines(x, y)
            self._mines_placed = True
        if self.cells[x][y].reveal():
            return True  # Hit a mine
        if self.cells[x][y].mines_around == 0:
            self.reveal_adjacent(x, y)
        return False

    def reveal_adjacent(self, x: int, y: int) -> None:
        stack = [(x, y)] 
        while stack:
            cx, cy = stack.pop()
            
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                        cell = self.cells[nx][ny]
                        if not cell.is_revealed and not cell.is_mine:
                            cell.reveal()

                            if cell.mines_around == 0:
                                stack.append((nx, ny)) 

    def check_win_condition(self) -> bool:
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def reveal_all_mines(self) -> None:
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.reveal()

    def draw(self, screen: Any) -> None:
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
