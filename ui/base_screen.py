"""
Módulo base_screen.py — Clase base para todas las pantallas de UI.

Provee funciones utilitarias de dibujado comunes:
- Fondos con gradiente.
- Títulos con sombra.
- Menús navegables con teclado.
- Paneles con borde dorado.
"""

import pygame
from abc import ABC, abstractmethod
from systems.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_NAVY, COLOR_NAVY_LIGHT, COLOR_GOLD, COLOR_GOLD_LIGHT,
    COLOR_WHITE, COLOR_GRAY, COLOR_LIGHT_GRAY, COLOR_BLACK,
    COLOR_DARK_GRAY,
)
from systems.asset_manager import assets


class BaseScreen(ABC):
    """
    Clase base abstracta para todas las pantallas del juego.

    Provee métodos de dibujado reutilizables para mantener
    consistencia visual entre todas las pantallas.

    Subclases deben implementar:
        handle_event(event): Manejar entrada del usuario.
        update(delta_time): Actualizar lógica de la pantalla.
        draw(): Dibujar la pantalla completa.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self._bg_scroll: float = 0.0  # Para fondo animado

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Procesa eventos de Pygame para esta pantalla."""
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Actualiza la lógica animada de la pantalla."""
        pass

    @abstractmethod
    def draw(self) -> None:
        """Dibuja la pantalla completa."""
        pass

    # ──────────────────────────────────────────────
    # UTILIDADES DE DIBUJADO
    # ──────────────────────────────────────────────

    def draw_gradient_background(self) -> None:
        """
        Dibuja un fondo con gradiente vertical de azul marino a oscuro.

        Simula el efecto de iluminación de un edificio corporativo nocturno.
        Usa pygame.draw.rect con franjas horizontales de color interpolado.
        """
        for y in range(SCREEN_HEIGHT):
            # Interpolación lineal entre los colores superior e inferior
            ratio = y / SCREEN_HEIGHT
            r = int(COLOR_NAVY[0] + (COLOR_DARK_GRAY[0] - COLOR_NAVY[0]) * ratio)
            g = int(COLOR_NAVY[1] + (COLOR_DARK_GRAY[1] - COLOR_NAVY[1]) * ratio)
            b = int(COLOR_NAVY[2] + (COLOR_DARK_GRAY[2] - COLOR_NAVY[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_animated_background(self, delta_time: float) -> None:
        """
        Fondo animado con líneas diagonales que se desplazan (efecto corporativo).

        Args:
            delta_time (float): Tiempo transcurrido para la animación.
        """
        self.draw_gradient_background()
        self._bg_scroll = (self._bg_scroll + delta_time * 20) % 80

        # Líneas diagonales sutiles como decoración
        line_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(-SCREEN_HEIGHT, SCREEN_WIDTH + SCREEN_HEIGHT, 80):
            offset_x = x + int(self._bg_scroll)
            pygame.draw.line(
                line_surf,
                (255, 255, 255, 8),
                (offset_x, 0),
                (offset_x + SCREEN_HEIGHT, SCREEN_HEIGHT),
                1
            )
        self.screen.blit(line_surf, (0, 0))

    def draw_title(self, text: str, y: int,
                   font_size: int = 52,
                   color: tuple = None) -> None:
        """
        Dibuja un título grande con efecto de sombra y brillo dorado.

        Args:
            text (str): Texto del título.
            y (int): Posición Y del centro del texto.
            font_size (int): Tamaño de la fuente.
            color (tuple): Color del texto (por defecto dorado).
        """
        color = color or COLOR_GOLD
        font = assets.get_font(font_size, bold=True)

        # Capa de sombra (desplazada 3px)
        shadow_surf = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=y + 3
        )
        self.screen.blit(shadow_surf, shadow_rect)

        # Texto principal
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=y
        )
        self.screen.blit(text_surf, text_rect)

    def draw_subtitle(self, text: str, y: int,
                      font_size: int = 18,
                      color: tuple = None) -> None:
        """
        Dibuja un subtítulo centrado.

        Args:
            text (str): Texto del subtítulo.
            y (int): Posición Y del centro.
            font_size (int): Tamaño de fuente.
            color (tuple): Color (por defecto blanco suave).
        """
        color = color or COLOR_LIGHT_GRAY
        font = assets.get_font(font_size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(centerx=SCREEN_WIDTH // 2, centery=y)
        self.screen.blit(surf, rect)

    def draw_panel(self, x: int, y: int, width: int, height: int,
                   border_color: tuple = None, alpha: int = 200) -> None:
        """
        Dibuja un panel semitransparente con borde.

        Args:
            x, y (int): Posición superior-izquierda.
            width, height (int): Dimensiones del panel.
            border_color (tuple): Color del borde (dorado por defecto).
            alpha (int): Opacidad del fondo (0-255).
        """
        border_color = border_color or COLOR_GOLD
        panel_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        panel_surf.fill((10, 15, 40, alpha))
        pygame.draw.rect(panel_surf, border_color,
                         panel_surf.get_rect(), 2)
        self.screen.blit(panel_surf, (x, y))

    def draw_menu(self, options: list, selected_idx: int,
                  y_start: int, spacing: int = 50) -> None:
        """
        Dibuja un menú navegable con el ítem seleccionado resaltado.

        Args:
            options (list): Lista de strings con las opciones.
            selected_idx (int): Índice de la opción actualmente seleccionada.
            y_start (int): Posición Y del primer ítem.
            spacing (int): Separación vertical entre ítems.
        """
        font_normal = assets.get_font(24)
        font_selected = assets.get_font(28, bold=True)

        for i, option in enumerate(options):
            is_selected = i == selected_idx
            y = y_start + i * spacing

            if is_selected:
                # Opción seleccionada: fondo y texto dorado
                text_surf = font_selected.render(option, True, COLOR_GOLD_LIGHT)
                text_rect = text_surf.get_rect(
                    centerx=SCREEN_WIDTH // 2, centery=y
                )
                # Fondo de selección
                bg_rect = text_rect.inflate(40, 12)
                bg_surf = pygame.Surface(
                    (bg_rect.width, bg_rect.height), pygame.SRCALPHA
                )
                bg_surf.fill((212, 175, 55, 40))
                pygame.draw.rect(bg_surf, COLOR_GOLD,
                                 bg_surf.get_rect(), 1)
                self.screen.blit(bg_surf, bg_rect.topleft)

                # Flechas indicadoras
                arrow_font = assets.get_font(24, bold=True)
                left_arrow = arrow_font.render("▶", True, COLOR_GOLD)
                right_arrow = arrow_font.render("◀", True, COLOR_GOLD)
                self.screen.blit(left_arrow,
                                 (text_rect.left - 30, text_rect.top))
                self.screen.blit(right_arrow,
                                 (text_rect.right + 10, text_rect.top))
            else:
                text_surf = font_normal.render(option, True, COLOR_LIGHT_GRAY)
                text_rect = text_surf.get_rect(
                    centerx=SCREEN_WIDTH // 2, centery=y
                )

            self.screen.blit(text_surf, text_rect)

    def draw_decorative_lines(self) -> None:
        """Dibuja líneas decorativas horizontales doradas como separadores."""
        line_y_top = 80
        line_y_bottom = SCREEN_HEIGHT - 80
        pygame.draw.line(self.screen, COLOR_GOLD,
                         (60, line_y_top), (SCREEN_WIDTH - 60, line_y_top), 1)
        pygame.draw.line(self.screen, COLOR_GOLD,
                         (60, line_y_bottom),
                         (SCREEN_WIDTH - 60, line_y_bottom), 1)

    def draw_back_hint(self, key: str = "ESC",
                       text: str = "Volver al menú") -> None:
        """
        Dibuja un indicador de tecla para volver en la esquina inferior.

        Args:
            key (str): Nombre de la tecla.
            text (str): Texto descriptivo.
        """
        font = assets.get_font(14)
        hint = f"[ {key} ] {text}"
        surf = font.render(hint, True, (120, 125, 145))
        rect = surf.get_rect(
            centerx=SCREEN_WIDTH // 2,
            bottom=SCREEN_HEIGHT - 20
        )
        self.screen.blit(surf, rect)
