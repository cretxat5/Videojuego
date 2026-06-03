# DOCUMENTACIÓN TÉCNICA — ASCENSO CORPORATIVO

> Computación Gráfica | Proyecto Final  
> Desarrollado con Python 3 + Pygame

---

## 1. Descripción General

### Nombre del Proyecto
**Ascenso Corporativo**

### Objetivo del Juego
Dos estudiantes deben recorrer cinco pisos de un edificio corporativo, recolectar cuatro documentos clave, evitar ser detectados por guardias de seguridad y llegar a la oficina del Director General para conseguir empleo.

### Historia
Después de enviar múltiples hojas de vida sin éxito, dos estudiantes descubren una oportunidad laboral en una importante empresa. Sin embargo, para llegar a la entrevista deben atravesar varios pisos del edificio, reunir documentación y demostrar su ingenio.

### Mecánicas Principales

| Mecánica | Descripción |
|----------|-------------|
| Movimiento | WASD en 4 direcciones con colisiones |
| Cambio de personaje | TAB alterna entre P1 y P2 |
| Recolección | Tocar objetos los agrega al inventario |
| Interacción | E abre puertas y activa mecanismos |
| Distracción | Q lanza objetos que atraen a los guardias |
| Sigilo | Evitar el radio de detección de guardias |

### Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje principal
- **Pygame 2.x**: Motor gráfico 2D, entrada, audio y colisiones
- **Módulo `abc`**: Clases abstractas para herencia
- **Módulo `math`**: Cálculos trigonométricos (distancias, animaciones)
- **Módulo `os`**: Manejo de rutas de archivos
- **Módulo `time`**: Medición del tiempo de juego

---

## 2. Arquitectura del Proyecto

### Flujo General del Programa

```
main.py
   │
   └─► pygame.init() + pygame.display.set_mode()
          │
          └─► StateManager(screen)
                 │
                 ├─► TitleScreen
                 ├─► InstructionsScreen
                 ├─► CreditsScreen
                 ├─► IntroScreen
                 ├─► PauseMenu
                 ├─► WinScreen
                 ├─► GameOverScreen
                 └─► LevelManager
                        │
                        ├─► Floor1 (BaseLevel)
                        ├─► Floor2 (BaseLevel)
                        ├─► Floor3 (BaseLevel)
                        ├─► Floor4 (BaseLevel)
                        └─► Floor5 (BaseLevel)
                               │
                               ├─► Player (Sprite)
                               ├─► Guard  (Sprite)
                               ├─► Item   (Sprite)
                               └─► Door
```

### Organización de Carpetas

```
ascenso_corporativo/
├── main.py            ← Punto de entrada, bucle principal
├── systems/           ← Núcleo: estados, inventario, colisiones
├── entities/          ← Entidades: jugadores, guardias, objetos
├── levels/            ← Mapas y lógica de cada piso
├── ui/                ← Pantallas de menú e interfaz
└── assets/            ← Recursos: imágenes, sonidos
```

### Relación Entre Módulos

```
main.py
  usa → StateManager
           usa → todas las pantallas UI
           usa → LevelManager
                    usa → Floor1..Floor5 (hereda BaseLevel)
                               usa → Player, Guard, Item
                               usa → Inventory, CollisionSystem

AssetManager  ← usado por TODOS los módulos (instancia global)
constants.py  ← importado por TODOS los módulos
```

---

## 3. Explicación de Cada Archivo

### `main.py`
- **Responsabilidad**: Punto de entrada. Inicializa Pygame, crea la ventana, instancia el StateManager y ejecuta el bucle principal.
- **Funciones**: `main()` — contiene el game loop completo.
- **Interacción**: Importa StateManager y constants.

---

### `systems/constants.py`
- **Responsabilidad**: Centraliza todos los valores constantes del juego.
- **Contenido**: Dimensiones de pantalla, colores, velocidades, estados, rutas de assets, textos.
- **Interacción**: Importado por todos los módulos.

---

