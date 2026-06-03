"""
Módulo floor2.py — Piso 2: Administración.

Objetivo: Conseguir la Carpeta de Documentos.
Mecánicas nuevas:
    - Primer guardia de seguridad patrullando.
    - Primera mecánica de distracción (Q para lanzar objetos).
    - La carpeta está detrás del guardia, requiere distraerlo.
"""

import pygame
from levels.base_level import BaseLevel, Door
from entities.player import Player
from entities.guard import Guard
from entities.item import Item
from systems.constants import TILE_SIZE


class Floor2(BaseLevel):
    """
    Piso 2 - Departamento de Administración.

    Introduce el primer guardia de seguridad. El jugador debe
    aprender a usar la mecánica de distracción (tecla Q) para
    cruzar la zona vigilada y obtener la Carpeta de Documentos.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager, floor_number=2)

    def _get_objective(self) -> str:
        return "Conseguir la Carpeta de Documentos"

    def _build_map(self) -> None:
        """
        Mapa del Piso 2 (Administración).

        Estructura:
        - Corredor de entrada al sur con acceso al ascensor.
        - Oficinas abiertas en el centro (zona patrullada).
        - Sala restringida al norte con la carpeta.
        - Cubículos de trabajo para cobertura.
        """
        self.tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 6, 6, 0, 0, 6, 6, 0, 0, 1, 0, 0, 1, 0, 1, 6, 6, 0, 0, 0, 1],
            [1, 0, 6, 5, 0, 0, 6, 5, 0, 0, 1, 0, 0, 1, 1, 1, 6, 5, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 3, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1],
            [1, 0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def _place_entities(self) -> None:
        """
        Coloca entidades del Piso 2.

        - Jugadores en la zona sur.
        - Guardia patrullando el corredor central y un guardia extra custodiando la sala bloqueada.
        - Carpeta en la sala norte restringida.
        - Llave de acceso dentro de la sala bloqueada.
        - Latas y monedas para distracciones.
        """
        ts = TILE_SIZE

        # ── Jugadores (comienzan en zona sur) ──
        p1 = Player(11 * ts + ts // 2, 13 * ts + ts // 2, player_id=1)
        p2 = Player(12 * ts + ts // 2, 13 * ts + ts // 2, player_id=2)
        p1.is_active = True
        self.players = [p1, p2]

        # ── Guardia 1 patrullando el corredor central (fila 6-8) ──
        guard_patrol = [
            (4 * ts + ts // 2, 8 * ts + ts // 2),   # Punto oeste
            (10 * ts + ts // 2, 8 * ts + ts // 2),  # Punto centro
            (17 * ts + ts // 2, 8 * ts + ts // 2),  # Punto este
        ]
        guard1 = Guard(4 * ts + ts // 2, 8 * ts + ts // 2, patrol_points=guard_patrol)
        
        # ── Guardia 2 custodiando la entrada a la sala bloqueada (fila 6) ──
        guard2_patrol = [
            (12 * ts + ts // 2, 6 * ts + ts // 2),
            (15 * ts + ts // 2, 6 * ts + ts // 2)
        ]
        guard2 = Guard(15 * ts + ts // 2, 6 * ts + ts // 2, patrol_points=guard2_patrol)
        
        self.guards = [guard1, guard2]

        # ── Objeto principal: Carpeta de Documentos (zona norte) ──
        self.items.append(Item(11 * ts + ts // 2, 3 * ts + ts // 2,
                               "carpeta"))

        # ── Llave de piso (Dentro de la sala bloqueada en noreste) ──
        self.items.append(Item(18 * ts + ts // 2, 3 * ts + ts // 2, "key_floor_2"))

        # ── Objetos secundarios para distracción ──
        self.items.append(Item(3 * ts + ts // 2, 12 * ts + ts // 2, "lata"))
        self.items.append(Item(18 * ts + ts // 2, 13 * ts + ts // 2, "lata"))
        self.items.append(Item(8 * ts + ts // 2, 12 * ts + ts // 2, "moneda"))
        self.items.append(Item(15 * ts + ts // 2, 7 * ts + ts // 2, "papel"))

    def _on_exit_reached(self) -> None:
        """Requiere la Carpeta de Documentos para avanzar."""
        gd = self.state_manager.game_data
        if gd.inventory.has_item("carpeta"):
            super()._on_exit_reached()
        else:
            self.show_notification(
                "Necesitas la Carpeta de Documentos",
                (220, 80, 80), 2.5
            )
