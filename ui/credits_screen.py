"""
Módulo credits_screen.py — Pantalla de créditos del juego.

Muestra: nombre del juego, integrantes, materia, profesor y año.
Permite regresar al menú principal con ESC.
"""

import math
import pygame
from ui.base_screen import BaseScreen
from systems.constants import (
    STATE_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_GOLD, COLOR_WHITE, COLOR_LIGHT_GRAY, COLOR_GRAY,
    CREDITS_INFO,
)
from systems.asset_manager import assets


class CreditsScreen(BaseScreen):
    """
    Pantalla de créditos del proyecto.

    Muestra información académica del proyecto con animación
    de aparición gradual (fade-in por línea).
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager)
        self._time: float = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        """Vuelve al menú con cualquier tecla."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_BACKSPACE):
                self.state_manager.change_state(STATE_TITLE)

    def update(self, delta_time: float) -> None:
        self._time += delta_time

    def draw(self) -> None:
        """Dibuja la pantalla de créditos."""
        self.draw_gradient_background()
        self.draw_decorative_lines()
        self.draw_title("CRÉDITOS", 55, font_size=42)

        # Panel central
        panel_x = SCREEN_WIDTH // 2 - 280
        panel_y = 100
        panel_w = 560
        panel_h = 400
        self.draw_panel(panel_x, panel_y, panel_w, panel_h, alpha=210)

        font_section = assets.get_font(16, bold=True)
        font_value = assets.get_font(22, bold=True)
        font_sub = assets.get_font(15)

        # Icono decorativo animado
        angle = self._time * 40
        icon_surf = assets.get_font(30, bold=True).render("🏢", True, COLOR_GOLD)
        icon_rect = icon_surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=panel_y + 35
        )
        self.screen.blit(icon_surf, icon_rect)

        # ── Nombre del juego ──
        y = panel_y + 75
        self._draw_credit_row("JUEGO", CREDITS_INFO["juego"],
                               font_section, font_value, y, COLOR_GOLD)

        # Separador
        y += 55
        pygame.draw.line(self.screen, (50, 60, 100),
                         (panel_x + 30, y), (panel_x + panel_w - 30, y))

        # ── Integrantes ──
        y += 15
        label_surf = font_section.render("INTEGRANTES", True, COLOR_GOLD)
        label_rect = label_surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=y
        )
        self.screen.blit(label_surf, label_rect)

        for integrante in CREDITS_INFO["integrantes"]:
            y += 32
            val_surf = font_value.render(integrante, True, COLOR_WHITE)
            val_rect = val_surf.get_rect(centerx=SCREEN_WIDTH // 2, centery=y)
            self.screen.blit(val_surf, val_rect)

        # ── Materia ──
        y += 50
        pygame.draw.line(self.screen, (50, 60, 100),
                         (panel_x + 30, y), (panel_x + panel_w - 30, y))
        y += 15
        self._draw_credit_row("MATERIA", CREDITS_INFO["materia"],
                               font_section, font_sub, y, COLOR_LIGHT_GRAY)

        # ── Profesor ──
        y += 55
        self._draw_credit_row("PROFESOR", CREDITS_INFO["profesor"],
                               font_section, font_sub, y, COLOR_LIGHT_GRAY)

        # ── Año ──
        y += 55
        self._draw_credit_row("AÑO", CREDITS_INFO["anio"],
                               font_section, font_sub, y, COLOR_GRAY)

        self.draw_back_hint("ESC / ENTER", "Volver al menú principal")

    def _draw_credit_row(self, label: str, value: str,
                          label_font, value_font,
                          y: int, value_color: tuple) -> None:
        """
        Dibuja una fila de crédito: etiqueta arriba, valor abajo (centrado).

        Args:
            label (str): Etiqueta de la categoría.
            value (str): Valor a mostrar.
            label_font: Fuente para la etiqueta.
            value_font: Fuente para el valor.
            y (int): Posición Y base.
            value_color (tuple): Color del valor.
        """
        label_surf = label_font.render(label, True, COLOR_GOLD)
        label_rect = label_surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=y
        )
        self.screen.blit(label_surf, label_rect)

        val_surf = value_font.render(value, True, value_color)
        val_rect = val_surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=y + 28
        )
        self.screen.blit(val_surf, val_rect)