### `systems/asset_manager.py`
**Clase: `AssetManager`**
- **Responsabilidad**: Cargar y cachear todos los recursos multimedia (imágenes, sonidos, fuentes). Genera recursos de respaldo si los archivos no existen.
- **Atributos**: `_images`, `_sounds`, `_fonts` (diccionarios de caché).
- **Métodos importantes**:
  - `get_image(key, path, size)` → carga o retorna imagen cacheada
  - `_create_fallback_surface(size, key)` → genera sprite de respaldo
  - `get_player_image(player_id, direction, size)` → sprite de jugador
  - `get_guard_image(direction, size)` → sprite de guardia
  - `play_sound(key, filename, volume)` → reproduce efecto
  - `play_music(filename, loops, volume)` → inicia música de fondo
- **Instancia global**: `assets = AssetManager()` — importada desde cualquier módulo.

---

### `systems/state_manager.py`
**Clases: `GameData`, `StateManager`**

**`GameData`**:
- Contenedor de datos persistentes entre estados (inventario, piso actual, detecciones, tiempo).
- Método `reset()` reinicia para nueva partida.

**`StateManager`**:
- **Responsabilidad**: Implementar la máquina de estados del juego.
- **Atributos**: `current_state`, `_states` (diccionario), `game_data`, `should_quit`.
- **Métodos importantes**:
  - `change_state(new_state)` → transición entre estados
  - `handle_event(event)` → delega al estado activo
  - `update(delta_time)` → delega al estado activo
  - `draw()` → delega al estado activo

---

### `systems/inventory.py`
**Clase: `Inventory`**
- **Responsabilidad**: Gestionar objetos recolectados y verificar condiciones de victoria.
- **Atributos**: `_items` (dict), `_current_objective`, `_total_collected`.
- **Métodos importantes**:
  - `add_item(item_id)` → agrega objeto
  - `remove_item(item_id)` → consume objeto (distracciones)
  - `has_item(item_id)` → verifica presencia
  - `has_all_required()` → condición de victoria
  - `get_distraction_item()` → obtiene objeto para lanzar
  - `draw(screen, x, y)` → dibuja panel HUD del inventario

---

### `systems/collision.py`
**Clase: `CollisionSystem`** (métodos estáticos)
- **Responsabilidad**: Centralizar detección de colisiones con el método AABB.
- **Métodos**:
  - `check_wall_collision(rect, walls, dx, dy)` → movimiento con deslizamiento
  - `check_guard_detection(player_rect, guard_rect, range)` → detección circular
  - `check_sound_detection(pos, guard_rect, range)` → radio de sonido
  - `get_interaction_targets(player_rect, interactables, range)` → objetos cercanos

---

### `entities/player.py`
**Clase: `Player` (hereda `pygame.sprite.Sprite`)**
- **Responsabilidad**: Movimiento, animación y representación visual del jugador.
- **Atributos**: `player_id`, `rect`, `speed`, `direction`, `is_active`, `_float_x/_float_y`.
- **Métodos**:
  - `move(dx, dy, wall_rects, delta_time)` → movimiento con colisión
  - `update_animation(delta_time)` → ciclo de animación
  - `set_position(x, y)` → teleportación
  - `draw(screen, camera_offset)` → dibuja sprite + indicadores

---

### `entities/guard.py`
**Clase: `Guard` (hereda `pygame.sprite.Sprite`)**
- **Responsabilidad**: IA de patrullaje e investigación de sonidos.
- **Estados internos**: `PATROL`, `WAIT`, `INVESTIGATE`, `RETURN`, `ALERT`.
- **Métodos**:
  - `update(delta_time, walls, player_rects)` → actualiza FSM
  - `investigate_sound(pos)` → activa investigación de sonido
  - `_update_patrol(dt, walls)` → lógica de patrullaje
  - `_check_detection(player_rects)` → detección de jugadores
  - `draw(screen, camera_offset)` → sprite + indicadores de estado

---

### `entities/item.py`
**Clases: `Item`, `DistractionProjectile`**

**`Item`**:
- Objeto recolectable con animación de flotación (bob) y halo visual.
- `update(delta_time)` → actualiza posición con función seno.
- `draw(screen, camera_offset)` → dibuja con glow.

**`DistractionProjectile`**:
- Proyectil visual del objeto lanzado.
- `update(delta_time)` → mueve hacia destino, genera rastro.
- Al aterrizar: notifica a guardias cercanos via `guard.investigate_sound()`.

---

### `levels/base_level.py`
**Clases: `Door`, `BaseLevel` (abstracta)**

**`Door`**:
- Puerta con estado abierto/bloqueado y requisito de item.
- `try_open(inventory)` → abre si el inventario cumple el requisito.

