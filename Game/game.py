import pygame
from pygame.font import Font

from Game.bot import Bot
from Game.colors import *
from Game.grid import Grid
from Game.information_widget import TopBar

pygame.init()


class Game:
    def __init__(
            self,
            cell_num: int = 20,
            mines_count: int = 20,
            num_flags: int = 20
            ) -> None:
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.screen_width: int = self.screen.get_width()
        self.screen_height: int = self.screen.get_height()
        self.top_bar_height: float = 0.20 * self.screen_height
        self.grid_height: float = self.screen_height - self.top_bar_height
        
        self.grid_width: int = self.screen_width
        
        self.cell_num: int = cell_num
        self.cell_size: int = self.grid_width // self.cell_num
        self.mines_count: int = mines_count
        self.top_bar = TopBar(width=self.screen_width, height=self.top_bar_height, num_flags=num_flags)
        self.grid = Grid(width=self.grid_width, height=self.grid_height, cell_size=self.cell_size, cell_num=self.cell_num, mines_count=self.mines_count, shift=self.top_bar_height)
        self.bot = Bot(grid=self.grid, top_bar=self.top_bar)
        self.running = True
        self.paused = False
        self.game_over = False
        self.win = False  # Ajouté pour suivre la victoire
    


    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused: bool = not self.paused
                    self.top_bar.is_paused = self.paused
                    
                    if self.paused:
                        self.pause_time: int = pygame.time.get_ticks()
                    else:
                        # Adjust timer start ticks to account for the pause duration
                        paused_duration: int = pygame.time.get_ticks() - self.pause_time
                        self.top_bar.timer_start_ticks += paused_duration


                elif event.key == pygame.K_ESCAPE and self.game_over or self.win:
                    self.reset_game()


            elif event.type == pygame.MOUSEBUTTONDOWN and not self.paused and not self.game_over and not self.win:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_y > self.top_bar_height:  # Grid area
                    cell_x = mouse_x // self.cell_size
                    cell_y = (mouse_y - self.top_bar_height) // self.cell_size
                    cell_y = int(cell_y)
                    
                    if event.button == 1:  # Left click
                        if self.grid.reveal_cell(cell_x, cell_y):
                            self.handle_game_over()
                        else:
                            self.top_bar.score += 1

                        if self.grid.check_win_condition():
                            self.handle_win()
                            self.top_bar.score += 1000

                    elif event.button == 3:  # Right click
                        cell = self.grid.cells[cell_x][cell_y]
                        if not cell.is_flagged and self.top_bar.num_flags:
                            cell.toggle_flag()
                            self.top_bar.num_flags -= 1
                        elif cell.is_flagged:
                            cell.toggle_flag()
                            self.top_bar.num_flags += 1


    def update(self):
        if not self.paused and not self.game_over and not self.win:
            self.top_bar.update()
            if self.bot.step():
                self.handle_game_over()  # Le bot a révélé une mine
                return
            # Vérifie la victoire après le tour du bot
            if self.grid.check_win_condition():
                self.handle_win()
        
    def draw_pause(self):
        font = pygame.font.SysFont(None, 72)
        paused_text = font.render("Paused", True, GREEN)
        rect = paused_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(paused_text, rect)


    def draw_game_over(self) -> None:
        font: Font = pygame.font.SysFont(name=None, size=72)
        game_over_text: pygame.Surface = font.render(text="Game Over", antialias=True, color=RED)
        rect: pygame.Rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(source=game_over_text, dest=rect)


    
    def draw_win(self) -> None:
        font: Font = pygame.font.SysFont(name=None, size=72)
        game_over_text: pygame.Surface = font.render(text="You Win", antialias=True, color=GREEN)
        rect: pygame.Rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(source=game_over_text, dest=rect)


    def handle_game_over(self) -> None:
        self.top_bar.add_loss()
        self.reset_game()

    def handle_win(self) -> None:
        self.top_bar.add_win()
        self.reset_game()

    def draw(self) -> None:
        self.screen.fill(WHITE)
        self.top_bar.draw()
        self.screen.blit(self.top_bar, (0, 0))
        self.grid.draw(self.screen)
        if self.paused:
            self.draw_pause()
        pygame.display.flip()

    def reset_game(self):
        self.top_bar.reset()
        self.grid = Grid(self.grid_width, self.grid_height, self.cell_size, self.cell_num, self.mines_count, self.top_bar_height)
        self.bot = Bot(self.grid, self.top_bar)  # <-- Passe la top_bar au bot
        self.game_over = False
        self.paused = False
        self.win = False


    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            pygame.time.wait(100)
