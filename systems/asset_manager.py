"""
Módulo asset_manager.py — Gestor centralizado de recursos multimedia.

Responsabilidades:
- Cargar imágenes, sonidos y fuentes una única vez (caché).
- Generar superficies de respaldo cuando un archivo no existe.
- Proveer acceso global a todos los recursos del juego.

Esto evita cargar el mismo archivo múltiples veces y facilita
el manejo de errores cuando faltan recursos externos.
"""

import os
import pygame
from systems.constants import (
    ASSETS_DIR, FONTS_DIR, SOUNDS_DIR, PLAYERS_DIR,
    GUARDS_DIR, ITEMS_DIR, BACKGROUNDS_DIR,
    COLOR_BLUE, COLOR_ORANGE, COLOR_RED, COLOR_GREEN,
    COLOR_GOLD, COLOR_GRAY, TILE_SIZE,
)


class AssetManager:
    """
    Gestor de recursos multimedia del juego.

    Carga y almacena en caché imágenes, sonidos y fuentes.
    Si un recurso no existe, genera una superficie de respaldo
    para que el juego pueda ejecutarse sin archivos externos.

    Attributes:
        _images (dict): Caché de superficies de imagen cargadas.
        _sounds (dict): Caché de objetos de sonido cargados.
        _fonts (dict): Caché de fuentes cargadas.
    """

    def __init__(self) -> None:
        """Inicializa los diccionarios de caché de recursos."""
        self._images: dict = {}
        self._sounds: dict = {}
        self._fonts: dict = {}

    # ──────────────────────────────────────────────
    # IMÁGENES
    # ──────────────────────────────────────────────

    def get_image(self, key: str, path: str,
                  size: tuple = None) -> pygame.Surface:
        """
        Carga una imagen desde disco o la retorna desde caché.

        Si el archivo no existe, genera una superficie de color sólido
        como respaldo visual para no interrumpir la ejecución.

        Args:
            key (str): Identificador único para la caché.
            path (str): Ruta completa al archivo de imagen.
            size (tuple, optional): (ancho, alto) para escalar la imagen.

        Returns:
            pygame.Surface: Superficie lista para dibujar.
        """
        cache_key = f"{key}_{size}"
        if cache_key in self._images:
            return self._images[cache_key]

        if os.path.exists(path):
            try:
                image = pygame.image.load(path).convert_alpha()
                if size:
                    image = pygame.transform.scale(image, size)
            except pygame.error:
                image = self._create_fallback_surface(size or (TILE_SIZE, TILE_SIZE), key)
        else:
            # Crear superficie de respaldo si el archivo no existe
            image = self._create_fallback_surface(size or (TILE_SIZE, TILE_SIZE), key)

        self._images[cache_key] = image
        return image

    def _create_fallback_surface(self, size: tuple, key: str) -> pygame.Surface:
        """
        Genera una superficie de respaldo cuando no existe el archivo.

        La superficie muestra un rectángulo de color con el identificador
        del recurso para facilitar la identificación visual durante desarrollo.

        Args:
            size (tuple): (ancho, alto) de la superficie.
            key (str): Identificador para seleccionar el color del respaldo.

        Returns:
            pygame.Surface: Superficie de respaldo lista para dibujar.
        """
        surface = pygame.Surface(size, pygame.SRCALPHA)

        # Seleccionar color según el tipo de recurso
        color_map = {
            "player1": COLOR_BLUE,
            "player2": COLOR_ORANGE,
            "guard": COLOR_RED,
            "item": COLOR_GREEN,
            "gold": COLOR_GOLD,
        }
        color = next(
            (v for k, v in color_map.items() if k in key.lower()),
            COLOR_GRAY
        )
        surface.fill((*color, 200))  # Semitransparente para indicar que es respaldo

        # Dibujar borde para mayor visibilidad
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 1)

        # Dibujar inicial del key como texto identificativo
        try:
            font = pygame.font.SysFont("arial", max(10, size[1] // 3))
            label = font.render(key[:2].upper(), True, (255, 255, 255))
            rect = label.get_rect(center=(size[0] // 2, size[1] // 2))
            surface.blit(label, rect)
        except Exception:
            pass  # Si la fuente falla, la superficie sigue siendo usable

        return surface

    def get_player_image(self, player_id: int,
                         direction: str = "down",
                         size: tuple = (28, 28)) -> pygame.Surface:
        """
        Retorna la imagen del personaje jugable indicado.

        Args:
            player_id (int): 1 o 2 para identificar el personaje.
            direction (str): Dirección de movimiento ("up","down","left","right").
            size (tuple): Tamaño en píxeles.

        Returns:
            pygame.Surface: Imagen del personaje.
        """
        filename = f"player{player_id}_{direction}.png"
        path = os.path.join(PLAYERS_DIR, filename)
        
        # Si es un frame de animación (ej: down_1) y no existe, usar la imagen base (down)
        if not os.path.exists(path) and "_" in direction:
            parts = direction.split("_")
            if len(parts) > 1 and parts[1].isdigit():
                base_direction = parts[0]
                filename = f"player{player_id}_{base_direction}.png"
                path = os.path.join(PLAYERS_DIR, filename)
                direction = base_direction
                
        key = f"player{player_id}_{direction}"
        return self.get_image(key, path, size)

    def get_guard_image(self, direction: str = "down",
                        size: tuple = (28, 28)) -> pygame.Surface:
        """
        Retorna la imagen del guardia de seguridad.

        Args:
            direction (str): Dirección del guardia.
            size (tuple): Tamaño en píxeles.

        Returns:
            pygame.Surface: Imagen del guardia.
        """
        filename = f"guard_{direction}.png"
        path = os.path.join(GUARDS_DIR, filename)
        key = f"guard_{direction}"
        return self.get_image(key, path, size)

    def get_item_image(self, item_id: str,
                       size: tuple = (20, 20)) -> pygame.Surface:
        """
        Retorna la imagen de un objeto recolectable.

        Args:
            item_id (str): Identificador del objeto (ej. "carpeta").
            size (tuple): Tamaño en píxeles.

        Returns:
            pygame.Surface: Imagen del objeto.
        """
        path = os.path.join(ITEMS_DIR, f"{item_id}.png")
        return self.get_image(f"item_{item_id}", path, size)

    def get_background(self, name: str) -> pygame.Surface:
        """
        Retorna la imagen de fondo para pantallas de UI.

        Args:
            name (str): Nombre del fondo sin extensión.

        Returns:
            pygame.Surface: Imagen de fondo.
        """
        from systems.constants import SCREEN_WIDTH, SCREEN_HEIGHT
        path = os.path.join(BACKGROUNDS_DIR, f"{name}.png")
        return self.get_image(f"bg_{name}", path, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # ──────────────────────────────────────────────
    # SONIDOS
    # ──────────────────────────────────────────────

    def get_sound(self, key: str, filename: str):
        """
        Carga un sonido desde disco o lo retorna desde caché.

        Args:
            key (str): Identificador único para la caché.
            filename (str): Nombre del archivo en la carpeta de sonidos.

        Returns:
            pygame.mixer.Sound | None: Objeto de sonido o None si falla.
        """
        if key in self._sounds:
            return self._sounds[key]

        path = os.path.join(SOUNDS_DIR, filename)
        if os.path.exists(path):
            try:
                sound = pygame.mixer.Sound(path)
                self._sounds[key] = sound
                return sound
            except pygame.error:
                pass  # Si no se puede cargar, retornar None

        self._sounds[key] = None  # Registrar como ausente para no reintentar
        return None

    def play_sound(self, key: str, filename: str,
                   volume: float = 0.7) -> None:
        """
        Carga y reproduce un efecto de sonido.

        Args:
            key (str): Identificador del sonido.
            filename (str): Nombre del archivo de sonido.
            volume (float): Volumen entre 0.0 y 1.0.
        """
        sound = self.get_sound(key, filename)
        if sound:
            sound.set_volume(volume)
            sound.play()

    def play_music(self, filename: str, loops: int = -1,
                   volume: float = 0.4) -> None:
        """
        Inicia la reproducción de música de fondo.

        Args:
            filename (str): Nombre del archivo de música.
            loops (int): Número de repeticiones (-1 = infinito).
            volume (float): Volumen entre 0.0 y 1.0.
        """
        path = os.path.join(SOUNDS_DIR, filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
            except pygame.error:
                pass  # Si el archivo no existe o falla, continuar sin música

    def stop_music(self) -> None:
        """Detiene la música de fondo en reproducción."""
        pygame.mixer.music.stop()

    # ──────────────────────────────────────────────
    # FUENTES
    # ──────────────────────────────────────────────

    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        """
        Retorna una fuente del sistema con el tamaño indicado.

        Args:
            size (int): Tamaño en puntos de la fuente.
            bold (bool): Si True, usa la variante en negrita.

        Returns:
            pygame.font.Font: Objeto fuente listo para renderizar texto.
        """
        key = f"sys_{size}_{'bold' if bold else 'normal'}"
        if key in self._fonts:
            return self._fonts[key]

        font = pygame.font.SysFont("segoeui", size, bold=bold)
        self._fonts[key] = font
        return font


# ──────────────────────────────────────────────────────────────────
# INSTANCIA GLOBAL del gestor de recursos
# Se importa desde otros módulos para acceso centralizado
# ──────────────────────────────────────────────────────────────────
assets = AssetManager()
