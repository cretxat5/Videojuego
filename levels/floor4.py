"""
Módulo floor4.py — Piso 4: Oficinas Ejecutivas.

Objetivo: Obtener la Hoja de Vida Oficial.
Mecánicas nuevas:
    - Uso obligatorio de AMBOS personajes.
    - Puzzle cooperativo: un personaje distrae al guardia mientras
      el otro abre la puerta con E.
    - Tres guardias con mayor cobertura.
"""

import pygame
from levels.base_level import BaseLevel, Door
from entities.player import Player
from entities.guard import Guard
from entities.item import Item
from systems.constants import TILE_SIZE, COLOR_GOLD


class Floor4(BaseLevel):
    """
    Piso 4 - Oficinas Ejecutivas.

    Nivel más complejo. Requiere coordinar ambos personajes:
    - Personaje 1 lanza una distracción para alejar al guardia.
    - Personaje 2 interactúa con la puerta de la sala VIP.
    - La Hoja de Vida está dentro de la sala VIP.

    Hay un indicador en pantalla que guía al jugador sobre
    qué debe hacer con cada personaje.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        # Rastrear el estado del puzzle cooperativo
        self._puzzle_hint_shown: bool = False
        super().__init__(screen, state_manager, floor_number=4)

    def _get_objective(self) -> str:
        return "Obtener la Hoja de Vida — ¡Usa ambos personajes!"

    def _build_map(self) -> None:
        """
        Mapa del Piso 4 (Oficinas Ejecutivas).

        Estructura:
        - Gran sala ejecutiva central (vigilada por 3 guardias).
        - Sala VIP al norte-centro (puerta bloqueada).
        - Oficinas abiertas al este y oeste.
        - Pasillo de servicio al sur.
        """
        self.tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 4, 4, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 5, 5, 5, 0, 1, 0, 6, 0, 1, 0, 0, 1, 0, 6, 0, 1, 5, 5, 0, 1],
            [1, 0, 5, 6, 5, 0, 0, 0, 6, 0, 1, 0, 0, 1, 0, 6, 0, 0, 5, 6, 0, 1],
            [1, 0, 5, 5, 5, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 5, 5, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 3, 3, 1, 1, 0, 1, 1, 1, 3, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 6, 6, 0, 0, 6, 6, 0, 1],
            [1, 0, 6, 5, 0, 0, 0, 6, 5, 0, 0, 0, 0, 0, 6, 5, 0, 0, 6, 5, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def _place_entities(self) -> None:
        """
        Coloca entidades del Piso 4.

        - Jugadores en el pasillo sur.
        - 3 guardias cubriendo la sala ejecutiva central.
        - Hoja de vida en la sala VIP.
        - Llave de piso 4 en la sala bloqueada este.
        - Puerta VIP requiere la Tarjeta de Acceso.
        """
        ts = TILE_SIZE

        # ── Jugadores ──
        p1 = Player(11 * ts + ts // 2, 13 * ts + ts // 2, player_id=1)
        p2 = Player(12 * ts + ts // 2, 13 * ts + ts // 2, player_id=2)
        p1.is_active = True
        self.players = [p1, p2]

        # ── Guardia 1: Corredor central ──
        g1_patrol = [
            (5 * ts + ts // 2, 7 * ts + ts // 2),
            (16 * ts + ts // 2, 7 * ts + ts // 2),
        ]
        self.guards.append(Guard(5 * ts + ts // 2, 7 * ts + ts // 2, patrol_points=g1_patrol))

        # ── Guardia 2: Zona norte-oeste (custodia zona VIP) ──
        g2_patrol = [
            (2 * ts + ts // 2, 2 * ts + ts // 2),
            (5 * ts + ts // 2, 2 * ts + ts // 2),
            (8 * ts + ts // 2, 4 * ts + ts // 2),
        ]
        self.guards.append(Guard(2 * ts + ts // 2, 2 * ts + ts // 2, patrol_points=g2_patrol))

        # ── Guardia 3: Zona noreste (custodia sala con la llave de piso) ──
        g3_patrol = [
            (15 * ts + ts // 2, 2 * ts + ts // 2),
            (18 * ts + ts // 2, 6 * ts + ts // 2),
        ]
        self.guards.append(Guard(15 * ts + ts // 2, 2 * ts + ts // 2, patrol_points=g3_patrol))

        # ── Objeto principal: Hoja de Vida (sala VIP norte) ──
        self.items.append(Item(8 * ts + ts // 2, 3 * ts + ts // 2, "hoja_vida"))

        # ── Llave de piso (Dentro de la sala bloqueada en el este) ──
        self.items.append(Item(19 * ts + ts // 2, 3 * ts + ts // 2, "key_floor_4"))

        # ── Objetos secundarios ──
        self.items.append(Item(4 * ts + ts // 2, 10 * ts + ts // 2, "lata"))
        self.items.append(Item(17 * ts + ts // 2, 10 * ts + ts // 2, "lata"))
        self.items.append(Item(10 * ts + ts // 2, 10 * ts + ts // 2, "moneda"))
        self.items.append(Item(2 * ts + ts // 2, 14 * ts + ts // 2, "papel"))
        self.items.append(Item(19 * ts + ts // 2, 14 * ts + ts // 2, "papel"))

        # ── Puerta VIP: requiere Tarjeta de Acceso ──
        vip_door = Door(
            11 * ts, 5 * ts,
            locked=True,
            required_item="tarjeta"
        )
        self.doors.append(vip_door)
        self.wall_rects.append(vip_door.rect)

    def _post_init(self) -> None:
        """Muestra hint del puzzle cooperativo al iniciar el nivel."""
        super()._post_init()
        self.show_notification(
            "¡Usa TAB para cambiar de personaje y resolver el puzzle!",
            COLOR_GOLD, 4.0
        )

    def _on_exit_reached(self) -> None:
        """Requiere la Hoja de Vida para avanzar al piso 5."""
        gd = self.state_manager.game_data
        if gd.inventory.has_item("hoja_vida"):
            super()._on_exit_reached()
        else:
            self.show_notification(
                "Necesitas la Hoja de Vida Oficial",
                (220, 80, 80), 2.5
            )
