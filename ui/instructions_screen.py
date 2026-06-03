"""
Módulo instructions_screen.py — Pantalla de instrucciones del juego.

Muestra controles, objetivo y mecánicas principales.
Permite volver al menú con ESC.
"""

import pygame
from ui.base_screen import BaseScreen
from systems.constants import (
    STATE_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_GOLD, COLOR_WHITE, COLOR_LIGHT_GRAY, COLOR_GREEN,
)
from systems.asset_manager import assets


class InstructionsScreen(BaseScreen):
    """
    Pantalla de instrucciones del juego.

    Muestra los controles del teclado y el objetivo del juego
    organizados en dos columnas para mejor legibilidad.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Vuelve al menú con ESC o ENTER/BACKSPACE."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_BACKSPACE):
                self.state_manager.change_state(STATE_TITLE)

    def update(self, delta_time: float) -> None:
        pass

    def draw(self) -> None:
        """Dibuja la pantalla de instrucciones con dos columnas."""
        self.draw_gradient_background()
        self.draw_decorative_lines()
        self.draw_title("INSTRUCCIONES", 50, font_size=40)

        # ── Panel izquierdo: Controles ──
        panel_x = 80
        panel_w = 360
        panel_h = 340
        panel_y = 100
        self.draw_panel(panel_x, panel_y, panel_w, panel_h)

        font_head = assets.get_font(18, bold=True)
        font_key = assets.get_font(15, bold=True)
        font_desc = assets.get_font(14)

        # Título de la columna
        head_surf = font_head.render("CONTROLES", True, COLOR_GOLD)
        self.screen.blit(head_surf, (panel_x + 20, panel_y + 15))

        controls = [
            ("W A S D", "Mover personaje"),
            ("TAB", "Cambiar entre personajes"),
            ("E", "Interactuar con objetos"),
            ("Q", "Lanzar distracción a guardias"),
            ("ESC", "Pausar el juego"),
            ("↑ ↓ + ENTER", "Navegar menús"),
        ]

        for i, (key, desc) in enumerate(controls):
            y = panel_y + 55 + i * 46
            # Caja de la tecla
            key_surf = font_key.render(key, True, COLOR_GOLD)
            key_bg = key_surf.get_rect(
                left=panel_x + 20, centery=y + 10
            ).inflate(10, 6)
            pygame.draw.rect(self.screen, (20, 30, 70), key_bg)
            pygame.draw.rect(self.screen, COLOR_GOLD, key_bg, 1)
            self.screen.blit(key_surf, (panel_x + 25, y + 2))

            # Descripción
            desc_surf = font_desc.render(desc, True, COLOR_LIGHT_GRAY)
            self.screen.blit(desc_surf, (panel_x + 25, y + 24))

        # ── Panel derecho: Objetivo y Mecánicas ──
        panel2_x = SCREEN_WIDTH - 80 - 380
        self.draw_panel(panel2_x, panel_y, 380, panel_h)

        head2 = font_head.render("OBJETIVO", True, COLOR_GOLD)
        self.screen.blit(head2, (panel2_x + 20, panel_y + 15))

        objective_lines = [
            "Explorar el edificio corporativo,",
            "reunir 4 documentos clave y",
            "llegar al último piso para la",
            "entrevista laboral.",
        ]
        for i, line in enumerate(objective_lines):
            surf = font_desc.render(line, True, COLOR_LIGHT_GRAY)
            self.screen.blit(surf, (panel2_x + 20, panel_y + 50 + i * 22))

        # Separador
        pygame.draw.line(self.screen, COLOR_GOLD,
                         (panel2_x + 20, panel_y + 145),
                         (panel2_x + 360, panel_y + 145))

        head3 = font_head.render("DOCUMENTOS REQUERIDOS", True, COLOR_GOLD)
        self.screen.blit(head3, (panel2_x + 20, panel_y + 160))

        docs = [
            "✓  Identificación Temporal  (Piso 1)",
            "✓  Carpeta de Documentos   (Piso 2)",
            "✓  Tarjeta de Acceso       (Piso 3)",
            "✓  Hoja de Vida Oficial    (Piso 4)",
        ]
        for i, doc in enumerate(docs):
            surf = font_desc.render(doc, True, COLOR_GREEN)
            self.screen.blit(surf, (panel2_x + 20, panel_y + 190 + i * 30))

        # ── Panel inferior: Mecánicas ──
        mec_y = panel_y + panel_h + 20
        self.draw_panel(80, mec_y, SCREEN_WIDTH - 160, 90)
        head4 = font_head.render("MECÁNICA DE DISTRACCIÓN", True, COLOR_GOLD)
        self.screen.blit(head4, (100, mec_y + 12))
        mec_lines = [
            "Presiona Q para lanzar un objeto → el guardia más cercano irá a investigar el sonido.",
            "Aprovecha ese momento para cruzar zonas vigiladas.",
        ]
        for i, line in enumerate(mec_lines):
            surf = font_desc.render(line, True, COLOR_LIGHT_GRAY)
            self.screen.blit(surf, (100, mec_y + 38 + i * 22))

        self.draw_back_hint("ESC / ENTER", "Volver al menú principal")
