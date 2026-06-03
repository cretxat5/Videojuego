# INFORME ACADÉMICO
## Proyecto Final: Ascenso Corporativo
### Asignatura: Computación Gráfica

---

| Campo | Detalle |
|-------|---------|
| **Nombre del Proyecto** | Ascenso Corporativo |
| **Asignatura** | Computación Gráfica |
| **Integrantes** | Estudiante 1 — Tu Nombre / Estudiante 2 — Tu Nombre |
| **Profesor** | Nombre del Profesor |
| **Período** | 2025 |

---

## 1. Introducción

El presente informe documenta el desarrollo del videojuego **Ascenso Corporativo**, proyecto final de la asignatura de Computación Gráfica. El proyecto consiste en un videojuego 2D de vista superior (*top-down*) desarrollado íntegramente en Python 3 utilizando la biblioteca Pygame, orientado a demostrar de forma práctica los conceptos fundamentales del renderizado 2D, gestión de escenas, animación por cuadros, sistemas de colisión y composición visual.

La elección de un videojuego como proyecto permite abordar de manera integrada y aplicada la gran mayoría de los temas teóricos vistos en clase, ya que un juego 2D exige la implementación simultánea de renderizado, transformaciones, eventos de entrada, animación y gestión de recursos gráficos.

---

## 2. Objetivos

### 2.1 Objetivo General

Diseñar e implementar un videojuego 2D funcional utilizando Python 3 y Pygame, aplicando los principios de computación gráfica estudiados durante el curso y siguiendo buenas prácticas de ingeniería de software.

### 2.2 Objetivos Específicos

1. Implementar un sistema de renderizado por capas con sprites 2D.
2. Aplicar el algoritmo de colisión AABB (Axis-Aligned Bounding Box).
3. Desarrollar una máquina de estados finitos para la gestión de escenas del juego.
4. Implementar animación por cuadros (frame-based animation) para los personajes.
5. Aplicar técnicas de interpolación lineal (lerp) para suavizado de cámara.
6. Demostrar el uso de canal alfa para composición de superficies semitransparentes.
7. Implementar frustum culling básico para optimización del renderizado de tiles.
8. Crear un sistema de inteligencia artificial simple mediante FSM para los guardias.
9. Aplicar el paradigma de Programación Orientada a Objetos en toda la arquitectura.
10. Documentar el código siguiendo el estándar PEP 8 y PEP 257.

---

## 3. Marco Teórico

### 3.1 Renderizado 2D con Pygame

Pygame es una biblioteca de Python construida sobre SDL (Simple DirectMedia Layer), una capa de abstracción de bajo nivel sobre las capacidades multimedia del sistema operativo. En Pygame, toda la información visual se representa mediante `pygame.Surface`, objetos que almacenan datos de píxeles en memoria y que se componen en pantalla mediante la operación `blit` (Block Image Transfer).

El proceso de renderizado en cada frame sigue el patrón:

```
1. Limpiar pantalla (fill)
2. Dibujar fondo
3. Dibujar capas intermedias
4. Dibujar HUD
5. Presentar buffer (flip)
```

Este proceso implementa el concepto de **doble buffer**: la escena se construye en un buffer de memoria oculto y se presenta completa en pantalla, evitando el artefacto visual conocido como *screen tearing* o *flickering*.

### 3.2 Sistema de Coordenadas

Pygame utiliza un sistema de coordenadas con el origen `(0,0)` en la esquina superior izquierda, con el eje X positivo hacia la derecha y el eje Y positivo hacia abajo. Esto difiere del sistema matemático estándar donde Y positivo apunta hacia arriba.

```
(0,0) ─────────────► X
  │
  │
  ▼
  Y
```

### 3.3 Sprites y Texturas

En computación gráfica 2D, un *sprite* es una imagen bidimensional integrada en una escena mayor. En Pygame, los sprites se implementan mediante la clase `pygame.sprite.Sprite`, que combina una `Surface` (imagen) con un `Rect` (posición y dimensiones). La clase `pygame.sprite.Group` permite gestionar colecciones de sprites y detectar colisiones entre ellos.

