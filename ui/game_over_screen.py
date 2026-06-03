"""
Módulo game_over_screen.py — Pantalla de derrota.

Se muestra cuando los guardias detectan al jugador demasiadas veces.
Opciones: Reintentar o Volver al Menú.
"""

import math
import pygame
from ui.base_screen import BaseScreen
from systems.constants import (
    STATE_PLAYING, STATE_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_RED, COLOR_WHITE, COLOR_GOLD, COLOR_LIGHT_GRAY,
)
from systems.asset_manager import assets


class GameOverScreen(BaseScreen):
    """
    Pantalla de Game Over.

    Muestra mensaje de derrota con animación de estática/glitch
    y opciones para reintentar o volver al menú.

    Attributes:
        _options (list): Opciones del menú de derrota.
        _selected (int): Opción actualmente seleccionada.
        _time (float): Temporizador para animaciones.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager)
        self._options: list = ["Reintentar", "Volver al Menú"]
        self._selected: int = 0
        self._time: float = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self._selected = (self._selected - 1) % len(self._options)
        elif event.key == pygame.K_DOWN:
            self._selected = (self._selected + 1) % len(self._options)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._select()
        elif event.key == pygame.K_ESCAPE:
            self.state_manager.change_state(STATE_TITLE)

    def _select(self) -> None:
        """Ejecuta la opción seleccionada."""
        if self._selected == 0:
            # Reintentar: reiniciar la partida desde el piso 1
            self.state_manager.game_data.reset()
            self.state_manager.change_state(STATE_PLAYING)
        else:
            self.state_manager.change_state(STATE_TITLE)

    def update(self, delta_time: float) -> None:
        self._time += delta_time

    def draw(self) -> None:
        """Dibuja la pantalla de game over con efecto de alerta."""
        # Fondo rojo oscuro con pulso
        pulse = abs(math.sin(self._time * 1.5)) * 0.3
        bg_color = (int(30 + pulse * 40), int(5 + pulse * 5), int(5 + pulse * 5))
        self.screen.fill(bg_color)

        # Efecto de estática/ruido
        self._draw_scanlines()

        self.draw_decorative_lines()

        # ── Título ──
        title_font = assets.get_font(54, bold=True)
        r = int(200 + math.sin(self._time * 3) * 55)
        title_color = (min(255, r), 30, 30)
        title_surf = title_font.render("HAS SIDO DESCUBIERTO", True, title_color)
        shadow_surf = title_font.render("HAS SIDO DESCUBIERTO", True, (0, 0, 0))
        title_rect = title_surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2 - 160
        )
        self.screen.blit(shadow_surf, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title_surf, title_rect)

        # ── Subtítulo ──
        sub_font = assets.get_font(20)
        sub_surf = sub_font.render(
            "Los guardias te han encontrado. Inténtalo de nuevo.",
            True, COLOR_LIGHT_GRAY
        )
        sub_rect = sub_surf.get_rect(
            centerx=SCREEN_WIDTH // 2,
            centery=SCREEN_HEIGHT // 2 - 100
        )
        self.screen.blit(sub_surf, sub_rect)

        # ── Icono de alerta ──
        alert_scale = 1.0 + math.sin(self._time * 4) * 0.1
        alert_font = assets.get_font(int(48 * alert_scale), bold=True)
        alert_surf = alert_font.render("⚠", True,
                                        (255, int(180 + math.sin(self._time * 3) * 75), 0))
        alert_rect = alert_surf.get_rect(
            centerx=SCREEN_WIDTH // 2,
            centery=SCREEN_HEIGHT // 2 - 30
        )
        self.screen.blit(alert_surf, alert_rect)

        # ── Panel del menú ──
        panel_w, panel_h = 320, 140
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = SCREEN_HEIGHT // 2 + 40
        self.draw_panel(panel_x, panel_y, panel_w, panel_h,
                        border_color=COLOR_RED, alpha=200)

        self.draw_menu(self._options, self._selected,
                       SCREEN_HEIGHT // 2 + 90, spacing=55)

        self.draw_back_hint("↑ ↓ + ENTER", "Seleccionar opción")

    def _draw_scanlines(self) -> None:
        """Dibuja líneas horizontales sutiles para efecto de monitor CRT."""
        scanline_surf = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(scanline_surf, (0, 0, 0, 30),
                             (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(scanline_surf, (0, 0))
