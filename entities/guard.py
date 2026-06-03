"""
Módulo guard.py — IA de guardias con patrullaje dinámico, visión cónica,
persecución y búsqueda del último punto visto.
"""

import math
import random
import pygame
from systems.constants import (
    GUARD_SPEED, GUARD_CHASE_SPEED, GUARD_SIZE,
    GUARD_COLLISION_WIDTH, GUARD_COLLISION_HEIGHT,
    GUARD_DETECTION_RANGE, GUARD_VIEW_ANGLE, GUARD_SOUND_RANGE,
    GUARD_PATROL_WAIT, GUARD_INVESTIGATE_TIME, GUARD_SEARCH_TIME,
    GUARD_LOST_SIGHT_TIME, COLOR_RED, COLOR_YELLOW, COLOR_WHITE,
    COLOR_GREEN,
)
from systems.asset_manager import assets


GUARD_STATE_PATROL = "patrol"
GUARD_STATE_WATCH = "watch"
GUARD_STATE_ALERT = "alert"
GUARD_STATE_CHASE = "chase"
GUARD_STATE_SEARCH = "search"
GUARD_STATE_RETURN = "return"


_DIR_TO_VEC = {
    "right": (1.0, 0.0),
    "left": (-1.0, 0.0),
    "down": (0.0, 1.0),
    "up": (0.0, -1.0),
}


