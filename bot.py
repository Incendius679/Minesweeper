from typing import Any


class Bot:
    def __init__(self, grid: Any, top_bar: Any):
        self.grid = grid
        self.top_bar = top_bar

    def step(self) -> bool:
        for x in range(self.grid.cell_num):
            for y in range(self.grid.cell_num):
                cell = self.grid.cells[x][y]
                if cell.is_revealed and cell.mines_around > 0:
                    adj: list[tuple[int, int]] = []
                    flagged = 0
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.grid.cell_num and 0 <= ny < self.grid.cell_num:
                                adj_cell = self.grid.cells[nx][ny]
                                if not adj_cell.is_revealed and not adj_cell.is_flagged:
                                    adj.append((nx, ny))
                                if adj_cell.is_flagged:
                                    flagged += 1

                    # Règle 1 : flag
                    if len(adj) > 0 and len(adj) + flagged == cell.mines_around and self.top_bar.num_flags > 0:
                        nx, ny = adj[0]
                        self.grid.cells[nx][ny].toggle_flag()
                        self.top_bar.num_flags -= 1
                        return False

                    # Règle 2 : reveal
                    if flagged == cell.mines_around:
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < self.grid.cell_num and 0 <= ny < self.grid.cell_num:
                                    adj_cell = self.grid.cells[nx][ny]
                                    if not adj_cell.is_revealed and not adj_cell.is_flagged:
                                        if self.grid.reveal_cell(nx, ny):
                                            return True  # Mine révélée
                                        return False
        return False