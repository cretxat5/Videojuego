"""
Módulo level_manager.py — Gestor de niveles y transiciones entre pisos.

Actúa como intermediario entre el StateManager y los pisos individuales.
Carga el piso correcto, detecta cuando se completa y gestiona la transición.
"""

import pygame
from systems.constants import (
    STATE_PLAYING, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BLACK, COLOR_WHITE, COLOR_GOLD,
)
from systems.asset_manager import assets


class LevelManager:
    """
    Gestor de niveles del juego.

    Mantiene una referencia al nivel activo y gestiona:
    - Carga de pisos según el número de piso actual.
    - Detección de niveles completados.
    - Transiciones visuales entre pisos (fade).
    - Delegación de update/draw/handle_event al nivel activo.

    Attributes:
        screen (pygame.Surface): Superficie principal.
        state_manager: Gestor de estados global.
        _current_level: Instancia del nivel activo.
        _transition_alpha (int): Opacidad del efecto de transición.
        _transitioning (bool): Si hay una transición en curso.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self._current_level = None
        self._transition_alpha: int = 0
        self._transitioning: bool = False
        self._transition_timer: float = 0.0
        self._transition_duration: float = 0.8  # Segundos del fade

    def load_floor(self, floor_number: int) -> None:
        """
        Carga e instancia el piso indicado.

        Importaciones locales para evitar dependencias circulares.

        Args:
            floor_number (int): Número del piso a cargar (1-5).
        """
        from levels.floor1 import Floor1
        from levels.floor2 import Floor2
        from levels.floor3 import Floor3
        from levels.floor4 import Floor4
        from levels.floor5 import Floor5

        # Mapa de número de piso → clase del nivel
        floor_classes = {
            1: Floor1,
            2: Floor2,
            3: Floor3,
            4: Floor4,
            5: Floor5,
        }

        floor_class = floor_classes.get(floor_number)
        if floor_class:
            self._current_level = floor_class(self.screen, self.state_manager)
            self._start_transition()  # Efecto de entrada al nuevo piso
        else:
            # Si se pide un piso inválido, no hacer nada
            pass

    def _start_transition(self) -> None:
        """Inicia el efecto de transición de entrada (fade-in)."""
        self._transitioning = True
        self._transition_timer = self._transition_duration
        self._transition_alpha = 255  # Comienza completamente negro

    # ──────────────────────────────────────────────
    # DELEGACIÓN AL NIVEL ACTIVO
    # ──────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        """Delega el evento al nivel activo."""
        if self._current_level:
            self._current_level.handle_event(event)

    def update(self, delta_time: float) -> None:
        """
        Actualiza el nivel activo y gestiona transiciones y cambios de piso.

        Args:
            delta_time (float): Tiempo transcurrido desde el último frame.
        """
        if not self._current_level:
            return

        self._current_level.update(delta_time)

        # Actualizar transición
        if self._transitioning:
            self._transition_timer -= delta_time
            progress = self._transition_timer / self._transition_duration
            self._transition_alpha = max(0, int(255 * progress))
            if self._transition_timer <= 0:
                self._transitioning = False
                self._transition_alpha = 0

        # Verificar si el nivel fue completado → cargar siguiente piso
        if self._current_level.completed:
            gd = self.state_manager.game_data
            next_floor = gd.current_floor
            self.load_floor(next_floor)

    def draw(self) -> None:
        """Dibuja el nivel activo y el overlay de transición."""
        if self._current_level:
            self._current_level.draw()

        # Overlay de transición (fade negro encima)
        if self._transition_alpha > 0:
            fade_surf = pygame.Surface(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
            )
            fade_surf.fill((0, 0, 0, self._transition_alpha))
            self.screen.blit(fade_surf, (0, 0))

            # Texto del piso durante la transición
            if self._transition_alpha > 100:
                gd = self.state_manager.game_data
                font = assets.get_font(32, bold=True)
                floor_text = f"PISO {gd.current_floor}"
                text_surf = font.render(floor_text, True, COLOR_GOLD)
                text_rect = text_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                )
                text_surf.set_alpha(self._transition_alpha)
                self.screen.blit(text_surf, text_rect)

                # Subtítulo del piso
                subtitles = {
                    1: "Recepción",
                    2: "Administración",
                    3: "Recursos Humanos",
                    4: "Oficinas Ejecutivas",
                    5: "Dirección General",
                }
                sub = subtitles.get(gd.current_floor, "")
                sub_font = assets.get_font(20)
                sub_surf = sub_font.render(sub, True, COLOR_WHITE)
                sub_rect = sub_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
                )
                sub_surf.set_alpha(self._transition_alpha)
                self.screen.blit(sub_surf, sub_rect)
