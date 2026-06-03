"""
Constantes globales del proyecto Ascenso Corporativo.

Centraliza todos los valores fijos utilizados a lo largo del juego:
dimensiones, colores, rutas de recursos, velocidades y estados.

No se deben modificar estos valores en tiempo de ejecución.
"""

import os

# ──────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PANTALLA
# ──────────────────────────────────────────────────────────────────
SCREEN_WIDTH: int = 960       # Ancho de la ventana en píxeles
SCREEN_HEIGHT: int = 640      # Alto de la ventana en píxeles
FPS: int = 60                 # Fotogramas por segundo objetivo
TITLE: str = "Ascenso Corporativo"  # Título del juego

# ──────────────────────────────────────────────────────────────────
# TAMAÑO DE TILES Y CELDAS
# ──────────────────────────────────────────────────────────────────
TILE_SIZE: int = 32           # Tamaño en píxeles de cada celda del mapa

# ──────────────────────────────────────────────────────────────────
# PALETA DE COLORES (R, G, B)
# ──────────────────────────────────────────────────────────────────
COLOR_BLACK: tuple = (0, 0, 0)
COLOR_WHITE: tuple = (255, 255, 255)
COLOR_GRAY: tuple = (128, 128, 128)
COLOR_DARK_GRAY: tuple = (40, 40, 50)
COLOR_LIGHT_GRAY: tuple = (200, 200, 210)

COLOR_NAVY: tuple = (15, 25, 60)         # Fondo principal del juego
COLOR_NAVY_LIGHT: tuple = (25, 45, 90)   # Fondo secundario / hover
COLOR_GOLD: tuple = (212, 175, 55)       # Acento dorado corporativo
COLOR_GOLD_LIGHT: tuple = (255, 215, 80) # Acento dorado claro

COLOR_GREEN: tuple = (50, 200, 80)       # Éxito / objetos recolectables
COLOR_RED: tuple = (220, 50, 50)         # Peligro / guardias alertados
COLOR_BLUE: tuple = (60, 130, 255)       # Personaje 1 (indicador)
COLOR_ORANGE: tuple = (255, 140, 0)      # Personaje 2 (indicador)
COLOR_YELLOW: tuple = (255, 230, 0)      # Efectos de distracción
COLOR_PURPLE: tuple = (140, 60, 200)     # Elementos especiales

# Colores de tiles del mapa
COLOR_WALL: tuple = (50, 55, 80)         # Paredes del edificio
COLOR_FLOOR: tuple = (80, 85, 100)       # Suelo general
COLOR_FLOOR_ALT: tuple = (90, 95, 110)   # Suelo alternativo (patrón)
COLOR_DOOR: tuple = (140, 90, 40)        # Puertas
COLOR_DOOR_LOCKED: tuple = (160, 50, 50) # Puertas bloqueadas
COLOR_EXIT: tuple = (50, 180, 100)       # Salida / escaleras

# ──────────────────────────────────────────────────────────────────
# ESTADOS DEL JUEGO (máquina de estados)
# ──────────────────────────────────────────────────────────────────
STATE_TITLE: str = "TITLE_SCREEN"
STATE_INSTRUCTIONS: str = "INSTRUCTIONS"
STATE_CREDITS: str = "CREDITS"
STATE_INTRO: str = "INTRO"
STATE_PLAYING: str = "PLAYING"
STATE_PAUSED: str = "PAUSED"
STATE_WIN: str = "WIN"
STATE_GAME_OVER: str = "GAME_OVER"

# ──────────────────────────────────────────────────────────────────
# IDENTIFICADORES DE OBJETOS RECOLECTABLES
# ──────────────────────────────────────────────────────────────────
ITEM_ID: dict = {
    "identificacion": "Identificación Temporal",
    "carpeta": "Carpeta de Documentos",
    "tarjeta": "Tarjeta de Acceso",
    "hoja_vida": "Hoja de Vida Oficial",
    "key_floor_1": "Llave Piso 1",
    "key_floor_2": "Llave Piso 2",
    "key_floor_3": "Llave Piso 3",
    "key_floor_4": "Llave Piso 4",
    "key_floor_5": "Llave Dirección",
    "moneda": "Moneda",
    "lata": "Lata",
    "papel": "Papel",
}

