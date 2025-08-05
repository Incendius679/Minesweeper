import random
from typing import Any

from Game.cell import Cell


class Grid:
    def __init__(
            self,
            width: int,
            height: float,
            cell_size: int,
            cell_num: int,
            mines_count: int,
            shift: float
            ) -> None:
        self.width: int = width
        self.height: float = height
        
        self.cell_size: int = cell_size
        self.cell_num: int = cell_num
        self.mines_count: int = mines_count
        self.shift: float = shift
        self.cells: list[list[Cell]] = [[
            Cell(x=x, y=y, size=self.cell_size, shift=self.shift)
            for y in range(0, self.cell_num)
            ] for x in range(0, self.cell_num)]
        self.mines_placed = False

    def place_mines(self, safe_x: int, safe_y: int) -> None:
        # Calculer les coordonnées interdites (safe + adjacentes)
        forbidden: set[tuple[int, int]] = set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = safe_x + dx, safe_y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    forbidden.add((nx, ny))

        mines_to_place: int = self.mines_count
        while mines_to_place > 0:
            x: int = random.randint(a=0, b=self.cell_num - 1)
            y: int = random.randint(a=0, b=self.cell_num - 1)
            if (x, y) not in forbidden and not self.cells[x][y].is_mine:
                self.cells[x][y].is_mine = True
                mines_to_place -= 1

        # Update the mines around count
        for x in range(self.cell_num):
            for y in range(self.cell_num):
                self.cells[x][y].mines_around = self.count_mines_around(x, y)

    def count_mines_around(self, x: int, y: int) -> int:
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    if self.cells[nx][ny].is_mine:
                        count += 1
        return count

    def reveal_cell(self, x: int, y: int) -> bool:
        if not self.mines_placed:
            self.place_mines(x, y)
            self.mines_placed = True
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
