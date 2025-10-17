# 🃏 Solitario Klondike - Proyecto Programación III

## 📋 Descripción General

Proyecto completo de juego de Solitario (Klondike) desarrollado en Python con interfaz web. Este proyecto cumple con todos los requisitos establecidos en las consignas del curso de Programación III.

## 🎯 Características Principales

- ✅ **Arquitectura modular** con separación frontend/backend
- ✅ **Programación Orientada a Objetos** con herencia y polimorfismo
- ✅ **CRUD completo** en la clase principal (Deck)
- ✅ **Persistencia de datos** con JSON
- ✅ **Interfaz gráfica web** HTML5 + CSS3 + JavaScript
- ✅ **API REST** con Flask
- ✅ **Sistema de guardado/carga** de partidas
- ✅ **Estadísticas** de juego

## 📁 Estructura del Proyecto

```
solitaire/
├── backend/
│   ├── __init__.py          # Inicialización del paquete
│   ├── card.py              # Clase Card (hereda de AbstractCard)
│   ├── deck.py              # Clase Deck con CRUD completo
│   ├── game_manager.py      # Lógica principal del juego
│   ├── database.py          # Persistencia con JSON
│   └── main.py              # Servidor Flask y punto de entrada
│
├── frontend/
│   ├── index.html           # Interfaz del juego
│   ├── style.css            # Estilos visuales
│   └── script.js            # Lógica de interacción (fetch API)
│
├── requirements.txt         # Dependencias Python
└── README.md                # Este archivo
```

## 🧱 Requisitos Cumplidos

### 1. Clases y Herencia

#### `AbstractCard` (Clase Abstracta)
- Clase abstracta con métodos abstractos: `get_value()`, `get_suit()`, `is_red()`, `to_dict()`

#### `Card` (Hereda de AbstractCard)
- Implementa todos los métodos abstractos
- Atributos: `suit`, `value`, `face_up`
- Métodos adicionales: `flip()`, `can_place_on()`, `from_dict()`
- **Polimorfismo**: Sobrecarga de operadores `__str__`, `__repr__`, `__eq__`

#### `Deck` (Clase Principal con CRUD)
**5 Atributos:**
1. `deck_id` (str) - Identificador único
2. `created_at` (str) - Timestamp de creación
3. `shuffled` (bool) - Estado de mezclado
4. `size` (int) - Número de cartas
5. `__cards` (deque) - **Encapsulado** (privado)

**CRUD Completo:**
- ✅ **CREATE**: `create_card(suit, value, face_up)` - Crea y agrega carta
- ✅ **READ**: `read_card(index)` - Lee carta en posición específica
- ✅ **UPDATE**: `update_card(index, suit, value, face_up)` - Actualiza atributos
- ✅ **DELETE**: `delete_card(index)` - Elimina carta del mazo

**Polimorfismo:**
- Sobrecarga del operador `len()` con `__len__()`
- Métodos `__str__()` y `__repr__()`

#### `GameManager`
- Gestiona la lógica del Solitario Klondike
- **Relación de uso**: Utiliza instancias de `Deck` y `Card`
- Maneja: tableau, foundations, stock, waste
- Validación de movimientos según reglas del juego

#### `Database`
- Simula base de datos con archivos JSON
- Guardar/cargar/listar/eliminar partidas
- Estadísticas de juego
- Exportar/importar partidas

### 2. Módulos Obligatorios (Mínimo 3)

✅ **1. `collections.deque`** - Usado en:
- `Deck.__cards`: Cola de cartas (estructura de datos eficiente)
- `GameManager.stock`: Mazo de robo
- `GameManager.waste`: Pila de descarte

✅ **2. `json`** - Usado en:
- `database.py`: Persistencia completa de datos
- Guardar/cargar estado del juego
- Serialización de objetos (Card, Deck, GameManager)

✅ **3. `re` (regex)** - Usado en:
- `game_manager.py`: Validación de formato de ubicaciones
- Patrón: `r'^(tableau_\d|foundation_\w+|waste|stock)$'`

✅ **4. `random`** - Usado en:
- `deck.py`: Método `shuffle()` para mezclar cartas

✅ **5. `abc` (Abstract Base Classes)** - Usado en:
- `card.py`: Clase abstracta `AbstractCard`

✅ **6. `datetime`** - Usado en:
- `database.py`: Timestamps de creación y modificación
- `deck.py`: Timestamp de creación del mazo

### 3. Interfaz Gráfica

✅ **Frontend Web Completo:**
- **HTML5**: Estructura semántica del juego
- **CSS3**: Diseño responsivo con gradientes y animaciones
- **JavaScript**: Interacción con DOM y comunicación con API

✅ **Funcionalidades:**
- Nuevo juego
- Mover cartas (click para seleccionar y mover)
- Extraer del mazo
- Guardar/cargar partidas
- Ver estadísticas
- Mensajes de feedback
- Modal para victorias
- Responsive design

### 4. Documentación

✅ **Todo el código está documentado con:**
- Comentarios `#` para explicaciones en línea
- Docstrings `""" """` en todas las clases y funciones
- Descripción de parámetros, retornos y excepciones
- Ejemplos de uso donde corresponde

### 5. Buenas Prácticas