**`BaseLevel`**:
- **Responsabilidad**: Clase base con toda la lógica compartida de los niveles.
- **Métodos abstractos**: `_build_map()`, `_place_entities()`, `_get_objective()`.
- **Métodos importantes**:
  - `update(delta_time)` → actualiza jugadores, guardias, items, proyectiles
  - `draw()` → renderiza mapa, entidades y HUD en capas
  - `_draw_tiles(cx, cy)` → tile rendering con frustum culling
  - `_update_camera()` → seguimiento suave con lerp
  - `handle_interact()` → lógica de interacción con E
  - `handle_throw()` → lanzamiento de distracción con Q
  - `handle_switch_player()` → alternancia de personajes con TAB
  - `show_notification(text, color, duration)` → mensajes temporales

---

### `levels/floor1.py` … `floor5.py`
Cada archivo implementa un piso concreto heredando de `BaseLevel`:
- Sobrescribe `_build_map()` con la matriz de tiles del piso.
- Sobrescribe `_place_entities()` con posiciones de jugadores, guardias y objetos.
- Sobrescribe `_on_exit_reached()` para verificar requisitos del piso.

---

### `levels/level_manager.py`
**Clase: `LevelManager`**
- **Responsabilidad**: Cargar el piso correcto y gestionar transiciones visuales (fade).
- `load_floor(floor_number)` → instancia el Floor correspondiente.
- `update(delta_time)` → detecta `current_level.completed` y carga el siguiente.
- `draw()` → dibuja nivel + overlay de transición con nombre del piso.

---

### Pantallas UI (`ui/`)

| Archivo | Clase | Función |
|---------|-------|---------|
| `base_screen.py` | `BaseScreen` | Clase base con utilidades de dibujado |
| `title_screen.py` | `TitleScreen` | Menú principal, fotos de estudiantes |
| `instructions_screen.py` | `InstructionsScreen` | Controles y objetivos |
| `credits_screen.py` | `CreditsScreen` | Información académica |
| `intro_screen.py` | `IntroScreen` | Narrativa con efecto typewriter |
| `pause_menu.py` | `PauseMenu` | Pausa superpuesta con overlay |
| `win_screen.py` | `WinScreen` | Victoria con estadísticas y confeti |
| `game_over_screen.py` | `GameOverScreen` | Derrota con efecto CRT |

---

## 4. Programación Orientada a Objetos

### Encapsulamiento
- Atributos privados con prefijo `_` (ej: `_float_x`, `_anim_timer`, `_items`).
- Acceso externo solo mediante propiedades (`@property`) y métodos públicos.
- **Justificación**: Protege el estado interno de modificaciones accidentales.

### Herencia
```
pygame.sprite.Sprite
    ├── Player
    ├── Guard
    └── Item

BaseScreen (ABC)
    ├── TitleScreen
    ├── InstructionsScreen
    ├── CreditsScreen
    ├── IntroScreen
    ├── PauseMenu
    ├── WinScreen
    └── GameOverScreen

BaseLevel (ABC)
    ├── Floor1
    ├── Floor2
    ├── Floor3
    ├── Floor4
    └── Floor5
```
**Justificación**: Evita código duplicado. El comportamiento común se define una vez en la clase base.

### Polimorfismo
- Todos los estados implementan `handle_event()`, `update()`, `draw()` con firmas idénticas.
- `StateManager` llama a estos métodos sin saber qué estado concreto está activo.
- **Justificación**: Permite agregar nuevos estados sin modificar el `StateManager`.

### Composición
- `BaseLevel` **tiene** una lista de `Player`, `Guard`, `Item` (no hereda de ellos).
- `StateManager` **tiene** un `GameData` y un `LevelManager`.
- `GameData` **tiene** un `Inventory`.
- **Justificación**: Relación "tiene un" en lugar de "es un", favorece flexibilidad.

### Clases Abstractas
- `BaseLevel` y `BaseScreen` usan `ABC` y `@abstractmethod` para forzar la implementación de métodos obligatorios en subclases.

---

## 5. Gestión de Estados del Juego