### 3.4 Colisión AABB

El método *Axis-Aligned Bounding Box* es el algoritmo de detección de colisiones más simple y eficiente para objetos 2D alineados con los ejes cartesianos. Dos rectángulos colisionan si y solo si se superponen en ambos ejes simultáneamente:

```
Colisión si:
  A.left < B.right  AND  A.right > B.left
  A.top  < B.bottom AND  A.bottom > B.top
```

Pygame implementa este algoritmo en `pygame.Rect.colliderect()`.

### 3.5 Máquina de Estados Finitos (FSM)

Una máquina de estados finitos es un modelo computacional que define un conjunto finito de estados, un estado inicial y transiciones entre estados disparadas por eventos. En videojuegos se utiliza tanto para gestionar escenas (StateManager) como para implementar comportamientos de IA (guardias).

```
Estados finitos: {S1, S2, S3, ..., Sn}
Estado actual:    S_actual
Evento:           E
Transición:       δ(S_actual, E) → S_siguiente
```

### 3.6 Interpolación Lineal (Lerp)

La interpolación lineal entre dos valores `a` y `b` con factor `t ∈ [0,1]` se define como:

```
lerp(a, b, t) = a + (b - a) * t
```

En el proyecto se usa para el seguimiento suave de la cámara. Con `t = 0.15`, la cámara recorre el 15% de la distancia restante al objetivo en cada frame, produciendo un efecto de suavizado exponencial.

### 3.7 Composición con Canal Alfa

El canal alfa define la opacidad por píxel de una imagen, permitiendo transparencias y semitransparencias. Pygame soporta canal alfa mediante `pygame.SRCALPHA`:

```
Color final = Color_src * alpha + Color_dst * (1 - alpha)
```

Este concepto es fundamental en composición de capas visuales, efectos de partículas y interfaces superpuestas.

### 3.8 Animación por Cuadros

La animación por cuadros (frame-based animation) se basa en mostrar imágenes ligeramente distintas en sucesión a velocidad suficiente para crear la ilusión de movimiento. En el proyecto, los personajes alternan entre dos frames de un ciclo de caminata controlado por un temporizador:

```
timer += delta_time
if timer >= frame_duration:
    timer = 0
    current_frame = (current_frame + 1) % num_frames
```

---

## 4. Metodología

### 4.1 Metodología de Desarrollo

Se adoptó una metodología iterativa e incremental:

1. **Iteración 1**: Configuración del proyecto, estructura de carpetas, constants.py, AssetManager.
2. **Iteración 2**: Sistema de estados (StateManager, GameData), pantallas básicas de UI.
3. **Iteración 3**: Entidades (Player, Guard, Item), sistema de colisiones.
4. **Iteración 4**: Clase base de niveles (BaseLevel), sistema de inventario.
5. **Iteración 5**: Implementación de los 5 pisos específicos.
6. **Iteración 6**: Pulido visual, efectos, notificaciones, transiciones.
7. **Iteración 7**: Documentación completa y pruebas.

### 4.2 Herramientas Utilizadas

| Herramienta | Uso |
|-------------|-----|
| Python 3.10+ | Lenguaje de programación |
| Pygame 2.x | Motor gráfico y multimedia |
| VSCode / PyCharm | Entorno de desarrollo |
| Git | Control de versiones |
| Aseprite / GIMP | Edición de sprites (opcional) |
| Audacity | Edición de audio (opcional) |

### 4.3 Convenciones de Código

- **PEP 8**: Estilo de código (nombres, indentación, longitud de línea ≤ 79 caracteres).
- **PEP 257**: Docstrings en todas las clases y funciones públicas.
- **Type Hints**: Anotaciones de tipos en parámetros y retornos.
- **Nombres descriptivos**: Variables y funciones con nombres autoexplicativos.

---

## 5. Desarrollo

### 5.1 Arquitectura del Sistema

El proyecto sigue el patrón **Model-View-Controller** adaptado a videojuegos:

- **Modelo**: `GameData`, `Inventory`, entidades (`Player`, `Guard`, `Item`).
- **Vista**: Métodos `draw()` de todas las clases, `AssetManager`.
- **Controlador**: `StateManager`, `BaseLevel.handle_event()`, `LevelManager`.

### 5.2 Implementación del StateManager

El `StateManager` almacena todas las instancias de pantallas en un diccionario y delega las operaciones al estado activo:

```python
self._states = {
    "TITLE_SCREEN":   TitleScreen(screen, self),
    "PLAYING":        LevelManager(screen, self),
    # ...
}

def update(self, dt):
    self._states[self.current_state].update(dt)
```

Este diseño permite agregar nuevos estados sin modificar el StateManager.

### 5.3 Implementación del Sistema de Tiles

El mapa de cada nivel se representa como una matriz 2D de enteros:

```python
tile_map = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 4, 0, 1],  # 4 = salida
    [1, 1, 1, 1, 1],
]
```

La conversión a rectángulos de colisión se realiza una sola vez al iniciar el nivel, generando listas de `pygame.Rect` para paredes y salidas.

### 5.4 Implementación del Sistema de Guardias

Los guardias implementan una FSM con 5 estados internos. El método `update()` actúa como dispatcher:

```python
if self.state == GUARD_STATE_PATROL:
    self._update_patrol(dt, walls)
    detected = self._check_detection(player_rects)
elif self.state == GUARD_STATE_INVESTIGATE:
    self._update_investigate(dt, walls)
# ...
```

La detección usa comparación de distancias al cuadrado para evitar la operación `sqrt` costosa:

```python
dist_sq = (px-gx)**2 + (py-gy)**2
if dist_sq <= detection_range**2:
    # detectado
```

### 5.5 Implementación del Puzzle Cooperativo (Piso 4)

El Piso 4 requiere coordinar ambos personajes. El jugador debe:
1. Cambiar a Personaje 1 con TAB → lanzar distracción con Q para alejar al guardia.
2. Cambiar a Personaje 2 con TAB → interactuar con la puerta VIP con E.

Esto se logra porque ambos personajes mantienen su posición independiente al cambiar con TAB, y el lanzamiento de distracción afecta a los guardias independientemente del personaje activo.

### 5.6 Efecto Typewriter en la Introducción

La pantalla de introducción implementa un efecto de máquina de escribir contando caracteres totales y revelando progresivamente el texto:

```python
self._display_chars += type_speed * delta_time
chars_shown = int(self._display_chars)
visible_text = full_text[:chars_shown]
```

### 5.7 Gestión de Recursos sin Archivos Externos

`AssetManager._create_fallback_surface()` genera sprites proceduralmente cuando no existen los archivos de imagen. Esto permite ejecutar el juego completo sin necesidad de archivos gráficos externos, facilitando la evaluación del proyecto.

---

## 6. Resultados Esperados

Al ejecutar el proyecto se obtendrá:

### 6.1 Funcionalidades Implementadas

| Funcionalidad | Estado |
|---------------|--------|
| Pantalla de título con menú navegable | ✅ Completo |
| Pantalla de instrucciones | ✅ Completo |
| Pantalla de créditos | ✅ Completo |
| Introducción narrativa con typewriter | ✅ Completo |
| 5 niveles jugables | ✅ Completo |
| Dos personajes alternables (TAB) | ✅ Completo |
| Sistema de inventario con HUD | ✅ Completo |
| Recolección de objetos | ✅ Completo |
| Guardias con FSM (patrulla/investigar) | ✅ Completo |
| Mecánica de distracción (Q) | ✅ Completo |
| Puertas bloqueadas con requisitos | ✅ Completo |
| Sistema de colisiones AABB | ✅ Completo |
| Cámara con seguimiento suave | ✅ Completo |
| Transiciones entre pisos (fade) | ✅ Completo |
| Menú de pausa (ESC) | ✅ Completo |
| Pantalla de victoria con estadísticas | ✅ Completo |
| Pantalla de game over | ✅ Completo |
| Sprites de respaldo automáticos | ✅ Completo |
| Gestión de audio (sin crash si falta) | ✅ Completo |
| Documentación PEP 8 / PEP 257 | ✅ Completo |

