"""
Módulo pause_menu.py — Menú de pausa del juego.

Se activa con ESC durante el juego. Permite:
    - Continuar la partida.
    - Volver al menú principal.
    - Salir del programa.
"""

import pygame
from ui.base_screen import BaseScreen
from systems.constants import (
    STATE_PLAYING, STATE_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_GOLD, COLOR_WHITE, COLOR_LIGHT_GRAY,
)
from systems.asset_manager import assets


class PauseMenu(BaseScreen):
    """
    Menú de pausa superpuesto sobre el juego.

    Dibuja un overlay semitransparente encima del estado
    de juego anterior para dar sensación de pausa real.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager)
        self._options: list = ["Continuar", "Menú Principal", "Salir"]
        self._selected: int = 0
        # Superficie de oscurecimiento del fondo
        self._overlay: pygame.Surface = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self._overlay.fill((0, 0, 0, 160))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.state_manager.change_state(STATE_PLAYING)
        elif event.key == pygame.K_UP:
            self._selected = (self._selected - 1) % len(self._options)
        elif event.key == pygame.K_DOWN:
            self._selected = (self._selected + 1) % len(self._options)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._select()

    def _select(self) -> None:
        """Ejecuta la opción seleccionada."""
        if self._selected == 0:
            self.state_manager.change_state(STATE_PLAYING)
        elif self._selected == 1:
            self.state_manager.change_state(STATE_TITLE)
        elif self._selected == 2:
            self.state_manager.quit_game()

    def update(self, delta_time: float) -> None:
        pass

    def draw(self) -> None:
        """Dibuja el overlay y el panel de pausa."""
        # Oscurecer la pantalla actual
        self.screen.blit(self._overlay, (0, 0))

        # Panel de pausa
        panel_w, panel_h = 340, 260
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        self.draw_panel(panel_x, panel_y, panel_w, panel_h, alpha=240)

        # Título
        self.draw_title("PAUSA", SCREEN_HEIGHT // 2 - 95, font_size=36)

        # Línea separadora
        pygame.draw.line(self.screen, COLOR_GOLD,
                         (panel_x + 20, panel_y + 75),
                         (panel_x + panel_w - 20, panel_y + 75))

        # Menú
        self.draw_menu(self._options, self._selected,
                       SCREEN_HEIGHT // 2 - 20, spacing=55)

        # Hint
        self.draw_back_hint("ESC", "Continuar jugando")
