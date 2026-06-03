"""
Módulo intro_screen.py — Pantalla de introducción narrativa.

Muestra el texto de la historia antes de comenzar el juego.
El jugador presiona ENTER para continuar al juego.
"""

import math
import pygame
from ui.base_screen import BaseScreen
from systems.constants import (
    STATE_PLAYING, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_WHITE, COLOR_GOLD, COLOR_LIGHT_GRAY,
    INTRO_TEXT,
)
from systems.asset_manager import assets


class IntroScreen(BaseScreen):
    """
    Pantalla de introducción narrativa del juego.

    Muestra el texto de la historia con animación de
    aparición letra por letra (typewriter effect).

    Attributes:
        _text_lines (list): Líneas del texto de introducción.
        _display_chars (float): Caracteres totales revelados hasta ahora.
        _type_speed (float): Caracteres por segundo del efecto typewriter.
        _blink_timer (float): Temporizador para parpadeo del cursor.
        _ready (bool): Si se puede continuar al juego.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager)
        self._text_lines: list = INTRO_TEXT
        self._total_chars: int = sum(len(line) for line in INTRO_TEXT)
        self._display_chars: float = 0.0
        self._type_speed: float = 40.0  # Caracteres por segundo
        self._blink_timer: float = 0.0
        self._ready: bool = False
        self._time: float = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        ENTER: si el texto aún aparece, lo muestra completo.
        Si ya está completo, continúa al juego.
        ESC: va directamente al juego.
        """
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if not self._ready:
                # Mostrar todo el texto de inmediato
                self._display_chars = float(self._total_chars)
                self._ready = True
            else:
                # Continuar al juego
                self.state_manager.change_state(STATE_PLAYING)

        elif event.key == pygame.K_ESCAPE:
            self.state_manager.change_state(STATE_PLAYING)

    def update(self, delta_time: float) -> None:
        """Actualiza el efecto typewriter."""
        self._time += delta_time
        self._blink_timer += delta_time

        if not self._ready:
            self._display_chars += self._type_speed * delta_time
            if self._display_chars >= self._total_chars:
                self._display_chars = float(self._total_chars)
                self._ready = True

    def draw(self) -> None:
        """Dibuja la pantalla de introducción con el efecto typewriter."""
        self.draw_gradient_background()

        # ── Efecto de partículas decorativas ──
        self._draw_particles()

        # ── Panel central de texto ──
        panel_w = 640
        panel_h = 320
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2 - 20
        self.draw_panel(panel_x, panel_y, panel_w, panel_h, alpha=220)

        # ── Logo/título pequeño ──
        logo_font = assets.get_font(14, bold=True)
        logo = logo_font.render("ASCENSO CORPORATIVO", True, COLOR_GOLD)
        logo_rect = logo.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=panel_y + 20
        )
        self.screen.blit(logo, logo_rect)

        # Separador bajo el logo
        pygame.draw.line(self.screen, COLOR_GOLD,
                         (panel_x + 30, panel_y + 34),
                         (panel_x + panel_w - 30, panel_y + 34))

        # ── Texto con efecto typewriter ──
        font = assets.get_font(16)
        chars_shown = int(self._display_chars)
        total_shown = 0
        text_y = panel_y + 50

        for line in self._text_lines:
            if total_shown >= chars_shown:
                break

            remaining = chars_shown - total_shown
            visible = line[:remaining]
            total_shown += len(line)

            if visible:
                surf = font.render(visible, True, COLOR_LIGHT_GRAY)
                rect = surf.get_rect(
                    centerx=SCREEN_WIDTH // 2, centery=text_y
                )
                self.screen.blit(surf, rect)

            text_y += 28

        # ── Cursor parpadeante ──
        if not self._ready and math.sin(self._blink_timer * 4) > 0:
            cursor_font = assets.get_font(18, bold=True)
            cursor = cursor_font.render("|", True, COLOR_GOLD)
            self.screen.blit(cursor, (SCREEN_WIDTH // 2 + 10, text_y - 28))

        # ── Instrucción para continuar ──
        if self._ready:
            alpha = int(abs(math.sin(self._blink_timer * 2)) * 255)
            hint_font = assets.get_font(16, bold=True)
            hint = hint_font.render(
                "[ ENTER ]  Comenzar la aventura", True, COLOR_GOLD
            )
            hint.set_alpha(alpha)
            hint_rect = hint.get_rect(
                centerx=SCREEN_WIDTH // 2,
                centery=panel_y + panel_h + 30
            )
            self.screen.blit(hint, hint_rect)
        else:
            skip_font = assets.get_font(12)
            skip = skip_font.render(
                "[ ENTER ] Saltar  |  [ ESC ] Continuar", True, (80, 85, 110)
            )
            self.screen.blit(
                skip,
                skip.get_rect(
                    centerx=SCREEN_WIDTH // 2,
                    centery=panel_y + panel_h + 30
                )
            )

    def _draw_particles(self) -> None:
        """Dibuja partículas de papel flotante como elemento decorativo."""
        import random
        random.seed(42)  # Seed fija para reproducibilidad
        for i in range(12):
            px = random.randint(50, SCREEN_WIDTH - 50)
            py = (random.randint(0, SCREEN_HEIGHT) + int(self._time * 20 * (i % 3 + 0.5))) % SCREEN_HEIGHT
            size = random.randint(3, 8)
            alpha = random.randint(30, 80)
            surf = pygame.Surface((size * 2, size), pygame.SRCALPHA)
            surf.fill((200, 195, 170, alpha))
            self.screen.blit(surf, (px, py))
