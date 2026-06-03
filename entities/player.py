"""
Módulo player.py — Clase Player: personaje jugable.

Maneja movimiento en cuatro direcciones, interacción con objetos,
lanzamiento de distracciones y representación visual del personaje.

Cada instancia representa uno de los dos estudiantes del juego.
"""

import pygame
from systems.constants import (
    PLAYER_SPEED, PLAYER_SIZE, PLAYER_COLLISION_WIDTH,
    PLAYER_COLLISION_HEIGHT, PLAYER_INTERACT_RANGE,
    COLOR_BLUE, COLOR_ORANGE, COLOR_WHITE, COLOR_GOLD,
    TILE_SIZE,
)
from systems.asset_manager import assets


class Player(pygame.sprite.Sprite):
    """
    Personaje jugable controlado por el usuario.

    Hereda de pygame.sprite.Sprite para integrarse con el
    sistema de sprites y grupos de Pygame.

    Attributes:
        player_id (int): Identificador del personaje (1 o 2).
        rect (pygame.Rect): Rectángulo de colisión y posición.
        speed (float): Velocidad de movimiento en píxeles/segundo.
        direction (str): Dirección actual ("up","down","left","right").
        is_active (bool): Si este personaje es el activo controlado.
        _anim_timer (float): Temporizador para animación de movimiento.
        _anim_frame (int): Frame actual de la animación.
        _move_trail (list): Historial de posiciones para efecto de trail.
    """

    def __init__(self, x: int, y: int, player_id: int) -> None:
        """
        Inicializa el personaje en una posición del mapa.

        Args:
            x (int): Posición X inicial en píxeles.
            y (int): Posición Y inicial en píxeles.
            player_id (int): 1 o 2 para identificar el personaje.
        """
        super().__init__()

        self.player_id: int = player_id
        self.speed: float = PLAYER_SPEED
        self.direction: str = "down"
        self.is_active: bool = False

        # Animación: temporizador y frame
        self._anim_timer: float = 0.0
        self._anim_frame: int = 0
        self._anim_speed: float = 0.15  # Segundos por frame
        self._is_moving: bool = False

        # Efecto de trail (huella visual al moverse)
        self._move_trail: list = []
        self._trail_max: int = 4

        # Color del indicador según personaje
        self.indicator_color: tuple = COLOR_BLUE if player_id == 1 else COLOR_ORANGE

        # Cargar imagen del personaje
        self.image: pygame.Surface = assets.get_player_image(
            player_id, "down", (PLAYER_SIZE, PLAYER_SIZE)
        )

        # Crear rectángulo de colisión centrado en (x, y)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.collision_rect: pygame.Rect = pygame.Rect(
            0, 0, PLAYER_COLLISION_WIDTH, PLAYER_COLLISION_HEIGHT
        )
        self._sync_collision_rect()

        # Posición en punto flotante para mayor precisión de movimiento
        self._float_x: float = float(x)
        self._float_y: float = float(y)

    def _sync_collision_rect(self) -> None:
        """Mantiene el hitbox en la zona baja del sprite para colisiones más naturales."""
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.centery = self.rect.centery + 3

    # ──────────────────────────────────────────────
    # MOVIMIENTO
    # ──────────────────────────────────────────────

    def move(self, dx: float, dy: float, wall_rects: list,
             delta_time: float) -> None:
        """
        Mueve el personaje aplicando la velocidad y detectando colisiones.

        El movimiento diagonal se normaliza para evitar velocidad mayor.
        Usa separación de ejes X/Y para deslizamiento en paredes.

        Args:
            dx (float): Dirección horizontal (-1, 0, 1).
            dy (float): Dirección vertical (-1, 0, 1).
            wall_rects (list): Lista de pygame.Rect de las paredes.
            delta_time (float): Tiempo transcurrido (segundos).
        """
        # Normalizar movimiento diagonal
        if dx != 0 and dy != 0:
            factor = 0.7071  # 1 / sqrt(2)
            dx *= factor
            dy *= factor

        # Actualizar dirección visual
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"

        # Calcular desplazamiento en píxeles
        move_x = dx * self.speed * delta_time
        move_y = dy * self.speed * delta_time

        self._is_moving = (dx != 0 or dy != 0)

        move_x = self._resolve_axis(move_x, 0.0, wall_rects)
        move_y = self._resolve_axis(0.0, move_y, wall_rects)

        # Actualizar rectángulo desde posición flotante
        self.rect.centerx = int(self._float_x)
        self.rect.centery = int(self._float_y)
        self._sync_collision_rect()

        # Guardar posición para efecto trail
        if self._is_moving and (move_x != 0 or move_y != 0):
            self._move_trail.append((self.rect.centerx, self.rect.centery))
            if len(self._move_trail) > self._trail_max:
                self._move_trail.pop(0)

    def _resolve_axis(self, move_x: float, move_y: float, wall_rects: list) -> float:
        """
        Aplica movimiento en pasos pequeños para evitar atravesar esquinas.

        El hitbox es menor que el sprite, así que los pasillos se sienten más
        justos visualmente sin que el jugador choque con píxeles invisibles.
        """
        amount = move_x if move_x != 0 else move_y
        if amount == 0:
            return 0.0

        sign = 1 if amount > 0 else -1
        remaining = abs(amount)
        moved = 0.0

        while remaining > 0:
            step = min(remaining, 3.0)
            test_rect = self.collision_rect.copy()
            if move_x != 0:
                test_rect.x += int(round(step * sign))
            else:
                test_rect.y += int(round(step * sign))

            if test_rect.collidelist(wall_rects) != -1:
                break

            if move_x != 0:
                self._float_x += step * sign
                self.rect.centerx = int(self._float_x)
            else:
                self._float_y += step * sign
                self.rect.centery = int(self._float_y)
            self._sync_collision_rect()
            moved += step * sign
            remaining -= step

        return moved

    def set_position(self, x: int, y: int) -> None:
        """
        Teletransporta el personaje a una nueva posición.

        Args:
            x (int): Nueva posición X (centro).
            y (int): Nueva posición Y (centro).
        """
        self._float_x = float(x)
        self._float_y = float(y)
        self.rect.centerx = x
        self.rect.centery = y
        self._sync_collision_rect()
        self._move_trail.clear()

    # ──────────────────────────────────────────────
    # ANIMACIÓN
    # ──────────────────────────────────────────────

    def update_animation(self, delta_time: float) -> None:
        """
        Actualiza el frame de animación según el movimiento.

        Alterna entre frames de caminata cuando el personaje se mueve.
        Cuando está quieto muestra el frame 0 (postura neutra).

        Args:
            delta_time (float): Tiempo transcurrido (segundos).
        """
        if self._is_moving:
            self._anim_timer += delta_time
            if self._anim_timer >= self._anim_speed:
                self._anim_timer = 0.0
                # Alternar entre frame 0 y 1 (walk cycle básico)
                self._anim_frame = 1 - self._anim_frame
        else:
            self._anim_frame = 0
            self._anim_timer = 0.0

        # Actualizar imagen según dirección y frame
        suffix = f"_{self._anim_frame}" if self._anim_frame > 0 else ""
        self.image = assets.get_player_image(
            self.player_id,
            self.direction + suffix if self._anim_frame > 0 else self.direction,
            (PLAYER_SIZE, PLAYER_SIZE)
        )

    # ──────────────────────────────────────────────
    # RENDERIZADO
    # ──────────────────────────────────────────────

    def draw(self, screen: pygame.Surface,
             camera_offset: tuple = (0, 0)) -> None:
        """
        Dibuja el personaje en pantalla con efectos visuales.

        Incluye: trail de movimiento, sprite del personaje,
        indicador del personaje activo e indicador de nombre.

        Args:
            screen (pygame.Surface): Superficie de renderizado.
            camera_offset (tuple): Desplazamiento de cámara (cx, cy).
        """
        cx, cy = camera_offset

        # ── Efecto trail de movimiento (solo activo) ──
        if self.is_active and len(self._move_trail) > 1:
            for i, pos in enumerate(self._move_trail[:-1]):
                alpha = int(80 * (i / len(self._move_trail)))
                radius = max(3, PLAYER_SIZE // 4 - i)
                trail_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    trail_surf,
                    (*self.indicator_color, alpha),
                    (radius, radius), radius
                )
                screen.blit(
                    trail_surf,
                    (pos[0] - radius - cx, pos[1] - radius - cy)
                )

        # ── Indicador de personaje activo (círculo pulsante debajo) ──
        if self.is_active:
            draw_x = self.rect.centerx - cx
            draw_y = self.rect.centery - cy
            # Sombra/glow bajo el personaje
            glow_surf = pygame.Surface((PLAYER_SIZE + 8, PLAYER_SIZE + 8),
                                       pygame.SRCALPHA)
            pygame.draw.ellipse(
                glow_surf,
                (*self.indicator_color, 120),
                glow_surf.get_rect()
            )
            screen.blit(glow_surf,
                        (draw_x - PLAYER_SIZE // 2 - 4,
                         draw_y + PLAYER_SIZE // 4))

        # ── Sprite del personaje ──
        draw_rect = self.rect.move(-cx, -cy)
        screen.blit(self.image, draw_rect.topleft)

        # ── Indicador de nombre sobre el personaje ──
        font = assets.get_font(10, bold=True)
        label = f"P{self.player_id}"
        color = self.indicator_color if self.is_active else (150, 150, 160)
        label_surf = font.render(label, True, color)
        label_rect = label_surf.get_rect(
            centerx=draw_rect.centerx,
            bottom=draw_rect.top - 2
        )
        screen.blit(label_surf, label_rect)

        # ── Borde brillante si está activo ──
        if self.is_active:
            border_rect = draw_rect.inflate(4, 4)
            pygame.draw.rect(screen, self.indicator_color, border_rect, 2)
