"""
Módulo base_level.py — Clase base abstracta para todos los pisos.

Define la interfaz común que todos los niveles deben implementar.
Contiene la lógica compartida de renderizado de tiles, gestión de
entidades, cámara y HUD.

Cada piso hereda de BaseLevel y sobrescribe _build_map() y
_place_entities() para definir su distribrama y entidades.

Tipos de tiles del mapa:
    0 = Suelo transitable
    1 = Pared (bloquea movimiento)
    2 = Puerta normal (abierta)
    3 = Puerta bloqueada (requiere tarjeta)
    4 = Salida / Escalera (avanza al siguiente piso)
    5 = Suelo alternativo (decorativo)
    6 = Mostrador / Escritorio (decorativo, colisiona)
"""

import pygame
from abc import ABC, abstractmethod
from typing import List, Optional
from systems.constants import (
    TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_WALL, COLOR_FLOOR, COLOR_FLOOR_ALT,
    COLOR_DOOR, COLOR_DOOR_LOCKED, COLOR_EXIT,
    COLOR_DARK_GRAY, COLOR_GOLD, COLOR_WHITE,
    COLOR_RED, COLOR_GREEN, COLOR_GRAY,
    MAX_DETECTIONS, ACCESS_KEYS, ITEM_ID, PLAYER_INTERACT_RANGE,
)
from systems.asset_manager import assets
from entities.player import Player
from entities.guard import Guard
from entities.item import Item, DistractionProjectile


class Door:
    """
    Puerta del nivel: puede estar abierta, bloqueada o requerir llave.

    Attributes:
        rect (pygame.Rect): Rectángulo de colisión.
        locked (bool): Si está bloqueada (requiere tarjeta de acceso).
        open (bool): Si está actualmente abierta.
        required_item (str): Item requerido para abrirla (o None).
    """

    def __init__(self, x: int, y: int, locked: bool = False,
                 required_item: str = None, label: str = "") -> None:
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.locked = locked
        self.open = not locked
        self.required_item = required_item
        self.label = label

    def try_open(self, inventory: object) -> bool:
        """
        Intenta abrir la puerta verificando el inventario.

        Args:
            inventory: Objeto Inventory del juego.

        Returns:
            bool: True si se abrió exitosamente.
        """
        if self.open:
            return True
        if self.required_item and inventory.has_item(self.required_item):
            self.open = True
            return True
        return False

    def draw(self, screen: pygame.Surface,
             camera_offset: tuple = (0, 0)) -> None:
        """Dibuja la puerta con color según su estado."""
        cx, cy = camera_offset
        draw_rect = self.rect.move(-cx, -cy)
        if self.open:
            color = COLOR_FLOOR
        elif self.locked:
            color = COLOR_DOOR_LOCKED
        else:
            color = COLOR_DOOR
        pygame.draw.rect(screen, color, draw_rect)
        if not self.open:
            # Candado visual
            pygame.draw.rect(screen, (200, 180, 0),
                             draw_rect.inflate(-8, -8), 2)
            font = assets.get_font(9, bold=True)
            key_text = "LOCK" if not self.label else self.label[:4].upper()
            text = font.render(key_text, True, COLOR_WHITE)
            screen.blit(text, text.get_rect(center=draw_rect.center))