### Diagrama de Transiciones

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
             ┌──────▼──────┐                                  │
         ┌──►│ TITLE_SCREEN│◄──────────────────────┐         │
         │   └──────┬──────┘                       │         │
         │          │                              │         │
    ┌────┘    ┌─────┼──────┐                      │         │
    │    ┌────▼──┐ ┌▼──────┴──┐ ┌──────────┐      │         │
    │    │INSTRU-│ │ CREDITS  │ │   INTRO  │      │         │
    │    │CTIONS │ └──────────┘ └────┬─────┘      │         │
    │    └───────┘                   │             │         │
    │                          ┌─────▼──────┐     │         │
    │                          │  PLAYING   │     │         │
    │                          └─────┬──────┘     │         │
    │                      ┌─────────┼──────────┐ │         │
    │                   ┌──▼──┐   ┌──▼───┐    ┌─▼─▼──┐     │
    │                   │PAUS-│   │ WIN  │    │GAME_ │     │
    │                   │ ED  │   └──────┘    │ OVER │     │
    │                   └─────┘               └──────┘     │
    │                                                       │
    └───────────────────────────────────────────────────────┘
```

### Eventos que Provocan Transiciones

| De → A | Evento |
|--------|--------|
| TITLE → INTRO | ENTER en "Iniciar Partida" |
| TITLE → INSTRUCTIONS | ENTER en "Instrucciones" |
| TITLE → CREDITS | ENTER en "Créditos" |
| INTRO → PLAYING | ENTER cuando texto completo |
| PLAYING → PAUSED | Tecla ESC |
| PAUSED → PLAYING | "Continuar" o ESC |
| PAUSED → TITLE | "Menú Principal" |
| PLAYING → WIN | Llegar a salida del Piso 5 con todos los documentos |
| PLAYING → GAME_OVER | `detection_count >= MAX_DETECTIONS` |
| WIN → TITLE | ENTER |
| GAME_OVER → PLAYING | "Reintentar" |
| GAME_OVER → TITLE | "Volver al Menú" |

---

## 6. Sistema de Inventario

### Estructura de Datos

```python
_items: dict = {
    "identificacion": 0,  # Objeto principal Piso 1
    "carpeta":        0,  # Objeto principal Piso 2
    "tarjeta":        0,  # Objeto principal Piso 3
    "hoja_vida":      0,  # Objeto principal Piso 4
    "moneda":         0,  # Distracción
    "lata":           0,  # Distracción
    "papel":          0,  # Distracción
}
```

### Verificación de Victoria

```python
REQUIRED_ITEMS = ["identificacion", "carpeta", "tarjeta", "hoja_vida"]

def has_all_required(self) -> bool:
    return all(self._items.get(item_id, 0) > 0 for item_id in REQUIRED_ITEMS)
```

### Uso de Distracciones

```
Jugador presiona Q
    ↓
inventory.get_distraction_item() → retorna primer disponible
    ↓
Crear DistractionProjectile(start, end, item_id)
    ↓
inventory.remove_item(item_id) → decrementa contador
    ↓
Proyectil llega al destino → guard.investigate_sound(pos)
```

---

## 7. Sistema de Guardias

### FSM del Guardia

```
Estado: PATROL
  - Sigue ruta de puntos
  - Al llegar a un punto → WAIT (timer: 1.5 s)
  - Detecta jugador → ALERT (timer: 1.5 s)

Estado: WAIT
  - Permanece quieto el tiempo del timer
  - Al terminar → avanza al siguiente punto → PATROL
  - Detecta jugador → ALERT

Estado: INVESTIGATE
  - Se mueve hacia la posición del sonido
  - Al llegar → espera INVESTIGATE_TIME (3.0 s)
  - Al terminar → RETURN

Estado: RETURN
  - Regresa al último punto de patrulla
  - Al llegar → PATROL

Estado: ALERT
  - Indica detección visual (símbolo !)
  - Suma detection_count en GameData
  - Al terminar timer → PATROL
```

### Detección por Distancia

```python
# Comparación de distancias sin raíz cuadrada (optimización)
dist_sq = (px - gx)**2 + (py - gy)**2
if dist_sq <= detection_range**2:
    # Jugador detectado
```

### Respuesta a Sonido

```python
# En DistractionProjectile.update():
if proj.landed:
    for guard in self.guards:
        if CollisionSystem.check_sound_detection(
                end_pos, guard.rect, guard.sound_range):
            guard.investigate_sound(end_pos)