### 6.2 Aspectos Visuales

- Fondo con gradiente animado de estilo corporativo.
- Silueta de edificio en la pantalla de título.
- Indicadores visuales de estado sobre los guardias (!, ?, •).
- Efecto de halo/glow sobre objetos recolectables.
- Trail de movimiento detrás del personaje activo.
- Partículas de confeti en la pantalla de victoria.
- Efecto de scanlines CRT en la pantalla de game over.
- Transiciones fade entre pisos con nombre del piso.

---

## 7. Conclusiones

### 7.1 Conclusiones Técnicas

1. **Pygame como motor gráfico 2D** demostró ser suficientemente expresivo para implementar todos los conceptos de computación gráfica requeridos, desde renderizado básico hasta efectos de partículas y transparencias por canal alfa.

2. **La arquitectura FSM** resultó la solución más clara y mantenible tanto para la gestión de escenas del juego como para la IA de los guardias. Su estructura permite escalar el proyecto agregando nuevos estados sin modificar código existente.

3. **La separación en capas** (systems, entities, levels, ui) facilitó el desarrollo modular y evitó dependencias circulares problemáticas, siguiendo el principio de responsabilidad única.

4. **El sistema de respaldo en AssetManager** fue fundamental para que el proyecto sea evaluable sin necesidad de archivos externos, demostrando la importancia del manejo defensivo de errores en aplicaciones gráficas.

5. **El movimiento con separación de ejes** (procesar X e Y por separado) resolvió elegantemente el problema del "atascamiento en esquinas" que tiene la colisión AABB simple, permitiendo deslizamiento suave a lo largo de paredes.

### 7.2 Relación con los Objetivos del Curso

El proyecto logra demostrar de forma práctica e integrada los siguientes conceptos de Computación Gráfica:

- Renderizado 2D con superficies y texturas.
- Transformaciones de escala y rotación.
- Gestión de escenas mediante máquina de estados.
- Animación por cuadros (frame animation).
- Colisión AABB.
- Canal alfa y composición de capas.
- Interpolación lineal.
- Frustum culling.
- Doble buffer.
- Gestión de recursos gráficos.

### 7.3 Aprendizajes

El desarrollo de este proyecto permitió comprender que los videojuegos son aplicaciones de computación gráfica en tiempo real con requisitos estrictos de rendimiento, donde cada frame debe completarse en aproximadamente 16.6 ms (60 FPS). Esto obliga a tomar decisiones de optimización como el tile culling, la caché de recursos y el uso de comparaciones al cuadrado en lugar de raíces cuadradas para cálculos de distancia.

---

## 8. Bibliografía

1. **McGugan, W.** (2007). *Beginning Game Development with Python and Pygame*. Apress.

2. **Pygame Documentation** (2024). Pygame Community. Recuperado de: https://www.pygame.org/docs/

3. **Kishimoto, M.** (2019). *Game Programming Patterns*. Recuperado de: https://gameprogrammingpatterns.com/

4. **van Rossum, G., Warsaw, B., & Coghlan, A.** (2001). *PEP 8 – Style Guide for Python Code*. Python Software Foundation. https://peps.python.org/pep-0008/

5. **Goodman, D.** (2001). *PEP 257 – Docstring Conventions*. Python Software Foundation. https://peps.python.org/pep-0257/

6. **Foley, J. D., van Dam, A., Feiner, S. K., & Hughes, J. F.** (1995). *Computer Graphics: Principles and Practice* (2nd ed.). Addison-Wesley.

7. **Ericson, C.** (2004). *Real-Time Collision Detection*. Morgan Kaufmann.

8. **Shiffman, D.** (2012). *The Nature of Code: Simulating Natural Systems with Processing*. Recuperado de: https://natureofcode.com/

9. **Python Software Foundation** (2024). *Python 3 Documentation*. https://docs.python.org/3/

10. **SDL Documentation** (2024). *Simple DirectMedia Layer*. https://www.libsdl.org/

---

*Documento generado como parte del proyecto final de Computación Gráfica.*  
*Año académico 2025.*
