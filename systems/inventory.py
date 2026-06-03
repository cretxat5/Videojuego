"""
Módulo inventory.py — Sistema de inventario compartido del juego.

Gestiona los objetos recolectados por ambos personajes,
la cantidad de distracciones disponibles y verifica si se
cumplen los requisitos para ganar el juego.

El inventario es compartido entre ambos jugadores.
"""

from systems.constants import ITEM_ID, REQUIRED_ITEMS, DISTRACTION_ITEMS, ACCESS_KEYS


class Inventory:
    """
    Sistema de inventario compartido para ambos personajes.

    Almacena objetos principales (requeridos para ganar) y
    objetos secundarios (usados como distracciones).

    Attributes:
        _items (dict): Diccionario {item_id: cantidad} de objetos recogidos.
        _current_objective (str): Descripción del objetivo actual del nivel.
        _total_collected (int): Contador total de objetos recogidos.
    """

    def __init__(self) -> None:
        """Inicializa el inventario vacío."""
        # Inicializar contadores para cada tipo de objeto
        self._items: dict = {item_id: 0 for item_id in ITEM_ID}
        self._current_objective: str = "Explorar el primer piso"
        self._total_collected: int = 0

    # ──────────────────────────────────────────────
    # GESTIÓN DE OBJETOS
    # ──────────────────────────────────────────────

    def add_item(self, item_id: str) -> bool:
        """
        Agrega un objeto al inventario.

        Args:
            item_id (str): Identificador del objeto a agregar.

        Returns:
            bool: True si el objeto fue agregado exitosamente.
        """
        if item_id not in self._items:
            return False  # Objeto desconocido, ignorar

        self._items[item_id] += 1
        self._total_collected += 1
        return True

    def remove_item(self, item_id: str) -> bool:
        """
        Elimina una unidad de un objeto del inventario.
        Se utiliza al lanzar objetos de distracción.

        Args:
            item_id (str): Identificador del objeto a eliminar.

        Returns:
            bool: True si se pudo eliminar (había al menos uno).
        """
        if item_id in self._items and self._items[item_id] > 0:
            self._items[item_id] -= 1
            return True
        return False

    def has_item(self, item_id: str) -> bool:
        """
        Verifica si el inventario contiene al menos una unidad del objeto.

        Args:
            item_id (str): Identificador del objeto a verificar.

        Returns:
            bool: True si el objeto está en el inventario.
        """
        return self._items.get(item_id, 0) > 0

    def has_key(self, floor_number: int) -> bool:
        """Verifica si el inventario contiene la llave de acceso del piso."""
        key_id = ACCESS_KEYS.get(floor_number)
        return bool(key_id and self.has_item(key_id))

    def get_count(self, item_id: str) -> int:
        """
        Retorna la cantidad de un objeto específico.

        Args:
            item_id (str): Identificador del objeto.

        Returns:
            int: Cantidad disponible en el inventario.
        """
        return self._items.get(item_id, 0)

    def get_distraction_item(self) -> str | None:
        """
        Retorna el identificador de un objeto de distracción disponible.

        Busca en orden: moneda, lata, papel.

        Returns:
            str | None: Identificador del objeto o None si no hay ninguno.
        """
        for item_id in DISTRACTION_ITEMS:
            if self._items.get(item_id, 0) > 0:
                return item_id
        return None

    def has_distraction_item(self) -> bool:
        """
        Verifica si hay al menos un objeto de distracción disponible.

        Returns:
            bool: True si hay objetos de distracción.
        """
        return self.get_distraction_item() is not None

    # ──────────────────────────────────────────────
    # VERIFICACIÓN DE VICTORIA
    # ──────────────────────────────────────────────

    def has_all_required(self) -> bool:
        """
        Verifica si el jugador posee todos los objetos requeridos para ganar.

        Los objetos requeridos están definidos en REQUIRED_ITEMS en constants.py.

        Returns:
            bool: True si se tienen todos los objetos necesarios.
        """
        return all(self._items.get(item_id, 0) > 0 for item_id in REQUIRED_ITEMS)

    def get_missing_items(self) -> list:
        """
        Retorna la lista de objetos requeridos que aún faltan por recoger.

        Returns:
            list: Lista de identificadores de objetos faltantes.
        """
        return [
            item_id for item_id in REQUIRED_ITEMS
            if self._items.get(item_id, 0) == 0
        ]

    # ──────────────────────────────────────────────
    # OBJETIVO ACTUAL
    # ──────────────────────────────────────────────

    def set_objective(self, objective: str) -> None:
        """
        Actualiza la descripción del objetivo actual mostrado en pantalla.

        Args:
            objective (str): Texto descriptivo del objetivo.
        """
        self._current_objective = objective

    @property
    def current_objective(self) -> str:
        """Texto del objetivo actual."""
        return self._current_objective

    # ──────────────────────────────────────────────
    # PROPIEDADES DE SOLO LECTURA
    # ──────────────────────────────────────────────

    @property
    def items(self) -> dict:
        """Diccionario de objetos y sus cantidades (copia de solo lectura)."""
        return dict(self._items)

    @property
    def total_collected(self) -> int:
        """Total acumulado de objetos recogidos durante la partida."""
        return self._total_collected

    # ──────────────────────────────────────────────
    # RENDERIZADO EN PANTALLA
    # ──────────────────────────────────────────────

    def draw(self, screen: object, x: int, y: int) -> None:
        """
        Dibuja el panel de inventario en la posición indicada.

        Muestra los objetos recolectados y el objetivo actual.

        Args:
            screen (pygame.Surface): Superficie de pantalla.
            y (int): Posición Y superior del panel.
            x (int): Posición X izquierda del panel.
        """
        import pygame
        from systems.constants import (
            COLOR_DARK_GRAY, COLOR_WHITE, COLOR_GOLD,
            COLOR_GREEN, COLOR_GRAY, COLOR_LIGHT_GRAY,
        )
        from systems.asset_manager import assets

        panel_width = 200
        panel_height = 300
        padding = 10

        # Fondo semitransparente del panel
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((10, 15, 40, 210))
        pygame.draw.rect(panel, COLOR_GOLD, panel.get_rect(), 1)
        screen.blit(panel, (x, y))

        font_title = assets.get_font(14, bold=True)
        font_item = assets.get_font(12)
        font_obj = assets.get_font(11)

        # Título del panel
        title_surf = font_title.render("INVENTARIO", True, COLOR_GOLD)
        screen.blit(title_surf, (x + padding, y + padding))

        # Mostrar objetos principales (requeridos)
        item_y = y + 35
        screen.blit(font_title.render("Documentos:", True, COLOR_LIGHT_GRAY),
                    (x + padding, item_y))
        item_y += 18

        for req_id in REQUIRED_ITEMS:
            count = self._items.get(req_id, 0)
            color = COLOR_GREEN if count > 0 else COLOR_GRAY
            check = "✓" if count > 0 else "○"
            name = ITEM_ID.get(req_id, req_id)[:18]  # Truncar nombre largo
            text = f"{check} {name}"
            screen.blit(font_item.render(text, True, color), (x + padding, item_y))
            item_y += 16

        # Separador
        item_y += 4
        pygame.draw.line(screen, COLOR_GOLD,
                         (x + padding, item_y), (x + panel_width - padding, item_y))
        item_y += 6

        # Llaves de acceso
        screen.blit(font_title.render("Llaves:", True, COLOR_LIGHT_GRAY),
                    (x + padding, item_y))
        item_y += 18
        for floor, key_id in ACCESS_KEYS.items():
            count = self._items.get(key_id, 0)
            if count > 0:
                text = f"  Piso {floor}"
                screen.blit(font_item.render(text, True, COLOR_GREEN),
                             (x + padding, item_y))
                item_y += 16

        item_y += 4
        pygame.draw.line(screen, COLOR_GOLD,
                         (x + padding, item_y), (x + panel_width - padding, item_y))
        item_y += 6

        # Distracciones disponibles
        screen.blit(font_title.render("Distracciones:", True, COLOR_LIGHT_GRAY),
                    (x + padding, item_y))
        item_y += 18
        for dist_id in DISTRACTION_ITEMS:
            count = self._items.get(dist_id, 0)
            if count > 0:
                name = ITEM_ID.get(dist_id, dist_id)
                text = f"  {name}: {count}"
                screen.blit(font_item.render(text, True, COLOR_GOLD),
                             (x + padding, item_y))
                item_y += 16

        # Objetivo actual
        item_y = y + panel_height - 55
        pygame.draw.line(screen, COLOR_GOLD,
                         (x + padding, item_y), (x + panel_width - padding, item_y))
        item_y += 6
        screen.blit(font_title.render("Objetivo:", True, COLOR_LIGHT_GRAY),
                    (x + padding, item_y))
        item_y += 18
        # Envolver texto largo en varias líneas
        obj_words = self._current_objective.split()
        line = ""
        for word in obj_words:
            test_line = f"{line} {word}".strip()
            if font_obj.size(test_line)[0] < panel_width - 2 * padding:
                line = test_line
            else:
                screen.blit(font_obj.render(line, True, COLOR_WHITE),
                             (x + padding, item_y))
                item_y += 14
                line = word
        if line:
            screen.blit(font_obj.render(line, True, COLOR_WHITE),
                         (x + padding, item_y))
