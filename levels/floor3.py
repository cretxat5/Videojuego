"""
Módulo floor3.py — Piso 3: Recursos Humanos.

Objetivo: Conseguir la Tarjeta de Acceso.
Mecánicas nuevas:
    - Puertas bloqueadas que requieren objetos específicos.
    - Mayor exploración del mapa.
    - Dos guardias con rutas de patrulla distintas.
"""

import pygame
from levels.base_level import BaseLevel, Door
from entities.player import Player
from entities.guard import Guard
from entities.item import Item
from systems.constants import TILE_SIZE


class Floor3(BaseLevel):
    """
    Piso 3 - Recursos Humanos.

    Introduce puertas bloqueadas. Una puerta requiere la Carpeta de
    Documentos (obtenida en piso 2) para abrirse. Hay dos guardias
    con rutas diferentes que complican la exploración.

    El jugador debe navegar por zonas separadas para encontrar
    la Tarjeta de Acceso escondida en la sala de archivos.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager, floor_number=3)

    def _get_objective(self) -> str:
        return "Conseguir la Tarjeta de Acceso"

    def _build_map(self) -> None:
        """
        Mapa del Piso 3 (Recursos Humanos).

        Estructura:
        - Corredor principal horizontal.
        - Zona de oficinas al oeste (acceso libre).
        - Sala de archivos al este (requiere Carpeta).
        - Sala de reuniones al norte (con guardia).
        - Cafetería pequeña al sur.
        """
        self.tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 4, 4, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 6, 6, 0, 1, 0, 5, 5, 0, 1, 0, 0, 1, 0, 6, 6, 6, 6, 0, 0, 1],
            [1, 0, 6, 6, 0, 0, 0, 5, 5, 0, 1, 0, 0, 1, 0, 6, 0, 0, 6, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 6, 5, 5, 6, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 1],
            [1, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 6, 0, 0, 0, 6, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 1],
            [1, 0, 6, 0, 5, 0, 6, 0, 0, 6, 0, 5, 5, 6, 0, 0, 0, 6, 0, 5, 0, 1],
            [1, 0, 6, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 6, 0, 6, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def _place_entities(self) -> None:
        """
        Coloca entidades del Piso 3.

        - Jugadores en la zona sur.
        - Guardias con patrullas ampliadas para cubrir accesos.
        - Tarjeta de acceso en la zona noroeste (accesible).
        - Llave del piso dentro de la sala bloqueada noreste.
        """
        ts = TILE_SIZE

        # ── Jugadores ──
        p1 = Player(11 * ts + ts // 2, 13 * ts + ts // 2, player_id=1)
        p2 = Player(12 * ts + ts // 2, 13 * ts + ts // 2, player_id=2)
        p1.is_active = True
        self.players = [p1, p2]

        # ── Guardia 1: Corredor central este-oeste ──
        guard1_patrol = [
            (3 * ts + ts // 2, 6 * ts + ts // 2),
            (10 * ts + ts // 2, 6 * ts + ts // 2),
            (18 * ts + ts // 2, 6 * ts + ts // 2),
        ]
        guard1 = Guard(3 * ts + ts // 2, 6 * ts + ts // 2, patrol_points=guard1_patrol)
        self.guards.append(guard1)

        # ── Guardia 2: Custodiando la Tarjeta en el noroeste ──
        guard2_patrol = [
            (2 * ts + ts // 2, 3 * ts + ts // 2),
            (6 * ts + ts // 2, 3 * ts + ts // 2),
            (2 * ts + ts // 2, 8 * ts + ts // 2)
        ]
        guard2 = Guard(6 * ts + ts // 2, 3 * ts + ts // 2, patrol_points=guard2_patrol)
        self.guards.append(guard2)

        # ── Objeto principal: Tarjeta de Acceso (movida al noroeste) ──
        self.items.append(Item(3 * ts + ts // 2, 2 * ts + ts // 2, "tarjeta"))

        # ── Llave de piso (Dentro de la sala bloqueada en noreste) ──
        self.items.append(Item(18 * ts + ts // 2, 3 * ts + ts // 2, "key_floor_3"))

        # ── Objetos secundarios ──
        self.items.append(Item(2 * ts + ts // 2, 10 * ts + ts // 2, "lata"))
        self.items.append(Item(19 * ts + ts // 2, 10 * ts + ts // 2, "lata"))
        self.items.append(Item(7 * ts + ts // 2, 7 * ts + ts // 2, "papel"))
        self.items.append(Item(13 * ts + ts // 2, 7 * ts + ts // 2, "moneda"))
        self.items.append(Item(4 * ts + ts // 2, 12 * ts + ts // 2, "moneda"))

        # ── Puerta que requiere Carpeta del piso 2 (pasillo norte, izquierda) ──
        door = Door(7 * ts, 5 * ts, locked=True, required_item="carpeta")
        self.doors.append(door)
        self.wall_rects.append(door.rect)

    def _on_exit_reached(self) -> None:
        """Verifica que el jugador tenga la Tarjeta de Acceso."""
        gd = self.state_manager.game_data
        if gd.inventory.has_item("tarjeta"):
            super()._on_exit_reached()
        else:
            self.show_notification(
                "Necesitas la Tarjeta de Acceso",
                (220, 80, 80), 2.5
            )