✅ **Cumplimiento de estándares:**
- Nombres descriptivos (snake_case para funciones, PascalCase para clases)
- Modularización y separación de responsabilidades
- Manejo de excepciones
- Type hints en Python
- Código DRY (Don't Repeat Yourself)

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar/Descargar el proyecto

```bash
cd solitaire
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar el juego

```bash
python -m backend.main
```

O directamente:

```bash
python backend/main.py
```

## Despliegue

### Despliegue 1-Clic (Render)

Haz clic en el botón para desplegar el proyecto automáticamente en Render. Asegúrate de que tu repositorio esté público en GitHub y, si es necesario, reemplaza la URL del repo en el enlace.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tu-usuario/lean)

Este repositorio incluye `render.yaml`, por lo que Render detectará la configuración y creará un servicio web de Python con:

- build: `pip install -r requirements.txt`
- start: `python -m backend.main`

La aplicación expone el puerto definido por la variable de entorno `PORT` (por defecto `5000`).

### Despliegue manual en Render

1. Crea una cuenta en Render (gratuita) y haz clic en `New > Web Service`.
2. Conecta tu cuenta de GitHub y selecciona este repositorio.
3. Configura:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m backend.main`
   - Auto Deploy: On (opcional)
4. Despliega. Render asignará una URL pública.

Notas:
- El backend Flask sirve el frontend estático desde `frontend/` en la ruta `/`.
- No se requieren variables de entorno adicionales.

### Paso 4: Abrir en el navegador

Acceder a: **http://localhost:5000**

## 🎮 Cómo Jugar

### Reglas del Solitario Klondike

1. **Objetivo**: Mover todas las cartas a las 4 fundaciones (una por palo) en orden ascendente (As → Rey)

2. **Tableau (7 columnas)**:
   - Las cartas se apilan en orden descendente
   - Deben alternar colores (roja sobre negra, negra sobre roja)
   - Solo se pueden mover Reyes a espacios vacíos

3. **Stock (Mazo)**:
   - Click para extraer cartas
   - Si se vacía, se reinicia automáticamente

4. **Movimientos**:
   - Click en una carta para seleccionarla
   - Click en el destino para moverla
   - El juego valida automáticamente los movimientos

### Controles

- **Nuevo Juego**: Inicia una partida nueva
- **Guardar Partida**: Guarda el estado actual
- **Cargar Partida**: Lista y carga partidas guardadas
- **Estadísticas**: Muestra estadísticas generales
- **Mazo (Stock)**: Click para extraer carta

## 📊 API REST Endpoints

### Juego

- `POST /api/new_game` - Inicia nuevo juego
- `POST /api/draw_card` - Extrae carta del mazo
- `POST /api/move_card` - Mueve carta(s) entre ubicaciones
- `GET /api/game_state` - Obtiene estado actual

### Persistencia

- `POST /api/save_game` - Guarda partida actual
- `GET /api/load_game/<game_id>` - Carga partida específica
- `GET /api/list_games` - Lista todas las partidas guardadas
- `DELETE /api/delete_game/<game_id>` - Elimina partida
- `GET /api/statistics` - Obtiene estadísticas

## 🧪 Ejemplo de Uso desde Python (Consola)

```python
from backend.game_manager import GameManager
from backend.database import Database

game = GameManager(game_id="test_game")
game.new_game()

print(f"Movimientos: {game.moves_count}")

game.draw_from_stock()

result = game.move_card("waste", "tableau_0")
print(result['message'])

db = Database()
db.save_game(game.game_id, game.to_dict())

stats = db.get_statistics()
print(f"Total de juegos: {stats['total_games']}")
```

## 📦 Dependencias

Ver `requirements.txt`:
- **Flask 3.0.0**: Framework web para el servidor
- **flask-cors 4.0.0**: Manejo de CORS para comunicación frontend-backend
- **Werkzeug 3.0.1**: Utilidades WSGI para Flask

## 🏆 Extras Implementados

- ✅ Sistema de estadísticas completo
- ✅ Mensajes de feedback visual
- ✅ Animaciones CSS
- ✅ Modal de victoria con celebración
- ✅ Diseño responsivo para móviles
- ✅ Validación completa de movimientos
- ✅ Sistema de timestamps
- ✅ Exportar/importar partidas
- ✅ Backup de base de datos

## 🎓 Consignas Cumplidas

### Checklist Completo

- [x] Mínimo dos clases (implementadas: Card, Deck, GameManager, Database)
- [x] Una clase hereda de clase abstracta (Card → AbstractCard)
- [x] Clase principal con 5 atributos (Deck: deck_id, created_at, shuffled, size, __cards)
- [x] Un atributo encapsulado (__cards en Deck)
- [x] CRUD completo en clase principal (Deck: create, read, update, delete)
- [x] Polimorfismo (sobrecarga de operadores en Card y Deck)
- [x] Relación de uso entre clases (GameManager usa Deck y Card)
- [x] Mínimo 3 módulos (collections, json, re, random, abc, datetime)
- [x] Interfaz gráfica/interactiva (HTML/CSS/JS con Flask)
- [x] Todo el código comentado y documentado
- [x] Archivo requirements.txt
- [x] Función main() como punto de entrada
- [x] README.md completo

## 👥 Créditos

Proyecto desarrollado para la materia **Programación III** - Trabajo Final Grupal

## 📄 Licencia

Este proyecto es con fines educativos. Desarrollado como trabajo práctico universitario.

---

## 🔧 Troubleshooting

### El servidor no inicia
```bash
pip install --upgrade -r requirements.txt
python -m backend.main
```

### Error de módulos no encontrados
Asegúrate de estar en el directorio raíz del proyecto y ejecutar:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python backend/main.py
```

### Puerto 5000 ocupado
Edita `backend/main.py` y cambia el puerto:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

**¡Disfruta del juego!** 🎉
