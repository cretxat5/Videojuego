# 🏢 Ascenso Corporativo

> Proyecto universitario para la asignatura de **Computación Gráfica**  
> Desarrollado con Python 3 y Pygame

---

## 📖 Descripción

**Ascenso Corporativo** es un videojuego 2D de vista superior (*top-down*) donde dos estudiantes deben recorrer los cinco pisos de un edificio corporativo, recolectar documentos importantes, esquivar guardias de seguridad y llegar a la oficina del Director General para conseguir empleo.

---

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| `W A S D` | Mover personaje |
| `TAB` | Cambiar entre personajes |
| `E` | Interactuar con objetos/puertas |
| `Q` | Lanzar objeto de distracción |
| `ESC` | Pausar el juego |
| `↑ ↓ + ENTER` | Navegar menús |

---

## 🗂️ Estructura del Proyecto

```
ascenso_corporativo/
│
├── main.py                    # Punto de entrada
│
├── systems/                   # Sistemas centrales
│   ├── constants.py           # Constantes globales
│   ├── state_manager.py       # Máquina de estados
│   ├── inventory.py           # Sistema de inventario
│   ├── collision.py           # Sistema de colisiones
│   └── asset_manager.py       # Gestor de recursos
│
├── entities/                  # Entidades del juego
│   ├── player.py              # Personaje jugable
│   ├── guard.py               # Guardia de seguridad
│   └── item.py                # Objetos recolectables
│
├── levels/                    # Niveles / Pisos
│   ├── base_level.py          # Clase base abstracta
│   ├── level_manager.py       # Gestor de transiciones
│   ├── floor1.py              # Piso 1: Recepción
│   ├── floor2.py              # Piso 2: Administración
│   ├── floor3.py              # Piso 3: Recursos Humanos
│   ├── floor4.py              # Piso 4: Oficinas Ejecutivas
│   └── floor5.py              # Piso 5: Dirección General
│
├── ui/                        # Pantallas de interfaz
│   ├── base_screen.py         # Clase base de pantallas
│   ├── title_screen.py        # Pantalla de título
│   ├── instructions_screen.py # Instrucciones
│   ├── credits_screen.py      # Créditos
│   ├── intro_screen.py        # Introducción narrativa
│   ├── pause_menu.py          # Menú de pausa
│   ├── win_screen.py          # Pantalla de victoria
│   └── game_over_screen.py    # Pantalla de derrota
│
└── assets/                    # Recursos multimedia
    ├── personajes/            # Sprites de jugadores
    ├── guardias/              # Sprites de guardias
    ├── objetos/               # Sprites de objetos
    ├── fondos/                # Imágenes de fondo
    └── sonidos/               # Efectos y música
```

---

## ⚙️ Instalación

### 1. Prerrequisitos

- Python 3.10 o superior
- pip

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install pygame
```

### 4. Ejecutar el juego

```bash
cd ascenso_corporativo
python main.py
```

---

## 🖼️ Personalizar Sprites

Para usar fotografías de los estudiantes:

1. Recortar la foto con fondo transparente (formato PNG).
2. Guardar como `player1_down.png` y `player2_down.png` en `assets/personajes/`.
3. Para animación, crear variantes: `_up`, `_left`, `_right`.

**Si no se colocan imágenes**, el juego funciona con sprites de respaldo de colores (azul para P1, naranja para P2).

---

## 🏆 Objetivo del Juego

Recolectar los **4 documentos requeridos** y llegar a la oficina del director:

| Documento | Piso |
|-----------|------|
| Identificación Temporal | Piso 1 - Recepción |
| Carpeta de Documentos | Piso 2 - Administración |
| Tarjeta de Acceso | Piso 3 - Recursos Humanos |
| Hoja de Vida Oficial | Piso 4 - Oficinas Ejecutivas |

---

## 🤖 Sistema de Guardias

Los guardias siguen una máquina de estados:

```
PATROL → WAIT → PATROL → ...
           ↓
       INVESTIGATE (escuchó sonido)
           ↓
        RETURN (regresa a ruta)
           ↓
        PATROL
```

---

## 🎓 Información Académica

- **Materia:** Computación Gráfica
- **Tecnologías:** Python 3, Pygame
- **Paradigma:** Programación Orientada a Objetos
- **Patrones de diseño:** State Machine, Template Method, Singleton

---

## 📦 Dependencias

```
pygame >= 2.1.0
```

---

*Proyecto educativo — Computación Gráfica*
