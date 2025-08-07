from typing import Self

import pygame
from pygame.font import Font

from colors import BLACK
from colors import GRAY


class TopBar(pygame.Surface):
    def __init__(
            self: Self,
            width: int,
            height: float,
            num_flags: int
        ) -> None:
        super().__init__((width, height))
        self._width: int = width
        self._height: float = height
        self.score: int = 0
        self.is_paused: bool = False
        self._elapsed_time: int = 0
        self.timer_start_ticks: int = pygame.time.get_ticks()
        self._FONT_SIZE: int = 36
        self._font: Font = pygame.font.SysFont(None, self._FONT_SIZE)
        self._start_num_flags: int = num_flags
        self.num_flags: int = num_flags
        self._wins: int = 0
        self._losses: int = 0
        self._SCORE_POS: tuple[float, float] = (0.1, 0.1)
        self._TIME_POS: tuple[float, float] = (0.1, 0.3)
        self._FLAGS_POS: tuple[float, float] = (0.1, 0.5)
        self._WINS_POS: tuple[float, float] = (0.1, 0.7)
        self._LOSSES_POS: tuple[float, float] = (0.5, 0.7)

    def update(self: Self) -> None:
        if not self.is_paused:
            current_time: int = pygame.time.get_ticks()
            self._elapsed_time = (
                current_time - self.timer_start_ticks
                ) // 1000

        self.draw()

    def draw(self: Self) -> None:
        self.fill(GRAY)
        score_text: pygame.Surface = self._font.render(
            f'Score: {self.score}',
            True,
            BLACK
            )
        time_text: pygame.Surface = self._font.render(
            f'Time: {self._elapsed_time}',
            True,
            BLACK
            )
        num_flags_text: pygame.Surface = self._font.render(
            f'Flags: {self.num_flags}',
            True,
            BLACK
            )
        wins_text: pygame.Surface = self._font.render(
            f'Wins: {self._wins}',
            True,
            BLACK
            )
        losses_text: pygame.Surface = self._font.render(
            f'Losses: {self._losses}',
            True,
            BLACK
            )
        self.blit(
            score_text,
            (
                self._SCORE_POS[0]*self._width,
                self._SCORE_POS[1]*self._height
                )
            )
        self.blit(
            time_text,
            (
                self._TIME_POS[0]*self._width,
                self._TIME_POS[1]*self._height
                )
            )
        self.blit(
            num_flags_text,
            (
                self._FLAGS_POS[0]*self._width,
                self._FLAGS_POS[1]*self._height
                )
            )
        self.blit(
            wins_text,
            (
                self._WINS_POS[0]*self._width,
                self._WINS_POS[1]*self._height
                )
            )
        self.blit(
            losses_text,
            (
                self._LOSSES_POS[0]*self._width,
                self._LOSSES_POS[1]*self._height
                )
            )

    def reset(self: Self) -> None:
        self.num_flags = self._start_num_flags
        self.score = 0
        self._elapsed_time = 0
        self.timer_start_ticks = pygame.time.get_ticks()

    def add_win(self: Self) -> None:
        self._wins += 1

    def add_loss(self: Self) -> None:
        self._losses += 1
