import pygame
from pygame.font import Font

from Game.colors import BLACK, GRAY


class TopBar(pygame.Surface):
    def __init__(self, width: int, height: float, num_flags: int) -> None:
        super().__init__(size=(width, height))
        self._width: int = width
        self._height: float = height
        self.score = 0
        self.is_paused = False
        self._elapsed_time = 0
        self.timer_start_ticks: int = pygame.time.get_ticks()
        self.font: Font = pygame.font.SysFont(name=None, size=36)  # noqawps432
        self._start_num_flags: int = num_flags
        self.num_flags: int = num_flags
        self.wins = 0
        self.losses = 0

    def update(self) -> None:
        if not self.is_paused:
            current_time: int = pygame.time.get_ticks()
            self._elapsed_time: int = (
                current_time - self.timer_start_ticks
                ) // 1000

        self.draw()

    def draw(self) -> None:
        self.fill(color=GRAY)
        score_text: pygame.Surface = self.font.render(
            f'Score: {self.score}',
            True,
            BLACK
            )
        time_text: pygame.Surface = self.font.render(
            f'Time: {self._elapsed_time}',
            True,
            BLACK
            )
        num_flags_text: pygame.Surface = self.font.render(
            f'Flags: {self.num_flags}',
            True,
            BLACK
            )
        wins_text: pygame.Surface = self.font.render(
            f'Wins: {self.wins}',
            True,
            BLACK
            )
        losses_text: pygame.Surface = self.font.render(
            f'Losses: {self.losses}',
            True,
            BLACK
            )
        self.blit(
            source=score_text,
            dest=(0.1*self._width, 0.1*self._height)
            )
        self.blit(
            source=time_text,
            dest=(0.1*self._width, 0.3*self._height)  # noqawps432
            )
        self.blit(
            source=num_flags_text,
            dest=(0.1*self._width, 0.5*self._height)
            )
        self.blit(
            source=wins_text,
            dest=(0.1*self._width, 0.7*self._height)  # noqawps432
            )
        self.blit(
            source=losses_text,
            dest=(0.5*self._width, 0.7*self._height)  # noqawps432
            )

    def reset(self) -> None:
        self.num_flags = self._start_num_flags
        self.score = 0
        self._elapsed_time = 0
        self.timer_start_ticks = pygame.time.get_ticks()

    def add_win(self) -> None:
        self.wins += 1

    def add_loss(self) -> None:
        self.losses += 1
