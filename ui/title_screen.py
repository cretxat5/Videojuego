"""
Módulo title_screen.py — Pantalla de título principal.

Muestra el título del juego, fotografías de los estudiantes,
y el menú principal navegable con teclado (↑ ↓ ENTER).

Opciones del menú:
    1. Iniciar Partida → STATE_INTRO
    2. Instrucciones  → STATE_INSTRUCTIONS
    3. Créditos       → STATE_CREDITS
    4. Salir          → Cierra el programa
"""

import math
import pygame
from ui.base_screen import BaseScreen
from systems.constants import (
    STATE_INTRO, STATE_INSTRUCTIONS, STATE_CREDITS,
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GOLD, COLOR_WHITE,
    COLOR_LIGHT_GRAY, COLOR_NAVY, PLAYERS_DIR,
)
from systems.asset_manager import assets
import os


class TitleScreen(BaseScreen):
    """
    Pantalla de título del juego Ascenso Corporativo.

    Características:
    - Fondo animado con efecto de edificio corporativo.
    - Título del juego con animación de pulso.
    - Espacio para fotos de los dos estudiantes.
    - Menú navegable con teclado.
    - Música de fondo.

    Attributes:
        _menu_options (list): Opciones del menú principal.
        _selected_idx (int): Índice de la opción actualmente seleccionada.
        _title_pulse (float): Temporizador para animación del título.
        _player_photos (list): Superficies de las fotos de estudiantes.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager)

        # Opciones del menú y su estado de navegación
        self._menu_options: list = [
            "▶  Iniciar Partida",
            "   Instrucciones",
            "   Créditos",
            "   Salir",
        ]
        self._selected_idx: int = 0
        self._title_pulse: float = 0.0
        self._logo_angle: float = 0.0  # Para icono rotante decorativo

        # Cargar fotos de los estudiantes (con respaldo)
        self._player_photos: list = [
            assets.get_player_image(1, "down", (90, 90)),
            assets.get_player_image(2, "down", (90, 90)),
        ]

        # Iniciar música de título
        assets.play_music("menu_music.ogg")

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Maneja los eventos del teclado en el menú de título.

        Controles:
            ↑ / ↓    : Navegar opciones.
            ENTER     : Seleccionar opción activa.
        """
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self._selected_idx = (self._selected_idx - 1) % len(self._menu_options)
            assets.play_sound("menu_nav", "menu_nav.wav", 0.5)

        elif event.key == pygame.K_DOWN:
            self._selected_idx = (self._selected_idx + 1) % len(self._menu_options)
            assets.play_sound("menu_nav", "menu_nav.wav", 0.5)

        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._select_option()

    def _select_option(self) -> None:
        """
        Ejecuta la acción de la opción seleccionada.

        Opciones:
            0: Ir a la introducción narrativa.
            1: Ir a instrucciones.
            2: Ir a créditos.
            3: Salir del programa.
        """
        assets.play_sound("menu_select", "menu_select.wav", 0.7)

        actions = {
            0: lambda: self.state_manager.change_state(STATE_INTRO),
            1: lambda: self.state_manager.change_state(STATE_INSTRUCTIONS),
            2: lambda: self.state_manager.change_state(STATE_CREDITS),
            3: lambda: self.state_manager.quit_game(),
        }
        action = actions.get(self._selected_idx)
        if action:
            action()

    def update(self, delta_time: float) -> None:
        """Actualiza las animaciones del título."""
        self._title_pulse += delta_time * 2.0
        self._logo_angle += delta_time * 30.0
        self.draw_animated_background(delta_time)

    def draw(self) -> None:
        """Dibuja la pantalla de título completa."""
        # ── Fondo animado ──
        self.draw_animated_background(0)

        # ── Icono decorativo del edificio ──
        self._draw_building_decoration()

        # ── Líneas decorativas ──
        self.draw_decorative_lines()

        # ── Título principal con pulso ──
        pulse = 1.0 + math.sin(self._title_pulse) * 0.02
        title_font = assets.get_font(int(56 * pulse), bold=True)
        self._draw_pulsing_title("ASCENSO CORPORATIVO", 110, title_font)

        # ── Subtítulo ──
        self.draw_subtitle("Un juego de ingenio y sigilo", 155, font_size=16)

        # ── Fotos de los estudiantes ──
        self._draw_student_photos()

        # ── Menú principal ──
        menu_y = 330
        self.draw_panel(
            SCREEN_WIDTH // 2 - 220, menu_y - 30,
            440, len(self._menu_options) * 50 + 40,
            alpha=180
        )
        self.draw_menu(self._menu_options, self._selected_idx,
                       menu_y + 10, spacing=50)

        # ── Controles del menú ──
        font_hint = assets.get_font(13)
        hints = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 55,
             "↑ ↓  Navegar   |   ENTER  Seleccionar"),
        ]
        for hx, hy, htxt in hints:
            surf = font_hint.render(htxt, True, (100, 105, 130))
            self.screen.blit(surf, surf.get_rect(centerx=hx, centery=hy))

    def _draw_pulsing_title(self, text: str, y: int,
                             font: pygame.font.Font) -> None:
        """
        Dibuja el título con efecto de brillo pulsante dorado.

        Args:
            text (str): Texto del título.
            y (int): Posición Y.
            font (pygame.font.Font): Fuente a usar.
        """
        # Sombra
        shadow = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(centerx=SCREEN_WIDTH // 2, centery=y + 4)
        self.screen.blit(shadow, shadow_rect)

        # Glow dorado (ligeramente más grande y desenfocado)
        glow_color = (
            min(255, int(212 + math.sin(self._title_pulse) * 43)),
            min(255, int(175 + math.sin(self._title_pulse) * 40)),
            int(55 + abs(math.sin(self._title_pulse)) * 100),
        )
        text_surf = font.render(text, True, glow_color)
        text_rect = text_surf.get_rect(centerx=SCREEN_WIDTH // 2, centery=y)
        self.screen.blit(text_surf, text_rect)

    def _draw_student_photos(self) -> None:
        """
        Dibuja las fotos de los dos estudiantes con marco dorado.

        Las fotos se ubican simétricamente debajo del título.
        Si no existen las imágenes reales, se muestra un respaldo.
        """
        from systems.constants import CREDITS_INFO
        photo_size = 90
        spacing = 200
        base_x = SCREEN_WIDTH // 2
        base_y = 235

        for i, photo in enumerate(self._player_photos):
            offset_x = -spacing // 2 if i == 0 else spacing // 2
            px = base_x + offset_x - photo_size // 2
            py = base_y - photo_size // 2

            # Marco dorado
            frame_rect = pygame.Rect(px - 4, py - 4,
                                     photo_size + 8, photo_size + 8)
            pygame.draw.rect(self.screen, COLOR_GOLD, frame_rect, 2)
            # Fondo del marco
            inner_surf = pygame.Surface((photo_size, photo_size), pygame.SRCALPHA)
            inner_surf.fill((20, 30, 60, 200))
            self.screen.blit(inner_surf, (px, py))

            # Foto del estudiante
            self.screen.blit(photo, (px, py))

            # Nombre del estudiante
            name = CREDITS_INFO["integrantes"][i] if i < len(
                CREDITS_INFO["integrantes"]) else f"Estudiante {i+1}"
            name_short = name.split(" - ")[-1][:16]  # Solo el nombre real
            font = assets.get_font(11)
            name_surf = font.render(name_short, True, COLOR_LIGHT_GRAY)
            name_rect = name_surf.get_rect(
                centerx=px + photo_size // 2,
                top=py + photo_size + 5
            )
            self.screen.blit(name_surf, name_rect)

    def _draw_building_decoration(self) -> None:
        """Dibuja una silueta de edificio decorativa en el fondo."""
        building_color = (20, 30, 65)
        # Silueta de edificio estilizada (rectángulos)
        buildings = [
            (50, 200, 80, 440),
            (150, 250, 60, 390),
            (840, 220, 70, 420),
            (760, 260, 50, 380),
            (380, 280, 40, 360),
            (540, 240, 50, 400),
            (680, 270, 45, 370),
        ]
        for bx, by, bw, bh in buildings:
            pygame.draw.rect(self.screen, building_color,
                             (bx, by, bw, SCREEN_HEIGHT - by))
            # Ventanas del edificio
            for wy in range(by + 20, SCREEN_HEIGHT - 20, 25):
                for wx in range(bx + 10, bx + bw - 10, 18):
                    win_color = (
                        (60, 80, 120) if (wx + wy) % 3 != 0
                        else (200, 180, 80)
                    )
                    pygame.draw.rect(self.screen, win_color,
                                     (wx, wy, 8, 12))
