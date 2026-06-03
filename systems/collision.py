"""
Módulo collision.py — Sistema de detección y resolución de colisiones.

Implementa colisiones basadas en rectángulos (AABB - Axis-Aligned Bounding Boxes),
técnica fundamental en computación gráfica 2D.

Métodos de colisión utilizados de Pygame:
- pygame.Rect.colliderect(): colisión entre dos rectángulos.
- pygame.Rect.collidelist(): colisión entre un rect y una lista.
- pygame.sprite.spritecollide(): colisión entre sprites.
"""

import pygame
from typing import Optional


class CollisionSystem:
    """
    Sistema de gestión de colisiones del juego.

    Centraliza toda la lógica de detección de colisiones para
    mantener el código de las entidades limpio y modular.

    Utiliza el método AABB (Axis-Aligned Bounding Box) que verifica
    si dos rectángulos se superponen en los ejes X e Y.
    """

    @staticmethod
    def check_wall_collision(entity_rect: pygame.Rect,
                              walls: list,
                              dx: float,
                              dy: float) -> tuple:
        """
        Verifica y resuelve colisiones con paredes.

        Separa el movimiento en ejes X e Y para permitir deslizamiento
        a lo largo de las paredes (no quedar completamente bloqueado).

        Algoritmo:
        1. Mover en el eje X y verificar colisión.
        2. Si hay colisión, revertir el movimiento en X.
        3. Mover en el eje Y y verificar colisión.
        4. Si hay colisión, revertir el movimiento en Y.

        Args:
            entity_rect (pygame.Rect): Rectángulo del jugador o entidad.
            walls (list): Lista de pygame.Rect que representan paredes.
            dx (float): Desplazamiento deseado en el eje X.
            dy (float): Desplazamiento deseado en el eje Y.

        Returns:
            tuple: (new_dx, new_dy) movimientos permitidos después de colisión.
        """
        # ── Movimiento en eje X ──
        test_rect_x = entity_rect.copy()
        test_rect_x.x += int(dx)

        if test_rect_x.collidelist(walls) != -1:
            dx = 0  # Bloquear movimiento horizontal

        # ── Movimiento en eje Y ──
        test_rect_y = entity_rect.copy()
        test_rect_y.y += int(dy)

        if test_rect_y.collidelist(walls) != -1:
            dy = 0  # Bloquear movimiento vertical

        return dx, dy

    @staticmethod
    def check_item_collision(entity_rect: pygame.Rect,
                              items: list) -> Optional[object]:
        """
        Detecta si el jugador está sobre un objeto recolectable.

        Args:
            entity_rect (pygame.Rect): Rectángulo del jugador.
            items (list): Lista de objetos Item con atributo rect.

        Returns:
            Item | None: El objeto colisionado o None.
        """
        for item in items:
            if entity_rect.colliderect(item.rect):
                return item
        return None

    @staticmethod
    def check_door_collision(entity_rect: pygame.Rect,
                              doors: list) -> Optional[object]:
        """
        Detecta si el jugador intenta cruzar una puerta.

        Args:
            entity_rect (pygame.Rect): Rectángulo del jugador.
            doors (list): Lista de objetos Door con atributo rect.

        Returns:
            Door | None: La puerta colisionada o None.
        """
        for door in doors:
            if entity_rect.colliderect(door.rect):
                return door
        return None

    @staticmethod
    def check_exit_collision(entity_rect: pygame.Rect,
                             exits: list) -> bool:
        """
        Verifica si el jugador ha llegado a una salida o escalera.

        Args:
            entity_rect (pygame.Rect): Rectángulo del jugador.
            exits (list): Lista de pygame.Rect que representan salidas.

        Returns:
            bool: True si hay colisión con una salida.
        """
        for exit_rect in exits:
            if entity_rect.colliderect(exit_rect):
                return True
        return False

    @staticmethod
    def check_guard_detection(player_rect: pygame.Rect,
                               guard_rect: pygame.Rect,
                               detection_range: int) -> bool:
        """
        Verifica si un guardia detecta al jugador.

        Utiliza distancia entre centros de los rectángulos,
        lo que crea un radio de detección circular.

        Args:
            player_rect (pygame.Rect): Rectángulo del jugador.
            guard_rect (pygame.Rect): Rectángulo del guardia.
            detection_range (int): Radio de detección en píxeles.

        Returns:
            bool: True si el jugador está dentro del rango de detección.
        """
        # Calcular distancia euclidiana entre centros
        px, py = player_rect.centerx, player_rect.centery
        gx, gy = guard_rect.centerx, guard_rect.centery
        distance_sq = (px - gx) ** 2 + (py - gy) ** 2

        # Comparar con el cuadrado del rango (evita raíz cuadrada costosa)
        return distance_sq <= detection_range ** 2

    @staticmethod
    def check_sound_detection(sound_pos: tuple,
                               guard_rect: pygame.Rect,
                               sound_range: int) -> bool:
        """
        Verifica si un guardia escucha un sonido de distracción.

        Args:
            sound_pos (tuple): Coordenadas (x, y) del sonido.
            guard_rect (pygame.Rect): Rectángulo del guardia.
            sound_range (int): Radio de escucha en píxeles.

        Returns:
            bool: True si el guardia puede escuchar el sonido.
        """
        gx, gy = guard_rect.centerx, guard_rect.centery
        distance_sq = (sound_pos[0] - gx) ** 2 + (sound_pos[1] - gy) ** 2
        return distance_sq <= sound_range ** 2

    @staticmethod
    def get_interaction_targets(player_rect: pygame.Rect,
                                 interactables: list,
                                 interact_range: int) -> list:
        """
        Retorna todos los objetos interactuables dentro del rango del jugador.

        Args:
            player_rect (pygame.Rect): Rectángulo del jugador.
            interactables (list): Lista de objetos con atributo rect y método interact.
            interact_range (int): Distancia máxima de interacción.

        Returns:
            list: Objetos dentro del rango de interacción.
        """
        result = []
        px, py = player_rect.centerx, player_rect.centery

        for obj in interactables:
            ox, oy = obj.rect.centerx, obj.rect.centery
            distance_sq = (px - ox) ** 2 + (py - oy) ** 2
            if distance_sq <= interact_range ** 2:
                result.append(obj)

        return result
