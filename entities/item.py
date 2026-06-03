"""
Módulo item.py — Clase Item: objetos recolectables del juego.

Los objetos pueden ser principales (requeridos para ganar)
o secundarios (usados como distracciones para guardias).
"""

import math
import pygame
from systems.constants import (
    ITEM_ID, COLOR_GOLD, COLOR_GREEN, COLOR_WHITE,
    COLOR_GRAY, TILE_SIZE,
)
from systems.asset_manager import assets


class Item(pygame.sprite.Sprite):
    """
    Objeto recolectable del mundo del juego.

    Hereda de pygame.sprite.Sprite para integrarse con los
    grupos de sprites de Pygame.

    Attributes:
        item_id (str): Identificador único del tipo de objeto.
        name (str): Nombre legible del objeto.
        rect (pygame.Rect): Rectángulo de posición y colisión.
        collected (bool): Si ya fue recolectado.
        _bob_timer (float): Temporizador para animación de flotación.
    """

    def __init__(self, x: int, y: int, item_id: str) -> None:
        """
        Inicializa el objeto en la posición indicada.

        Args:
            x (int): Posición X del centro del objeto.
            y (int): Posición Y del centro del objeto.
            item_id (str): Identificador del tipo de objeto.
        """
        super().__init__()

        self.item_id: str = item_id
        self.name: str = ITEM_ID.get(item_id, item_id)
        self.collected: bool = False

        # Temporizador para efecto de flotación (bobbing)
        self._bob_timer: float = 0.0
        self._bob_amplitude: float = 3.0  # Píxeles de desplazamiento
        self._bob_speed: float = 2.5      # Ciclos por segundo
        self._base_y: int = y             # Posición Y original

        # Determinar tamaño según tipo de objeto
        size = (22, 22) if item_id in ("moneda", "lata", "papel") else (26, 26)

        # Cargar imagen del objeto
        self.image: pygame.Surface = assets.get_item_image(item_id, size)

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    # ──────────────────────────────────────────────
    # ACTUALIZACIÓN
    # ──────────────────────────────────────────────

    def update(self, delta_time: float) -> None:
        """
        Actualiza la animación del objeto (efecto de flotación).

        Args:
            delta_time (float): Tiempo transcurrido (segundos).
        """
        if self.collected:
            return

        self._bob_timer += delta_time
        # Calcular offset de flotación usando función seno
        offset = math.sin(self._bob_timer * self._bob_speed * math.pi) * self._bob_amplitude
        self.rect.centery = int(self._base_y + offset)

    # ──────────────────────────────────────────────
    # RENDERIZADO
    # ──────────────────────────────────────────────

    def draw(self, screen: pygame.Surface,
             camera_offset: tuple = (0, 0)) -> None:
        """
        Dibuja el objeto con efectos visuales de brillos y etiqueta.

        Args:
            screen (pygame.Surface): Superficie de renderizado.
            camera_offset (tuple): Desplazamiento de cámara (cx, cy).
        """
        if self.collected:
            return

        cx, cy = camera_offset
        draw_rect = self.rect.move(-cx, -cy)

        # ── Halo de brillo bajo el objeto ──
        glow_radius = self.rect.width // 2 + 5
        glow_surf = pygame.Surface(
            (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
        )
        # Color del brillo según tipo de objeto
        glow_color = COLOR_GOLD[:3] + (60,) if self.item_id not in (
            "moneda", "lata", "papel") else COLOR_GREEN[:3] + (50,)
        pygame.draw.circle(glow_surf, glow_color,
                           (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surf,
                    (draw_rect.centerx - glow_radius,
                     draw_rect.centery - glow_radius))

        # ── Imagen del objeto ──
        screen.blit(self.image, draw_rect.topleft)

        # ── Etiqueta con el nombre ──
        font = assets.get_font(9)
        label = font.render(self.name[:12], True, COLOR_WHITE)
        label_rect = label.get_rect(
            centerx=draw_rect.centerx,
            top=draw_rect.bottom + 2
        )
        # Sombra del texto
        shadow = font.render(self.name[:12], True, (0, 0, 0))
        screen.blit(shadow, (label_rect.x + 1, label_rect.y + 1))
        screen.blit(label, label_rect)


class DistractionProjectile:
    """
    Proyectil visual que aparece al lanzar un objeto de distracción.

    Representa el objeto en vuelo desde el jugador hasta el destino.

    Attributes:
        start_pos (tuple): Posición de origen.
        end_pos (tuple): Posición de destino.
        pos (list): Posición actual del proyectil.
        speed (float): Velocidad de movimiento del proyectil.
        active (bool): Si el proyectil está en movimiento.
        landed (bool): Si ya llegó al destino.
    """

    def __init__(self, start_pos: tuple, end_pos: tuple,
                 item_id: str = "moneda") -> None:
        """
        Inicializa el proyectil.

        Args:
            start_pos (tuple): Posición inicial (x, y).
            end_pos (tuple): Posición destino (x, y).
            item_id (str): Tipo de objeto lanzado (afecta color).
        """
        self.start_pos: tuple = start_pos
        self.end_pos: tuple = end_pos
        self.pos: list = list(start_pos)
        self.speed: float = 350.0
        self.active: bool = True
        self.landed: bool = False
        self.item_id: str = item_id

        # Calcular dirección normalizada
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            self._dir_x = dx / dist
            self._dir_y = dy / dist
        else:
            self._dir_x = 0
            self._dir_y = 0

        # Color según objeto lanzado
        self._color = {
            "moneda": COLOR_GOLD,
            "lata": (150, 150, 160),
            "papel": (230, 230, 210),
        }.get(item_id, COLOR_WHITE)

        self._trail: list = []  # Rastro visual del proyectil

    def update(self, delta_time: float) -> None:
        """
        Actualiza la posición del proyectil.

        Args:
            delta_time (float): Tiempo transcurrido.
        """
        if not self.active:
            return

        # Guardar posición para el rastro
        self._trail.append(tuple(self.pos))
        if len(self._trail) > 6:
            self._trail.pop(0)

        # Mover hacia el destino
        self.pos[0] += self._dir_x * self.speed * delta_time
        self.pos[1] += self._dir_y * self.speed * delta_time

        # Verificar si llegó al destino
        dx = self.end_pos[0] - self.pos[0]
        dy = self.end_pos[1] - self.pos[1]
        if math.sqrt(dx ** 2 + dy ** 2) < 8:
            self.pos = list(self.end_pos)
            self.active = False
            self.landed = True

    def draw(self, screen: pygame.Surface,
             camera_offset: tuple = (0, 0)) -> None:
        """
        Dibuja el proyectil y su rastro visual.

        Args:
            screen (pygame.Surface): Superficie de renderizado.
            camera_offset (tuple): Desplazamiento de cámara.
        """
        if not self.active and not self.landed:
            return

        cx, cy = camera_offset

        # Rastro del proyectil
        for i, trail_pos in enumerate(self._trail):
            alpha = int(180 * (i / max(1, len(self._trail))))
            radius = max(2, 5 - (len(self._trail) - i))
            trail_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                trail_surf, (*self._color, alpha),
                (radius, radius), radius
            )
            screen.blit(trail_surf,
                        (int(trail_pos[0]) - radius - cx,
                         int(trail_pos[1]) - radius - cy))

        # Proyectil principal
        draw_x = int(self.pos[0]) - cx
        draw_y = int(self.pos[1]) - cy
        pygame.draw.circle(screen, self._color, (draw_x, draw_y), 5)
        pygame.draw.circle(screen, COLOR_WHITE, (draw_x, draw_y), 5, 1)

        # Indicador de impacto al aterrizar
        if self.landed:
            impact_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(impact_surf, (*self._color, 100), (15, 15), 14)
            pygame.draw.circle(impact_surf, (*self._color, 180), (15, 15), 14, 2)
            screen.blit(impact_surf, (draw_x - 15, draw_y - 15))