```

---

## 8. Sistema de Colisiones

### Método AABB (Axis-Aligned Bounding Box)

Todos los objetos usan `pygame.Rect` como bounding box.

```
┌───────────────┐
│    Rect A     │   Si A y B se superponen en X e Y → colisión
└───────────────┘
        ┌───────────────┐
        │    Rect B     │
        └───────────────┘
```

Pygame provee `rect_a.colliderect(rect_b)` para verificación eficiente.

### Colisión con Paredes (Deslizamiento)

```
Movimiento deseado: dx, dy

1. Probar posición = rect.x + dx
   Si colisión → dx = 0

2. Probar posición = rect.y + dy
   Si colisión → dy = 0

Resultado: permite deslizarse a lo largo de paredes
```

Este algoritmo permite que el jugador se mueva en diagonal a lo largo de una pared sin quedarse atascado.

### Culling de Tiles

El método `_draw_tiles()` calcula el rango de tiles visibles:

```python
start_col = cx // TILE_SIZE        # Primer tile visible X
end_col = (cx + SCREEN_WIDTH) // TILE_SIZE + 2  # Último tile X
```

Solo se dibujan los tiles dentro del viewport, optimizando el rendimiento.

---

## 9. Sistema de Renderizado

### Capas de Renderizado

El orden de dibujado en `BaseLevel.draw()` sigue estas capas:

```
Capa 1 (fondo): Tiles del mapa
Capa 2:         Puertas
Capa 3:         Items recolectables
Capa 4:         Jugadores inactivos
Capa 5:         Jugador activo (encima)
Capa 6:         Guardias
Capa 7:         Proyectiles
Capa 8 (HUD):   Inventario, notificaciones, controles
```

### Sprites y Superficies

Cada entidad es un `pygame.Surface` (imagen 2D en memoria RAM de la GPU).

```
pygame.Surface → almacena píxeles en memoria
pygame.Rect    → posición y dimensiones (no almacena píxeles)

screen.blit(surface, rect.topleft) → copia superficie en pantalla
```

### Cámara con Lerp (Interpolación Lineal)

```python
# Seguimiento suave de cámara
target_x = player.rect.centerx - SCREEN_WIDTH // 2
self._camera_x += (target_x - self._camera_x) * 0.15
```

El factor `0.15` controla la suavidad: 1.0 = inmediato, 0.0 = sin movimiento.

### Superficies Semitransparentes

```python
# Crear superficie con canal alfa
surf = pygame.Surface((w, h), pygame.SRCALPHA)
surf.fill((r, g, b, alpha))  # alpha: 0=transparente, 255=opaco
screen.blit(surf, (x, y))
```

### Relación con Computación Gráfica

| Concepto CG | Implementación en el proyecto |
|-------------|-------------------------------|
| Sprites | `pygame.Surface` + `pygame.Rect` |
| Transformaciones 2D | `pygame.transform.scale()`, `rotate()` |
| Gestión de escenas | `StateManager` + patrón State Machine |
| Colisiones | AABB con `pygame.Rect.colliderect()` |
| Animación de cuadros | Walk cycle basado en temporizador |
| Culling | Solo renderizar tiles visibles en viewport |
| Interpolación | Lerp para suavizado de cámara |
| Canal alfa | `pygame.SRCALPHA` para transparencias |
| Gradientes | Interpolación de color línea a línea |
| Doble buffer | `pygame.display.flip()` |

---

## 10. Eventos y Entrada de Usuario

### Tipos de Eventos

```python
pygame.QUIT           → Cierre de ventana
pygame.KEYDOWN        → Tecla presionada (un disparo)
pygame.key.get_pressed() → Estado continuo de teclas (movimiento)
```

### Movimiento Continuo vs Eventos Discretos

| Acción | Mecanismo |
|--------|-----------|
| Movimiento WASD | `get_pressed()` en cada frame |
| TAB, E, Q, ESC | `KEYDOWN` evento único |
| Navegación de menú | `KEYDOWN` evento único |

### Delegación de Eventos

```
pygame.event.get()  → lista de eventos del frame
    ↓
StateManager.handle_event(event)
    ↓