# Objetos requeridos para ganar el juego
REQUIRED_ITEMS: list = ["identificacion", "carpeta", "tarjeta", "hoja_vida"]

# Objetos que pueden usarse como distracción
DISTRACTION_ITEMS: list = ["moneda", "lata", "papel"]

# Llaves de acceso usadas para bloquear rutas de progresión
ACCESS_KEYS: dict = {
    1: "key_floor_1",
    2: "key_floor_2",
    3: "key_floor_3",
    4: "key_floor_4",
    5: "key_floor_5",
}

# ──────────────────────────────────────────────────────────────────
# PARÁMETROS DE JUGADORES
# ──────────────────────────────────────────────────────────────────
PLAYER_SPEED: float = 120.0    # Píxeles por segundo
PLAYER_SIZE: int = 28          # Tamaño del sprite del jugador
PLAYER_COLLISION_WIDTH: int = 18
PLAYER_COLLISION_HEIGHT: int = 20
PLAYER_INTERACT_RANGE: int = 40  # Distancia de interacción en píxeles
PLAYER_THROW_RANGE: int = 200    # Rango de lanzamiento de objetos

# ──────────────────────────────────────────────────────────────────
# PARÁMETROS DE GUARDIAS
# ──────────────────────────────────────────────────────────────────
GUARD_SPEED: float = 70.0          # Píxeles por segundo
GUARD_SIZE: int = 28               # Tamaño del sprite del guardia
GUARD_COLLISION_WIDTH: int = 18
GUARD_COLLISION_HEIGHT: int = 20
GUARD_DETECTION_RANGE: int = 130    # Radio de detección del jugador (px)
GUARD_VIEW_ANGLE: float = 110.0    # Grados del cono frontal de visión
GUARD_CHASE_SPEED: float = 92.0
GUARD_SEARCH_TIME: float = 4.0
GUARD_LOST_SIGHT_TIME: float = 1.1
GUARD_SOUND_RANGE: int = 160       # Radio de escucha de distracciones (px)
GUARD_PATROL_WAIT: float = 1.5     # Segundos de espera en cada punto de patrulla
GUARD_INVESTIGATE_TIME: float = 3.0  # Segundos investigando el sonido
MAX_DETECTIONS: int = 3            # Máximo de detecciones antes de game over

# ──────────────────────────────────────────────────────────────────
# RUTAS DE RECURSOS (relativas a la raíz del proyecto)
# ──────────────────────────────────────────────────────────────────
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR: str = os.path.join(BASE_DIR, "assets")
FONTS_DIR: str = os.path.join(ASSETS_DIR, "fonts")
SOUNDS_DIR: str = os.path.join(ASSETS_DIR, "sonidos")
PLAYERS_DIR: str = os.path.join(ASSETS_DIR, "personajes")
GUARDS_DIR: str = os.path.join(ASSETS_DIR, "guardias")
ITEMS_DIR: str = os.path.join(ASSETS_DIR, "objetos")
BACKGROUNDS_DIR: str = os.path.join(ASSETS_DIR, "fondos")

# ──────────────────────────────────────────────────────────────────
# INFORMACIÓN DE LOS CRÉDITOS
# (Personalizar con los datos reales del equipo)
# ──────────────────────────────────────────────────────────────────
CREDITS_INFO: dict = {
    "juego": "Ascenso Corporativo",
    "integrantes": ["Estudiante 1 - Santiago Cardona", "Estudiante 2 - Maria Jose Herrera"],
    "materia": "Computación Gráfica",
    "profesor": "Francisco Medina",
    "anio": "2025",
}

# ──────────────────────────────────────────────────────────────────
# TEXTO DE INTRODUCCIÓN NARRATIVA
# ──────────────────────────────────────────────────────────────────
INTRO_TEXT: list = [
    "Después de enviar múltiples hojas de vida sin éxito,",
    "dos estudiantes descubren una oportunidad laboral",
    "en una importante empresa.",
    "",
    "Sin embargo, para llegar a la entrevista deberán",
    "atravesar varios pisos del edificio, reunir",
    "documentación y demostrar su ingenio.",
    "",
    "Presiona ENTER para comenzar...",
]
