"""
Módulo floor1.py — Piso 1: Recepción.

Objetivo: Encontrar la Identificación Temporal.
Mecánicas: Movimiento básico, interacción y recolección.
Sin guardias en este piso (introducción al juego).

Layout del mapa (20x15 tiles):
    1 = Pared
    0 = Suelo
    4 = Salida (escalera al piso 2)
    5 = Suelo decorativo
    6 = Mueble/Mostrador
"""

import pygame
from levels.base_level import BaseLevel, Door
from entities.player import Player
from entities.item import Item
from systems.constants import TILE_SIZE


class Floor1(BaseLevel):
    """
    Piso 1 - Recepción del edificio corporativo.

    Es el nivel introductorio: sin guardias, orientado a enseñar
    al jugador los controles de movimiento, recolección e interacción.

    El jugador debe encontrar la Identificación Temporal escondida
    en la sala de espera para poder subir al Piso 2.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        """
        Inicializa el Piso 1.

        Args:
            screen: Superficie de renderizado.
            state_manager: Gestor de estados global.
        """
        super().__init__(screen, state_manager, floor_number=1)

    def _get_objective(self) -> str:
        return "Encontrar la Identificación Temporal"

    def _build_map(self) -> None:
        """
        Define el mapa del Piso 1 (Recepción).

        Estructura:
        - Entrada principal al sur.
        - Mostrador de recepción al centro.
        - Sala de espera al oeste.
        - Pasillo hacia escaleras al norte.
        - Identificación temporal escondida en sala de espera.
        """
        # Mapa 22 columnas × 16 filas
        # 1=Pared, 0=Suelo, 4=Salida, 5=Suelo alt, 6=Mueble
        self.tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 5, 5, 5, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 5, 5, 5, 5, 0, 0, 1],
            [1, 0, 5, 6, 5, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 5, 6, 6, 5, 0, 0, 1],
            [1, 0, 5, 5, 5, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 5, 5, 5, 5, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 6, 6, 6, 6, 6, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 6, 6, 6, 0, 1],
            [1, 0, 6, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 6, 0, 6, 0, 1],
            [1, 0, 6, 0, 5, 0, 6, 0, 0, 0, 6, 5, 0, 5, 6, 0, 0, 6, 0, 6, 0, 1],
            [1, 0, 6, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 6, 0, 6, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def _place_entities(self) -> None:
        """
        Coloca jugadores y objetos en el Piso 1.

        - Jugadores comienzan en la parte inferior central.
        - Identificación temporal en la sala de espera (sala norte-oeste).
        - Llave del piso 1 dentro de la sala bloqueada.
        """
        ts = TILE_SIZE

        # ── Jugadores ──
        p1 = Player(11 * ts + ts // 2, 13 * ts + ts // 2, player_id=1)
        p2 = Player(12 * ts + ts // 2, 13 * ts + ts // 2, player_id=2)
        p1.is_active = True
        self.players = [p1, p2]

        # ── Objeto principal: Identificación Temporal ──
        # Ubicada sobre el mostrador de la sala norte-oeste
        self.items.append(Item(3 * ts + ts // 2, 3 * ts + ts // 2,
                               "identificacion"))

        # ── Llave de piso (Dentro de la sala bloqueada en norte-este) ──
        self.items.append(Item(18 * ts + ts // 2, 3 * ts + ts // 2, "key_floor_1"))

        # ── Objetos secundarios: distracciones ──
        self.items.append(Item(17 * ts + ts // 2, 5 * ts + ts // 2, "moneda"))
        self.items.append(Item(5 * ts + ts // 2, 5 * ts + ts // 2, "papel"))
        self.items.append(Item(10 * ts + ts // 2, 8 * ts + ts // 2, "moneda"))
        self.items.append(Item(15 * ts + ts // 2, 11 * ts + ts // 2, "papel"))

    def _on_exit_reached(self) -> None:
        """
        Verifica que el jugador tenga la identificación antes de subir.
        """
        gd = self.state_manager.game_data
        if gd.inventory.has_item("identificacion"):
            super()._on_exit_reached()
        else:
            self.show_notification(
                "Necesitas la Identificación Temporal",
                (220, 80, 80), 2.5
            )