estado_actual.handle_event(event)  ← polimorfismo
```

---

## 11. Recursos Multimedia

### Estructura de Carpetas

```
assets/
├── personajes/    ← player1_down.png, player2_down.png, ...
├── guardias/      ← guard_down.png, guard_up.png, ...
├── objetos/       ← identificacion.png, carpeta.png, ...
├── fondos/        ← title_bg.png (opcional)
└── sonidos/       ← menu_music.ogg, recoger.wav, ...
```

### Archivos de Sonido Requeridos

| Archivo | Momento de uso |
|---------|----------------|
| `menu_music.ogg` | Música de fondo del menú |
| `recoger.wav` | Al recoger un objeto |
| `lanzar.wav` | Al lanzar una distracción |
| `cambiar.wav` | Al cambiar de personaje |
| `puerta.wav` | Al abrir una puerta |
| `detectado.wav` | Al ser detectado por un guardia |
| `subir_piso.wav` | Al pasar al siguiente piso |
| `victoria.wav` | Al ganar el juego |

**Nota**: Si algún archivo no existe, el juego continúa sin ese sonido gracias al manejo de errores en `AssetManager`.

---

## 12. Dependencias

### Requerimientos

```
pygame >= 2.1.0
Python >= 3.10
```

### Instalación

```bash
pip install pygame
```

### Verificar instalación

```bash
python -c "import pygame; print(pygame.__version__)"
```

---

## 13. Guía de Ejecución

### Paso 1: Clonar o descargar el proyecto

```bash
cd ascenso_corporativo
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Pygame

```bash
pip install pygame
```

### Paso 4: (Opcional) Agregar sprites y sonidos

Leer los archivos `LEER.txt` en cada carpeta de `assets/` para saber qué archivos colocar.

### Paso 5: Ejecutar

```bash
python main.py
```

---

## 14. Posibles Mejoras Futuras

| Mejora | Descripción técnica |
|--------|---------------------|
| Más niveles | Agregar Floor6..Floor10 heredando BaseLevel |
| IA avanzada | Implementar A* pathfinding para los guardias |
| Sistema de guardado | Serializar `GameData` con `pickle` o JSON |
| Animaciones avanzadas | Spritesheets con múltiples frames |
| Efectos de luz | Máscaras de visibilidad (line-of-sight) |
| Minijuegos | Puzzles en pisos específicos (subclases especiales) |
| Multijugador local | Dos teclados simultáneos |
| Resoluciones variables | Escalar con `pygame.transform.scale()` |
| Tiempo de récord | Guardar y mostrar mejores tiempos |
| Más tipos de guardias | Subclases de Guard con comportamientos distintos |

---

## 15. Relación con Computación Gráfica

Este proyecto cubre los siguientes temas de la asignatura:

### 1. Renderizado 2D
Uso de `pygame.Surface.blit()` para componer escenas mediante capas de superficies. Equivalente conceptual a composición de texturas en OpenGL.

### 2. Transformaciones
`pygame.transform.scale()` y `rotate()` aplican transformaciones afines a las superficies (escala, rotación), conceptos fundamentales en matrices de transformación 2D.

### 3. Gestión de Escenas
El `StateManager` implementa el patrón de gestión de escenas: cada estado es una "escena" independiente con su propia lógica de actualización y renderizado.

### 4. Animación por Cuadros
Los personajes alternan entre frames de sprite según un temporizador, implementando el concepto de animación discreta (flip-book animation).

### 5. Colisiones AABB
El método Axis-Aligned Bounding Box es el algoritmo de colisión 2D más fundamental. El proyecto lo implementa manualmente y también mediante `pygame.Rect.colliderect()`.

### 6. Sprites y Texturas
Cada entidad visual es una `pygame.Surface` (equivalente a una textura en gráficos 3D), con su transformación y posición gestionadas por `pygame.Rect`.

### 7. Doble Buffer
`pygame.display.flip()` implementa el concepto de doble buffer: la escena se dibuja en un buffer oculto y luego se muestra completa, evitando el parpadeo (flickering).

### 8. Interpolación
La cámara usa interpolación lineal (lerp) para un seguimiento suave, técnica ampliamente usada en animación y simulación gráfica.

### 9. Canal Alfa
Uso de `pygame.SRCALPHA` para transparencias por píxel, equivalente al canal alfa en composición de imágenes.

### 10. Frustum Culling
El método `_draw_tiles()` solo renderiza los tiles dentro del viewport, implementando el concepto básico de frustum culling para optimización de renderizado.

---

## 16. Informe Académico

Ver archivo `INFORME_ACADEMICO.md` para el informe completo listo para entrega.
