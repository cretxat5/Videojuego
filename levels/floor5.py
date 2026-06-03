"""
Módulo floor5.py — Piso 5: Dirección General.

Objetivo: Llegar a la oficina del Director General con TODOS los documentos.
Mecánicas:
    - Verificación de inventario completo.
    - Guardia elite con mayor rango de detección.
    - Nivel final: diseño imponente.
    - Zona de entrevista como tile de victoria.
"""

import pygame
from levels.base_level import BaseLevel, Door
from entities.player import Player
from entities.guard import Guard
from entities.item import Item
from systems.constants import TILE_SIZE, COLOR_GOLD, COLOR_GREEN


class Floor5(BaseLevel):
    """
    Piso 5 - Dirección General. El nivel final.

    El jugador debe llegar a la oficina del Director General.
    Condición de victoria: poseer los 4 documentos requeridos
    y alcanzar el tile de salida (escritorio del director).

    Hay un guardia elite con mayor rango de detección que
    protege el acceso final.
    """

    def __init__(self, screen: pygame.Surface, state_manager) -> None:
        super().__init__(screen, state_manager, floor_number=5)

    def _get_objective(self) -> str:
        return "¡Llegar a la oficina del Director con todos los documentos!"

    def _build_map(self) -> None:
        """
        Mapa del Piso 5 (Dirección General).

        Estructura:
        - Pasillo de acceso al sur.
        - Sala de secretaría al centro.
        - Oficina del director al norte (sala grande).
        - Sala de espera VIP al este.
        - Escritorio del director = tile de victoria (4).
        """
        self.tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 5, 5, 5, 5, 5, 5, 1, 0, 6, 6, 0, 1, 5, 5, 5, 5, 5, 5, 1, 1],
            [1, 1, 5, 6, 6, 6, 6, 5, 1, 0, 6, 6, 0, 1, 5, 6, 6, 6, 6, 5, 1, 1],
            [1, 1, 5, 6, 0, 0, 6, 5, 0, 0, 0, 0, 0, 0, 5, 6, 0, 0, 6, 5, 1, 1],
            [1, 1, 5, 5, 5, 5, 5, 5, 1, 0, 0, 0, 0, 1, 5, 5, 5, 5, 5, 5, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 1],
            [1, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def _place_entities(self) -> None:
        """
        Coloca entidades del Piso 5 (nivel final).

        - Jugadores en la zona sur.
        - Guardia elite frente a la oficina del director.
        - Guardia de patrulla en el corredor central.
        - Objetos secundarios de distracción.
        """
        ts = TILE_SIZE

        # ── Jugadores ──
        p1 = Player(11 * ts + ts // 2, 13 * ts + ts // 2, player_id=1)
        p2 = Player(12 * ts + ts // 2, 13 * ts + ts // 2, player_id=2)
        p1.is_active = True
        self.players = [p1, p2]

        # ── Guardia elite frente a la oficina del director ──
        # Tiene rango de detección aumentado
        elite_guard = Guard(
            10 * ts + ts // 2, 7 * ts + ts // 2,
            patrol_points=[
                (8 * ts + ts // 2, 7 * ts + ts // 2),
                (13 * ts + ts // 2, 7 * ts + ts // 2),
            ]
        )
        elite_guard.detection_range = 160  # Mayor rango de detección (global es 130)
        elite_guard.speed = 85             # Más rápido
        self.guards.append(elite_guard)

        # ── Guardia de patrulla corredor ──
        patrol_guard = Guard(
            4 * ts + ts // 2, 11 * ts + ts // 2,
            patrol_points=[
                (2 * ts + ts // 2, 11 * ts + ts // 2),
                (10 * ts + ts // 2, 11 * ts + ts // 2),
                (19 * ts + ts // 2, 11 * ts + ts // 2),
            ]
        )
        self.guards.append(patrol_guard)

        # ── Guardia adicional en zona lateral ──
        side_guard = Guard(
            17 * ts + ts // 2, 8 * ts + ts // 2,
            patrol_points=[
                (15 * ts + ts // 2, 8 * ts + ts // 2),
                (19 * ts + ts // 2, 8 * ts + ts // 2),
            ]
        )
        self.guards.append(side_guard)

        # ── Objetos secundarios ──
        self.items.append(Item(3 * ts + ts // 2, 12 * ts + ts // 2, "lata"))
        self.items.append(Item(18 * ts + ts // 2, 12 * ts + ts // 2, "lata"))
        self.items.append(Item(10 * ts + ts // 2, 11 * ts + ts // 2, "moneda"))
        self.items.append(Item(6 * ts + ts // 2, 8 * ts + ts // 2, "papel"))
        self.items.append(Item(15 * ts + ts // 2, 8 * ts + ts // 2, "papel"))

        # ── Puerta de acceso a la secretaría ──
        door1 = Door(5 * ts, 6 * ts, locked=False)
        door2 = Door(16 * ts, 6 * ts, locked=False)
        self.doors.extend([door1, door2])

        # ── Puerta final (oficina del director) ──
        final_door = Door(
            9 * ts, 6 * ts,
            locked=True,
            required_item="identificacion"  # Simbólico: identificación ya la tienen
        )
        # Se abre automáticamente si tienen todos los documentos
        self.doors.append(final_door)
        self.wall_rects.append(final_door.rect)

    def _post_init(self) -> None:
        """Muestra mensaje motivacional al llegar al piso final."""
        super()._post_init()
        self.show_notification(
            "¡Último piso! Llega al escritorio del Director.",
            COLOR_GOLD, 4.0
        )

    def handle_interact(self) -> None:
        """
        Sobrescribe la interacción para la puerta final:
        se abre si el jugador tiene TODOS los documentos requeridos.
        """
        if not self.players:
            return

        active = self.players[self.active_player_idx]
        inventory = self.state_manager.game_data.inventory

        for door in self.doors:
            interact_rect = active.rect.inflate(30, 30)
            if interact_rect.colliderect(door.rect) and not door.open:
                if inventory.has_all_required():
                    door.open = True
                    if door.rect in self.wall_rects:
                        self.wall_rects.remove(door.rect)
                    self.show_notification(
                        "¡Acceso concedido! Entra a la entrevista.",
                        COLOR_GREEN, 3.0
                    )
                else:
                    missing = len(inventory.get_missing_items())
                    self.show_notification(
                        f"Faltan {missing} documento(s) para entrar.",
                        (220, 80, 80), 2.5
                    )
                return

        # Si no hay puerta, llamar interacción base
        super().handle_interact()

    def _on_exit_reached(self) -> None:
        """
        Victoria: verifica que tenga todos los documentos y activa la pantalla WIN.
        """
        gd = self.state_manager.game_data
        if gd.inventory.has_all_required():
            from systems.constants import STATE_WIN
            from systems.asset_manager import assets
            assets.play_sound("win", "victoria.wav")
            self.state_manager.change_state(STATE_WIN)
        else:
            missing = len(gd.inventory.get_missing_items())
            self.show_notification(
                f"¡Faltan {missing} documento(s) para la entrevista!",
                (220, 80, 80), 3.0
            )