class BaseLevel(ABC):
    """
    Clase base abstracta para todos los pisos del juego.

    Define la estructura común: mapa de tiles, entidades,
    cámara, HUD y lógica de actualización.

    Subclases deben implementar:
        _build_map(): Definir el layout de tiles.
        _place_entities(): Colocar jugadores, guardias y objetos.

    Attributes:
        screen (pygame.Surface): Superficie de renderizado.
        state_manager: Referencia al gestor de estados global.
        floor_number (int): Número del piso (1-5).
        tile_map (list): Matriz 2D de enteros que definen el mapa.
        players (list): Lista de instancias Player.
        guards (list): Lista de instancias Guard.
        items (list): Lista de instancias Item.
        doors (list): Lista de instancias Door.
        exit_rects (list): Rectángulos de salida del nivel.
        wall_rects (list): Rectángulos de paredes para colisión.
        active_player_idx (int): Índice del jugador activo (0 o 1).
        completed (bool): Si el nivel fue completado.
        _projectiles (list): Proyectiles de distracción activos.
        _camera_x (float): Offset de cámara en X.
        _camera_y (float): Offset de cámara en Y.
        _notification (str): Texto de notificación en pantalla.
        _notif_timer (float): Tiempo restante de la notificación.
    """

    def __init__(self, screen: pygame.Surface, state_manager,
                 floor_number: int) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.floor_number = floor_number

        # Estructuras del nivel (se llenan en _build_map)
        self.tile_map: List[List[int]] = []
        self.wall_rects: List[pygame.Rect] = []
        self.exit_rects: List[pygame.Rect] = []
        self.doors: List[Door] = []

        # Entidades
        self.players: List[Player] = []
        self.guards: List[Guard] = []
        self.items: List[Item] = []
        self._projectiles: List[DistractionProjectile] = []

        # Estado del nivel
        self.active_player_idx: int = 0
        self.completed: bool = False

        # Cámara (desplazamiento del mundo)
        self._camera_x: float = 0.0
        self._camera_y: float = 0.0

        # Sistema de notificaciones en pantalla
        self._notification: str = ""
        self._notif_timer: float = 0.0
        self._notif_color: tuple = COLOR_WHITE

        # Límites del mapa en píxeles
        self._map_width: int = 0
        self._map_height: int = 0

        # Inicializar el nivel
        self._build_map()
        self._calculate_wall_rects()
        self._place_entities()
        self._post_init()

    def _post_init(self) -> None:
        """Lógica de post-inicialización ejecutada después de build/place."""
        # Activar el primer jugador
        if self.players:
            self.players[0].is_active = True
        # Actualizar inventario con objetivo del nivel
        gd = self.state_manager.game_data
        gd.inventory.set_objective(self._get_objective())
        self._ensure_progression_key_and_exit_lock()

    @abstractmethod
    def _build_map(self) -> None:
        """Define el layout de tiles del nivel. Implementar en subclase."""
        pass

    @abstractmethod
    def _place_entities(self) -> None:
        """Coloca jugadores, guardias y objetos. Implementar en subclase."""
        pass

    @abstractmethod
    def _get_objective(self) -> str:
        """Retorna el texto del objetivo de este nivel."""
        pass

    # ──────────────────────────────────────────────
    # CONSTRUCCIÓN DEL MAPA
    # ──────────────────────────────────────────────

    def _calculate_wall_rects(self) -> None:
        """
        Convierte la tile_map en rectángulos de colisión de paredes.

        Recorre la matriz y crea pygame.Rect para tiles sólidos
        (paredes, muebles) que bloquean el movimiento.
        """
        self.wall_rects.clear()
        self._map_height = len(self.tile_map)
        self._map_width = len(self.tile_map[0]) if self.tile_map else 0

        for row_idx, row in enumerate(self.tile_map):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                if tile == 1:      # Pared
                    self.wall_rects.append(rect)
                elif tile == 3:    # Puerta bloqueada definida en la matriz
                    from systems.constants import REQUIRED_ITEMS
                    # El objeto requerido es el del nivel actual
                    req_idx = min(self.floor_number - 1, len(REQUIRED_ITEMS) - 1)
                    req_item = REQUIRED_ITEMS[req_idx] if req_idx >= 0 else None
                    door = Door(
                        x, y,
                        locked=True,
                        required_item=req_item,
                        label="SALA"
                    )
                    self.doors.append(door)
                    self.wall_rects.append(door.rect)
                elif tile == 4:    # Salida
                    self.exit_rects.append(rect)
                elif tile == 6:    # Mueble/Mostrador
                    self.wall_rects.append(rect.inflate(-8, -8))

    def _tile_rect(self, col: int, row: int) -> pygame.Rect:
        """Retorna el pygame.Rect de un tile en coordenadas de cuadrícula."""
        return pygame.Rect(col * TILE_SIZE, row * TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)

    def _tile_center(self, col: int, row: int) -> tuple:
        """Retorna el centro en píxeles de un tile."""
        return (col * TILE_SIZE + TILE_SIZE // 2,
                row * TILE_SIZE + TILE_SIZE // 2)

    def _ensure_progression_key_and_exit_lock(self) -> None:
        """
        Bloquea las salidas de pisos 1-4 con la llave del piso.
        (La llave ya debe ser colocada manualmente en las subclases).
        """
        key_id = ACCESS_KEYS.get(self.floor_number)
        if not key_id or self.floor_number >= 5:
            return

        for exit_rect in self.exit_rects:
            if any(door.rect == exit_rect and door.required_item == key_id
                   for door in self.doors):
                continue
            door = Door(
                exit_rect.x, exit_rect.y,
                locked=True,
                required_item=key_id,
                label=f"P{self.floor_number}"
            )
            self.doors.append(door)
            if door.rect not in self.wall_rects:
                self.wall_rects.append(door.rect)

    def _choose_key_spawn(self) -> tuple | None:
        """
        Selecciona una ubicación válida para la llave del piso.

        Se puntúan tiles transitables por distancia al inicio, distancia a
        salidas y separación respecto a objetos ya existentes.
        """
        if not self.tile_map:
            return None

        starts = [p.collision_rect.center for p in self.players] or [(0, 0)]
        exits = [rect.center for rect in self.exit_rects] or starts
        occupied = [item.rect.center for item in self.items]
        best = None
        best_score = -1.0

        for row_idx, row in enumerate(self.tile_map):
            for col_idx, tile in enumerate(row):
                if tile not in (0, 5):
                    continue
                center = self._tile_center(col_idx, row_idx)
                test = pygame.Rect(0, 0, 18, 18)
                test.center = center
                if test.collidelist(self.wall_rects) != -1:
                    continue
                min_start = min(self._dist_sq(center, p) for p in starts)
                min_exit = min(self._dist_sq(center, e) for e in exits)
                min_item = min([self._dist_sq(center, o) for o in occupied] or [999999])
                if min_start < (TILE_SIZE * 5) ** 2:
                    continue
                score = min_start * 1.0 + min_exit * 0.45 + min_item * 0.2
                if score > best_score:
                    best_score = score
                    best = center
        return best

    def _dist_sq(self, a: tuple, b: tuple) -> float:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    # ──────────────────────────────────────────────
    # CÁMARA
    # ──────────────────────────────────────────────

    def _update_camera(self) -> None:
        """
        Centra la cámara en el jugador activo con suavizado.

        La cámara sigue al jugador con interpolación lineal (lerp)
        para un movimiento más suave.
        """
        if not self.players:
            return

        player = self.players[self.active_player_idx]
        target_x = player.rect.centerx - SCREEN_WIDTH // 2
        target_y = player.rect.centery - SCREEN_HEIGHT // 2

        # Lerp de cámara (interpolación suave, factor 0.15)
        lerp = 0.15
        self._camera_x += (target_x - self._camera_x) * lerp
        self._camera_y += (target_y - self._camera_y) * lerp

        # Limitar cámara a los bordes del mapa
        map_px_w = self._map_width * TILE_SIZE
        map_px_h = self._map_height * TILE_SIZE
        self._camera_x = max(0, min(self._camera_x,
                                    max(0, map_px_w - SCREEN_WIDTH)))
        self._camera_y = max(0, min(self._camera_y,
                                    max(0, map_px_h - SCREEN_HEIGHT)))

    @property
    def _camera_offset(self) -> tuple:
        """Offset de cámara como enteros para renderizado."""
        return (int(self._camera_x), int(self._camera_y))

    # ──────────────────────────────────────────────
    # ACTUALIZACIÓN
    # ──────────────────────────────────────────────

    def update(self, delta_time: float) -> None:
        """
        Actualiza toda la lógica del nivel.

        Args:
            delta_time (float): Tiempo transcurrido desde el último frame.
        """
        gd = self.state_manager.game_data
        inventory = gd.inventory

        # ── Entrada del jugador activo ──
        keys = pygame.key.get_pressed()
        if self.players:
            active = self.players[self.active_player_idx]
            dx = keys[pygame.K_d] - keys[pygame.K_a]
            dy = keys[pygame.K_s] - keys[pygame.K_w]
            active.move(float(dx), float(dy), self.wall_rects, delta_time)
            active.update_animation(delta_time)

            # Actualizar animación del personaje inactivo (sin movimiento)
            for i, p in enumerate(self.players):
                if i != self.active_player_idx:
                    p.update_animation(delta_time)

        # ── Guardias ──
        for guard in self.guards:
            detected = guard.update(delta_time, self.wall_rects, self.players)
            if detected:
                gd.detection_count += 1
                assets.play_sound("detect", "detectado.wav")
                self.show_notification("¡TE HAN VISTO!", COLOR_RED, 2.5)
                if gd.detection_count >= MAX_DETECTIONS:
                    from systems.constants import STATE_GAME_OVER
                    self.state_manager.change_state(STATE_GAME_OVER)

        # ── Proyectiles ──
        for proj in self._projectiles[:]:
            proj.update(delta_time)
            if proj.landed:
                # Notificar a guardias cercanos del sonido
                for guard in self.guards:
                    from systems.collision import CollisionSystem
                    if CollisionSystem.check_sound_detection(
                            tuple(proj.end_pos), guard.rect, guard.sound_range):
                        guard.investigate_sound(tuple(proj.end_pos))
                self._projectiles.remove(proj)

        # ── Items ──
        for item in self.items:
            item.update(delta_time)

        # ── Colisión items-jugador ──
        if self.players:
            active = self.players[self.active_player_idx]
            for item in self.items[:]:
                active_hitbox = getattr(active, "collision_rect", active.rect)
                if not item.collected and active_hitbox.colliderect(item.rect):
                    item.collected = True
                    inventory.add_item(item.item_id)
                    assets.play_sound("pickup", "recoger.wav")
                    self.show_notification(
                        f"+ {item.name}", COLOR_GOLD, 2.0
                    )
                    self.items.remove(item)

        # ── Colisión con puertas ──
        if self.players:
            active = self.players[self.active_player_idx]
            for door in self.doors:
                if not door.open and active.rect.colliderect(door.rect):
                    # Bloquear movimiento hacia la puerta
                    pass  # La colisión ya se maneja por wall_rects dinámicos

        # ── Verificar salida del nivel ──
        self._check_exit()

        # ── Cámara ──
        self._update_camera()

        # ── Notificaciones ──
        if self._notif_timer > 0:
            self._notif_timer -= delta_time

    def _check_exit(self) -> None:
        """
        Verifica si el jugador activo llegó a la salida del nivel.

        Mueve al siguiente piso si se cumplen los requisitos.
        """
        if not self.players or self.completed:
            return

        active = self.players[self.active_player_idx]
        for exit_rect in self.exit_rects:
            active_hitbox = getattr(active, "collision_rect", active.rect)
            if active_hitbox.colliderect(exit_rect):
                self._on_exit_reached()

    def _on_exit_reached(self) -> None:
        """
        Maneja el evento de llegar a la salida.
        Puede ser sobrescrito en subclases para requisitos especiales.
        """
        from systems.constants import STATE_WIN
        gd = self.state_manager.game_data

        if self.floor_number < 5:
            key_id = ACCESS_KEYS.get(self.floor_number)
            if key_id and not gd.inventory.has_item(key_id):
                self.show_notification(
                    f"Busca la {ITEM_ID.get(key_id, 'llave de acceso')}",
                    COLOR_RED, 2.5
                )
                return
            gd.current_floor = self.floor_number + 1
            gd.floors_completed += 1
            self.completed = True
            assets.play_sound("level_up", "subir_piso.wav")
            # El LevelManager detectará completed=True y cargará el siguiente piso
        else:
            # Piso 5: verificar si tiene todos los documentos
            if gd.inventory.has_all_required():
                assets.play_sound("win", "victoria.wav")
                self.state_manager.change_state(STATE_WIN)
            else:
                missing = gd.inventory.get_missing_items()
                self.show_notification(
                    f"Faltan documentos: {len(missing)}", COLOR_RED, 3.0
                )

    # ──────────────────────────────────────────────
    # INTERACCIONES
    # ──────────────────────────────────────────────

    def handle_interact(self) -> None:
        """
        Procesa la tecla E: interactuar con puertas y objetos cercanos.
        """
        if not self.players:
            return

        active = self.players[self.active_player_idx]
        inventory = self.state_manager.game_data.inventory

        # Intentar abrir puertas cercanas
        for door in self.doors:
            active_hitbox = getattr(active, "collision_rect", active.rect)
            interact_rect = active_hitbox.inflate(PLAYER_INTERACT_RANGE,
                                                  PLAYER_INTERACT_RANGE)
            if interact_rect.colliderect(door.rect):
                if door.try_open(inventory):
                    assets.play_sound("door", "puerta.wav")
                    self.show_notification("Puerta desbloqueada", COLOR_GREEN, 1.5)
                    # Remover de wall_rects cuando se abre
                    if door.rect in self.wall_rects:
                        self.wall_rects.remove(door.rect)
                else:
                    required = ITEM_ID.get(door.required_item, "Llave de Acceso")
                    self.show_notification(
                        f"Necesitas: {required}", COLOR_RED, 2.0
                    )

    def handle_throw(self) -> None:
        """
        Procesa la tecla Q: lanzar objeto de distracción.
        """
        if not self.players:
            return

        inventory = self.state_manager.game_data.inventory
        dist_item = inventory.get_distraction_item()

        if not dist_item:
            self.show_notification("Sin objetos de distracción", COLOR_GRAY, 1.5)
            return

        active = self.players[self.active_player_idx]

        # Calcular posición destino (delante del jugador)
        directions = {
            "up": (0, -120), "down": (0, 120),
            "left": (-120, 0), "right": (120, 0)
        }
        offset = directions.get(active.direction, (0, 120))
        end_x = active.rect.centerx + offset[0]
        end_y = active.rect.centery + offset[1]

        # Crear proyectil visual
        proj = DistractionProjectile(
            (active.rect.centerx, active.rect.centery),
            (end_x, end_y),
            dist_item
        )
        self._projectiles.append(proj)

        # Consumir objeto del inventario
        inventory.remove_item(dist_item)
        assets.play_sound("throw", "lanzar.wav")
        self.show_notification("¡Objeto lanzado!", COLOR_GOLD, 1.5)

    def handle_switch_player(self) -> None:
        """
        Procesa la tecla TAB: cambiar entre los dos personajes.
        """
        if len(self.players) < 2:
            return

        # Desactivar todos y activar el siguiente
        for p in self.players:
            p.is_active = False

        self.active_player_idx = (self.active_player_idx + 1) % len(self.players)
        self.players[self.active_player_idx].is_active = True
        assets.play_sound("switch", "cambiar.wav")

    # ──────────────────────────────────────────────
    # NOTIFICACIONES
    # ──────────────────────────────────────────────

    def show_notification(self, text: str, color: tuple = None,
                          duration: float = 2.0) -> None:
        """
        Muestra un mensaje temporal en pantalla.

        Args:
            text (str): Texto del mensaje.
            color (tuple): Color del texto.
            duration (float): Duración en segundos.
        """
        self._notification = text
        self._notif_timer = duration
        self._notif_color = color or COLOR_WHITE

    # ──────────────────────────────────────────────
    # RENDERIZADO
    # ──────────────────────────────────────────────

    def draw(self) -> None:
        """
        Dibuja todos los elementos del nivel en el orden correcto:
        1. Tiles del mapa (fondo)
        2. Puertas
        3. Items
        4. Jugadores
        5. Guardias
        6. Proyectiles
        7. HUD (inventario, notificaciones, info)
        """
        self.screen.fill(COLOR_DARK_GRAY)
        cx, cy = self._camera_offset

        # ── Tiles del mapa ──
        self._draw_tiles(cx, cy)

        # ── Puertas ──
        for door in self.doors:
            door.draw(self.screen, (cx, cy))

        # ── Items ──
        for item in self.items:
            item.draw(self.screen, (cx, cy))

        # ── Jugadores ──
        # Dibujar primero los inactivos, luego el activo (encima)
        for i, player in enumerate(self.players):
            if i != self.active_player_idx:
                player.draw(self.screen, (cx, cy))
        if self.players:
            self.players[self.active_player_idx].draw(
                self.screen, (cx, cy)
            )

        # ── Guardias ──
        for guard in self.guards:
            guard.draw(self.screen, (cx, cy))

        # ── Proyectiles ──
        for proj in self._projectiles:
            proj.draw(self.screen, (cx, cy))

        # ── HUD ──
        self._draw_hud()

    def _draw_tiles(self, cx: int, cy: int) -> None:
        """
        Dibuja los tiles del mapa visibles en la cámara.

        Solo dibuja tiles dentro de la ventana para optimizar rendimiento
        (culling de tiles fuera de pantalla).

        Args:
            cx (int): Offset de cámara X.
            cy (int): Offset de cámara Y.
        """
        # Calcular rango de tiles visibles
        start_col = max(0, cx // TILE_SIZE)
        start_row = max(0, cy // TILE_SIZE)
        end_col = min(self._map_width,
                      (cx + SCREEN_WIDTH) // TILE_SIZE + 2)
        end_row = min(self._map_height,
                      (cy + SCREEN_HEIGHT) // TILE_SIZE + 2)

        TILE_COLORS = {
            0: COLOR_FLOOR,
            1: COLOR_WALL,
            2: COLOR_DOOR,
            3: COLOR_DOOR_LOCKED,
            4: COLOR_EXIT,
            5: COLOR_FLOOR_ALT,
            6: (60, 50, 80),  # Mueble/Mostrador
        }

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if row >= len(self.tile_map) or col >= len(self.tile_map[row]):
                    continue
                tile = self.tile_map[row][col]
                color = TILE_COLORS.get(tile, COLOR_FLOOR)

                draw_x = col * TILE_SIZE - cx
                draw_y = row * TILE_SIZE - cy
                rect = pygame.Rect(draw_x, draw_y, TILE_SIZE, TILE_SIZE)

                pygame.draw.rect(self.screen, color, rect)

                # Borde sutil entre tiles
                if tile != 1:
                    pygame.draw.rect(self.screen,
                                     (max(0, color[0] - 15),
                                      max(0, color[1] - 15),
                                      max(0, color[2] - 15)),
                                     rect, 1)

                # Ícono especial para salida
                if tile == 4:
                    font = assets.get_font(10, bold=True)
                    label = font.render("▲", True, COLOR_WHITE)
                    lrect = label.get_rect(center=rect.center)
                    self.screen.blit(label, lrect)

    def _draw_hud(self) -> None:
        """
        Dibuja la interfaz de usuario (HUD) superpuesta al juego.

        Incluye: inventario, indicador de piso, conteo de detecciones
        y notificaciones temporales.
        """
        gd = self.state_manager.game_data

        # ── Panel inventario (esquina derecha) ──
        inv_x = SCREEN_WIDTH - 210
        inv_y = 10
        gd.inventory.draw(self.screen, inv_x, inv_y)

        # ── Indicador de piso ──
        font_big = assets.get_font(18, bold=True)
        floor_surf = font_big.render(
            f"PISO {self.floor_number}", True, COLOR_GOLD
        )
        self.screen.blit(floor_surf, (15, 15))

        # ── Conteo de detecciones ──
        font_sm = assets.get_font(13)
        detect_color = COLOR_RED if gd.detection_count > 0 else COLOR_GRAY
        detect_text = f"Detecciones: {gd.detection_count}/{MAX_DETECTIONS}"
        self.screen.blit(
            font_sm.render(detect_text, True, detect_color), (15, 42)
        )

        # ── Controles rápidos ──
        hint_font = assets.get_font(11)
        hints = [
            "WASD: Mover",
            "TAB: Cambiar personaje",
            "E: Interactuar",
            "Q: Lanzar distracción",
            "ESC: Pausa",
        ]
        for i, hint in enumerate(hints):
            surf = hint_font.render(hint, True, (140, 145, 165))
            self.screen.blit(surf, (15, SCREEN_HEIGHT - 90 + i * 14))

        # ── Notificación temporal ──
        if self._notif_timer > 0 and self._notification:
            alpha = min(255, int(255 * self._notif_timer))
            notif_font = assets.get_font(20, bold=True)
            text_surf = notif_font.render(self._notification, True,
                                          self._notif_color)
            text_rect = text_surf.get_rect(
                centerx=SCREEN_WIDTH // 2,
                centery=SCREEN_HEIGHT // 2 - 60
            )
            # Fondo semitransparente
            bg = pygame.Surface(
                (text_rect.width + 20, text_rect.height + 10),
                pygame.SRCALPHA
            )
            bg.fill((0, 0, 0, min(180, alpha)))
            self.screen.blit(bg, (text_rect.x - 10, text_rect.y - 5))
            text_surf.set_alpha(alpha)
            self.screen.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Maneja eventos de teclado durante el juego.

        Args:
            event: Evento de Pygame.
        """
        from systems.constants import STATE_PAUSED

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(STATE_PAUSED)
            elif event.key == pygame.K_TAB:
                self.handle_switch_player()
            elif event.key == pygame.K_e:
                self.handle_interact()
            elif event.key == pygame.K_q:
                self.handle_throw()
