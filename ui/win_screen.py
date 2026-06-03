"""
Módulo win_screen.py — Pantalla de victoria del juego.

Muestra: felicitaciones, tiempo de juego, objetos recolectados
y pisos completados. Permite volver al menú principal.
"""

import math
import time
import pygame
from ui.base_screen import BaseScreen
from systems.constants import (
    STATE_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_GOLD, COLOR_GOLD_LIGHT, COLOR_WHITE,
    COLOR_GREEN, COLOR_LIGHT_GRAY,
)
from systems.asset_manager import assets


class WinScreen(BaseScreen):
    """
    Pantalla de victoria final.

    Muestra las estadísticas de la partida ganada:
    tiempo total, objetos recolectados y pisos completados.
    Incluye animación de confeti dorado.

    Attributes:
        _time (float): Temporizador de la animación.
        _particles (list): Partículas de confeti.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager)
        self._time: float = 0.0
        self._particles: list = self._create_particles()

    def _create_particles(self) -> list:
        """Crea las partículas de confeti para la animación de victoria."""
        import random
        particles = []
        for _ in range(60):
            particles.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(-SCREEN_HEIGHT, 0),
                "vx": random.uniform(-30, 30),
                "vy": random.uniform(60, 150),
                "color": random.choice([
                    COLOR_GOLD, (255, 215, 80), COLOR_GREEN,
                    (100, 200, 255), (255, 100, 100)
                ]),
                "size": random.randint(4, 10),
                "angle": random.uniform(0, 360),
                "spin": random.uniform(-120, 120),
            })
        return particles

    def handle_event(self, event: pygame.event.Event) -> None:
        """ENTER o ESC vuelve al menú principal."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                self.state_manager.change_state(STATE_TITLE)

    def update(self, delta_time: float) -> None:
        """Actualiza partículas de confeti."""
        self._time += delta_time
        for p in self._particles:
            p["x"] += p["vx"] * delta_time
            p["y"] += p["vy"] * delta_time
            p["angle"] += p["spin"] * delta_time
            # Reiniciar partículas que salen por abajo
            if p["y"] > SCREEN_HEIGHT + 20:
                import random
                p["y"] = random.randint(-50, -10)
                p["x"] = random.randint(0, SCREEN_WIDTH)

    def draw(self) -> None:
        """Dibuja la pantalla de victoria completa."""
        self.draw_gradient_background()
        self._draw_particles()

        self.draw_decorative_lines()

        # ── Título de victoria ──
        pulse = 1 + math.sin(self._time * 2) * 0.03
        title_font = assets.get_font(int(52 * pulse), bold=True)
        self._draw_glow_text("¡FELICIDADES!", SCREEN_HEIGHT // 2 - 170,
                              title_font, COLOR_GOLD_LIGHT)

        subtitle_font = assets.get_font(22)
        self._draw_glow_text("¡Has conseguido el empleo!",
                              SCREEN_HEIGHT // 2 - 120, subtitle_font, COLOR_WHITE)

        # ── Estadísticas ──
        gd = self.state_manager.game_data
        elapsed = gd.elapsed_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)

        stats_data = [
            ("⏱  Tiempo de juego", f"{mins:02d}:{secs:02d}"),
            ("📦  Objetos recolectados", str(gd.inventory.total_collected)),
            ("🏢  Pisos completados", f"{gd.floors_completed + 1} / 5"),
            ("⚠   Detecciones", str(gd.detection_count)),
        ]

        panel_w, panel_h = 420, 220
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = SCREEN_HEIGHT // 2 - 90
        self.draw_panel(panel_x, panel_y, panel_w, panel_h, alpha=220)

        font_label = assets.get_font(16)
        font_value = assets.get_font(18, bold=True)

        for i, (label, value) in enumerate(stats_data):
            row_y = panel_y + 25 + i * 48
            # Label
            label_surf = font_label.render(label, True, COLOR_LIGHT_GRAY)
            self.screen.blit(label_surf, (panel_x + 25, row_y))
            # Valor (alineado a la derecha)
            value_surf = font_value.render(value, True, COLOR_GOLD)
            value_rect = value_surf.get_rect(
                right=panel_x + panel_w - 25,
                centery=row_y + 10
            )
            self.screen.blit(value_surf, value_rect)
            # Línea separadora sutil
            if i < len(stats_data) - 1:
                pygame.draw.line(self.screen, (40, 50, 90),
                                 (panel_x + 15, row_y + 32),
                                 (panel_x + panel_w - 15, row_y + 32))

        # ── Botón de regreso ──
        btn_alpha = int(abs(math.sin(self._time * 2)) * 200 + 55)
        btn_font = assets.get_font(20, bold=True)
        btn_surf = btn_font.render(
            "[ ENTER / ESC ]  Volver al Menú Principal", True, COLOR_GOLD
        )
        btn_surf.set_alpha(btn_alpha)
        btn_rect = btn_surf.get_rect(
            centerx=SCREEN_WIDTH // 2,
            centery=SCREEN_HEIGHT // 2 + 165
        )
        self.screen.blit(btn_surf, btn_rect)

    def _draw_glow_text(self, text: str, y: int,
                         font: pygame.font.Font, color: tuple) -> None:
        """Dibuja texto con sombra y aura de brillo."""
        shadow = font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, shadow.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=y + 3
        ))
        surf = font.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=y
        ))

    def _draw_particles(self) -> None:
        """Dibuja las partículas de confeti animadas."""
        for p in self._particles:
            surf = pygame.Surface((p["size"], p["size"]), pygame.SRCALPHA)
            surf.fill((*p["color"][:3], 200))
            rotated = pygame.transform.rotate(surf, p["angle"])
            self.screen.blit(rotated, (int(p["x"]), int(p["y"])))