class Guard(pygame.sprite.Sprite):
    """
    Guardia de seguridad con FSM ampliada.

    Estados:
    - patrol: avanza por puntos de patrulla con variación.
    - watch: se detiene y barre la vista izquierda/derecha.
    - alert: reacción breve al detectar.
    - chase: persigue mientras mantiene contacto visual.
    - search: inspecciona el último punto visto.
    - return: vuelve a su ruta.
    """

    def __init__(self, x: int, y: int, patrol_points: list = None) -> None:
        super().__init__()

        self._start_x = float(x)
        self._start_y = float(y)
        self._float_x = float(x)
        self._float_y = float(y)

        self.patrol_points = patrol_points or [(x, y)]
        self._patrol_index = 0
        self._patrol_direction = 1
        self._patrol_variant_timer = random.uniform(1.5, 3.5)

        self.state = GUARD_STATE_PATROL
        self._state_timer = 0.0
        self._seen_player = False
        self._last_seen_pos = None
        self._last_seen_timer = 0.0
        self._sound_target = None
        self._search_points = []
        self._search_index = 0

        self.speed = GUARD_SPEED
        self.detection_range = GUARD_DETECTION_RANGE
        self.view_angle = GUARD_VIEW_ANGLE
        self.sound_range = GUARD_SOUND_RANGE
        self.direction = "down"
        self._look_angle = self._direction_to_angle(self.direction)
        self._look_target_angle = self._look_angle
        self._watch_side = 1
        self.debug_draw_vision = True

        self._anim_timer = 0.0
        self._anim_frame = 0
        self._alert_pulse = 0.0

        self.image = assets.get_guard_image("down", (GUARD_SIZE, GUARD_SIZE))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.collision_rect = pygame.Rect(
            0, 0, GUARD_COLLISION_WIDTH, GUARD_COLLISION_HEIGHT
        )
        self._sync_collision_rect()

    def _sync_collision_rect(self) -> None:
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.centery = self.rect.centery + 3

    def update(self, delta_time: float, wall_rects: list, players: list) -> bool:
        """
        Actualiza IA y devuelve True solo cuando inicia una nueva detección.
        """
        detected_now = False
        self._update_animation(delta_time)
        self._alert_pulse += delta_time * 3.0
        self._update_look(delta_time)

        visible_player = self._get_visible_player(players, wall_rects)
        if visible_player:
            self._last_seen_pos = visible_player.collision_rect.center
            self._last_seen_timer = GUARD_LOST_SIGHT_TIME
            if self.state not in (GUARD_STATE_ALERT, GUARD_STATE_CHASE):
                detected_now = True
                self.state = GUARD_STATE_ALERT
                self._state_timer = 0.45
            elif self.state == GUARD_STATE_CHASE:
                self._seen_player = True
        else:
            self._last_seen_timer = max(0.0, self._last_seen_timer - delta_time)

        if self.state == GUARD_STATE_PATROL:
            self._update_patrol(delta_time, wall_rects)
        elif self.state == GUARD_STATE_WATCH:
            self._update_watch(delta_time)
        elif self.state == GUARD_STATE_ALERT:
            self._state_timer -= delta_time
            if self._state_timer <= 0:
                self.state = GUARD_STATE_CHASE
        elif self.state == GUARD_STATE_CHASE:
            self._update_chase(delta_time, wall_rects, visible_player)
        elif self.state == GUARD_STATE_SEARCH:
            self._update_search(delta_time, wall_rects)
        elif self.state == GUARD_STATE_RETURN:
            self._update_return(delta_time, wall_rects)

        return detected_now

    def _update_patrol(self, delta_time: float, wall_rects: list) -> None:
        self._patrol_variant_timer -= delta_time
        if self._patrol_variant_timer <= 0 and len(self.patrol_points) > 2:
            if random.random() < 0.35:
                self._patrol_direction *= -1
            elif random.random() < 0.45:
                self._patrol_index = random.randrange(len(self.patrol_points))
            self._patrol_variant_timer = random.uniform(2.5, 5.0)

        target = self.patrol_points[self._patrol_index]
        if self._move_to(target, delta_time, wall_rects, self.speed):
            self.state = GUARD_STATE_WATCH
            self._state_timer = random.uniform(
                GUARD_PATROL_WAIT * 0.6, GUARD_PATROL_WAIT * 1.8
            )
            self._watch_side = random.choice([-1, 1])

    def _update_watch(self, delta_time: float) -> None:
        self._state_timer -= delta_time
        sweep = math.sin(self._alert_pulse * 1.4) * 42.0 * self._watch_side
        self._look_target_angle = self._direction_to_angle(self.direction) + sweep
        if self._state_timer <= 0:
            self._advance_patrol_point()
            self.state = GUARD_STATE_PATROL

    def _update_chase(self, delta_time: float, wall_rects: list, visible_player) -> None:
        if visible_player:
            self._last_seen_pos = visible_player.collision_rect.center
            self._move_to(self._last_seen_pos, delta_time, wall_rects, GUARD_CHASE_SPEED)
            return

        if self._last_seen_pos and self._last_seen_timer > 0:
            self._move_to(self._last_seen_pos, delta_time, wall_rects, GUARD_CHASE_SPEED)
            return

        self._begin_search()

    def _begin_search(self) -> None:
        base = self._last_seen_pos or self.rect.center
        offsets = [(0, 0), (48, 0), (-48, 0), (0, 48), (0, -48)]
        random.shuffle(offsets)
        self._search_points = [(base[0] + ox, base[1] + oy) for ox, oy in offsets]
        self._search_index = 0
        self._state_timer = GUARD_SEARCH_TIME
        self.state = GUARD_STATE_SEARCH

    def _update_search(self, delta_time: float, wall_rects: list) -> None:
        self._state_timer -= delta_time
        if self._search_points:
            target = self._search_points[self._search_index]
            if self._move_to(target, delta_time, wall_rects, self.speed * 0.85):
                self._search_index = (self._search_index + 1) % len(self._search_points)
                self._watch_side *= -1
        self._look_target_angle += math.sin(self._alert_pulse * 2.2) * 2.5
        if self._state_timer <= 0:
            self.state = GUARD_STATE_RETURN

    def _update_return(self, delta_time: float, wall_rects: list) -> None:
        target = self.patrol_points[self._patrol_index]
        if self._move_to(target, delta_time, wall_rects, self.speed):
            self.state = GUARD_STATE_PATROL

    def investigate_sound(self, sound_pos: tuple) -> None:
        """Ordena investigar una distracción sonora."""
        if self.state in (GUARD_STATE_PATROL, GUARD_STATE_WATCH, GUARD_STATE_RETURN):
            self._sound_target = sound_pos
            self._last_seen_pos = sound_pos
            self.state = GUARD_STATE_SEARCH
            self._state_timer = GUARD_INVESTIGATE_TIME
            self._search_points = [
                sound_pos,
                (sound_pos[0] + 40, sound_pos[1]),
                (sound_pos[0] - 40, sound_pos[1]),
                (sound_pos[0], sound_pos[1] + 40),
                (sound_pos[0], sound_pos[1] - 40),
            ]
            self._search_index = 0

    def _advance_patrol_point(self) -> None:
        if len(self.patrol_points) <= 1:
            return
        self._patrol_index += self._patrol_direction
        if self._patrol_index >= len(self.patrol_points):
            self._patrol_index = len(self.patrol_points) - 2
            self._patrol_direction = -1
        elif self._patrol_index < 0:
            self._patrol_index = 1
            self._patrol_direction = 1

    def _move_to(self, target: tuple, delta_time: float, wall_rects: list,
                 speed: float) -> bool:
        tx, ty = float(target[0]), float(target[1])
        dx = tx - self._float_x
        dy = ty - self._float_y
        distance = math.hypot(dx, dy)
        if distance < 5.0:
            return True

        dx /= distance
        dy /= distance
        self._set_direction_from_vector(dx, dy)
        self._move_with_alternatives(dx, dy, delta_time, wall_rects, speed)
        return False

    def _move_with_alternatives(self, dx: float, dy: float, delta_time: float,
                                wall_rects: list, speed: float) -> None:
        amount_x = dx * speed * delta_time
        amount_y = dy * speed * delta_time

        moved_x = self._resolve_axis(amount_x, 0.0, wall_rects)
        moved_y = self._resolve_axis(0.0, amount_y, wall_rects)

        if moved_x == 0 and moved_y == 0:
            # Pequeño rodeo: prueba perpendicular para no quedarse atascado.
            side = random.choice([-1, 1])
            self._resolve_axis(-dy * speed * delta_time * side, 0.0, wall_rects)
            self._resolve_axis(0.0, dx * speed * delta_time * side, wall_rects)

        self.rect.centerx = int(self._float_x)
        self.rect.centery = int(self._float_y)
        self._sync_collision_rect()

    def _resolve_axis(self, move_x: float, move_y: float, wall_rects: list) -> float:
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

    def _get_visible_player(self, players: list, wall_rects: list):
        best_player = None
        best_dist = float("inf")
        for player in players:
            target_rect = getattr(player, "collision_rect", player.rect)
            if self._can_see_point(target_rect.center, wall_rects):
                dist = self._distance_to(target_rect.center)
                if dist < best_dist:
                    best_player = player
                    best_dist = dist
        return best_player

    def _can_see_point(self, target: tuple, wall_rects: list) -> bool:
        gx, gy = self.collision_rect.center
        dx = target[0] - gx
        dy = target[1] - gy
        distance = math.hypot(dx, dy)
        if distance > self.detection_range or distance <= 0:
            return False

        angle_to_target = math.degrees(math.atan2(dy, dx))
        if abs(self._angle_delta(self._look_angle, angle_to_target)) > self.view_angle / 2:
            return False

        line = (gx, gy, target[0], target[1])
        for wall in wall_rects:
            if wall.clipline(line):
                return False
        return True

    def _distance_to(self, target: tuple) -> float:
        return math.hypot(target[0] - self.collision_rect.centerx,
                          target[1] - self.collision_rect.centery)

    def _update_look(self, delta_time: float) -> None:
        self._look_angle += self._angle_delta(
            self._look_angle, self._look_target_angle
        ) * min(1.0, delta_time * 7.5)

    def _set_direction_from_vector(self, dx: float, dy: float) -> None:
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"
        self._look_target_angle = self._direction_to_angle(self.direction)

    def _direction_to_angle(self, direction: str) -> float:
        return {
            "right": 0.0,
            "down": 90.0,
            "left": 180.0,
            "up": -90.0,
        }.get(direction, 90.0)

    def _angle_delta(self, current: float, target: float) -> float:
        return (target - current + 180.0) % 360.0 - 180.0

    def _update_animation(self, delta_time: float) -> None:
        self._anim_timer += delta_time
        if self._anim_timer >= 0.2:
            self._anim_timer = 0.0
            self._anim_frame = 1 - self._anim_frame
        self.image = assets.get_guard_image(self.direction, (GUARD_SIZE, GUARD_SIZE))

    def draw(self, screen: pygame.Surface, camera_offset: tuple = (0, 0)) -> None:
        cx, cy = camera_offset
        draw_rect = self.rect.move(-cx, -cy)

        if self.debug_draw_vision:
            self._draw_vision_cone(screen, camera_offset)

        screen.blit(self.image, draw_rect.topleft)
        self._draw_state_indicator(screen, draw_rect)

    def _draw_vision_cone(self, screen: pygame.Surface, camera_offset: tuple) -> None:
        cx, cy = camera_offset
        gx = self.collision_rect.centerx - cx
        gy = self.collision_rect.centery - cy
        half = self.view_angle / 2
        points = [(gx, gy)]
        for angle in (self._look_angle - half, self._look_angle, self._look_angle + half):
            rad = math.radians(angle)
            points.append((
                gx + math.cos(rad) * self.detection_range,
                gy + math.sin(rad) * self.detection_range,
            ))
        color = (220, 50, 50, 38)
        if self.state in (GUARD_STATE_SEARCH, GUARD_STATE_ALERT):
            color = (255, 230, 0, 48)
        elif self.state == GUARD_STATE_CHASE:
            color = (255, 40, 40, 70)
        cone = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(cone, color, points)
        pygame.draw.lines(cone, (*color[:3], 95), False, points, 1)
        screen.blit(cone, (0, 0))

    def _draw_state_indicator(self, screen: pygame.Surface, draw_rect: pygame.Rect) -> None:
        pulse = abs(math.sin(self._alert_pulse))
        font = assets.get_font(16, bold=True)

        symbols = {
            GUARD_STATE_ALERT: ("!", COLOR_RED),
            GUARD_STATE_CHASE: ("!", COLOR_RED),
            GUARD_STATE_SEARCH: ("?", COLOR_YELLOW),
            GUARD_STATE_WATCH: ("·", COLOR_YELLOW),
            GUARD_STATE_RETURN: ("↺", COLOR_WHITE),
            GUARD_STATE_PATROL: ("", COLOR_GREEN),
        }
        symbol, color = symbols.get(self.state, ("", COLOR_WHITE))
        if symbol:
            surf = font.render(symbol, True, color)
            screen.blit(surf, (draw_rect.centerx - 5, draw_rect.top - 20))
        elif self.state == GUARD_STATE_PATROL:
            pygame.draw.circle(screen, COLOR_GREEN,
                               (draw_rect.centerx, draw_rect.top - 5), 3)
