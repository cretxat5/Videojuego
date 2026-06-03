"""
Módulo state_manager.py — Máquina de estados del juego.

Implementa el patrón de diseño State Machine (Máquina de estados finitos).
Controla qué pantalla o lógica está activa en cada momento del juego.

Estados disponibles:
    TITLE_SCREEN → INSTRUCTIONS, CREDITS, INTRO, salir
    INSTRUCTIONS → TITLE_SCREEN
    CREDITS      → TITLE_SCREEN
    INTRO        → PLAYING
    PLAYING      → PAUSED, WIN, GAME_OVER
    PAUSED       → PLAYING, TITLE_SCREEN, salir
    WIN          → TITLE_SCREEN
    GAME_OVER    → PLAYING (reintentar), TITLE_SCREEN
"""

import pygame
import time
from systems.constants import (
    STATE_TITLE, STATE_INSTRUCTIONS, STATE_CREDITS,
    STATE_INTRO, STATE_PLAYING, STATE_PAUSED,
    STATE_WIN, STATE_GAME_OVER,
)
from systems.inventory import Inventory


class GameData:
    """
    Contenedor de datos compartidos entre todos los estados del juego.

    Esta clase actúa como "memoria global" del juego, almacenando
    información que necesita persistir entre transiciones de estado.

    Attributes:
        inventory (Inventory): Inventario compartido de ambos jugadores.
        current_floor (int): Piso actual (1-5).
        detection_count (int): Número de veces que los guardias detectaron al jugador.
        start_time (float): Tiempo de inicio de la partida.
        floors_completed (int): Pisos completados.
    """

    def __init__(self) -> None:
        """Inicializa los datos del juego con valores predeterminados."""
        self.inventory: Inventory = Inventory()
        self.current_floor: int = 1
        self.detection_count: int = 0
        self.start_time: float = time.time()
        self.floors_completed: int = 0

    def reset(self) -> None:
        """Reinicia todos los datos para una nueva partida."""
        self.inventory = Inventory()
        self.current_floor = 1
        self.detection_count = 0
        self.start_time = time.time()
        self.floors_completed = 0

    @property
    def elapsed_time(self) -> float:
        """Retorna el tiempo transcurrido desde el inicio de la partida."""
        return time.time() - self.start_time


class StateManager:
    """
    Gestor central de estados del juego.

    Implementa el patrón Finite State Machine (FSM).
    Mantiene el estado activo y delega las operaciones
    update/draw/handle_event al estado correspondiente.

    Attributes:
        screen (pygame.Surface): Superficie principal de renderizado.
        game_data (GameData): Datos compartidos del juego.
        current_state (str): Identificador del estado activo.
        _states (dict): Mapa de identificador → objeto de estado.
        should_quit (bool): Señal para cerrar el juego.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Inicializa el gestor y carga todos los estados del juego.

        Args:
            screen (pygame.Surface): Superficie principal de renderizado.
        """
        self.screen: pygame.Surface = screen
        self.game_data: GameData = GameData()
        self.current_state: str = STATE_TITLE
        self.should_quit: bool = False

        # Importaciones aquí para evitar dependencias circulares
        from ui.title_screen import TitleScreen
        from ui.instructions_screen import InstructionsScreen
        from ui.credits_screen import CreditsScreen
        from ui.intro_screen import IntroScreen
        from ui.pause_menu import PauseMenu
        from ui.win_screen import WinScreen
        from ui.game_over_screen import GameOverScreen
        from levels.level_manager import LevelManager

        # Diccionario de estados: clave → instancia
        self._states: dict = {
            STATE_TITLE: TitleScreen(screen, self),
            STATE_INSTRUCTIONS: InstructionsScreen(screen, self),
            STATE_CREDITS: CreditsScreen(screen, self),
            STATE_INTRO: IntroScreen(screen, self),
            STATE_PAUSED: PauseMenu(screen, self),
            STATE_WIN: WinScreen(screen, self),
            STATE_GAME_OVER: GameOverScreen(screen, self),
        }

        # El nivel manager se crea aparte porque necesita reiniciarse
        self._level_manager: LevelManager = LevelManager(screen, self)
        self._states[STATE_PLAYING] = self._level_manager

    def change_state(self, new_state: str) -> None:
        """
        Cambia el estado activo del juego.

        Se llama desde cualquier estado para realizar transiciones.
        Maneja lógica especial para iniciar/reiniciar partidas.

        Args:
            new_state (str): Identificador del nuevo estado.
        """
        # Lógica especial al iniciar nueva partida
        if new_state == STATE_INTRO:
            self.game_data.reset()

        # Reiniciar nivel al comenzar a jugar
        if new_state == STATE_PLAYING:
            self._level_manager.load_floor(self.game_data.current_floor)

        self.current_state = new_state

    def quit_game(self) -> None:
        """Señala al bucle principal que debe terminar el programa."""
        self.should_quit = True

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Delega el manejo de eventos al estado activo.

        Args:
            event (pygame.event.Event): Evento de Pygame a procesar.
        """
        state = self._states.get(self.current_state)
        if state:
            state.handle_event(event)

    def update(self, delta_time: float) -> None:
        """
        Actualiza la lógica del estado activo.

        Args:
            delta_time (float): Tiempo transcurrido desde el último frame (segundos).
        """
        state = self._states.get(self.current_state)
        if state:
            state.update(delta_time)

    def draw(self) -> None:
        """Dibuja el estado activo en la superficie de pantalla."""
        state = self._states.get(self.current_state)
        if state:
            state.draw()
