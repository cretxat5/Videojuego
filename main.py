"""
Ascenso Corporativo - Punto de entrada principal del juego.

Este módulo inicializa Pygame, crea la ventana principal y lanza
el bucle de control de estados del juego.

Autor: Proyecto Universitario - Computación Gráfica
Versión: 1.0.0
"""

import sys
import pygame
from systems.state_manager import StateManager
from systems.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE


def main() -> None:
    """
    Función principal que inicializa y ejecuta el juego.

    Realiza la inicialización de Pygame, configura la ventana,
    instancia el StateManager y ejecuta el bucle principal.
    """
    # Inicializar todos los módulos de Pygame
    pygame.init()
    pygame.mixer.init()  # Inicializar el sistema de audio

    # Crear la ventana principal con las dimensiones definidas en constants.py
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)  # Título de la ventana del sistema operativo

    # Reloj para controlar los fotogramas por segundo (FPS)
    clock: pygame.time.Clock = pygame.time.Clock()

    # Instanciar el gestor de estados, que controla todas las pantallas
    state_manager: StateManager = StateManager(screen)

    # ──────────────────────────────────────────────
    # BUCLE PRINCIPAL DEL JUEGO
    # ──────────────────────────────────────────────
    running: bool = True
    while running:
        # Delta time: tiempo transcurrido desde el último fotograma (en segundos)
        # Se utiliza para movimientos independientes de la velocidad de FPS
        delta_time: float = clock.tick(FPS) / 1000.0

        # Procesar eventos del sistema operativo (cierre de ventana, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Delegar el manejo de eventos al estado activo
                state_manager.handle_event(event)

        # Verificar si el gestor de estados solicita terminar el programa
        if state_manager.should_quit:
            running = False

        # Actualizar la lógica del estado activo
        state_manager.update(delta_time)

        # Dibujar el estado activo en pantalla
        state_manager.draw()

        # Actualizar la pantalla completa (doble buffer)
        pygame.display.flip()

    # Liberar recursos de Pygame y salir limpiamente
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
