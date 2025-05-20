# Conway's Game of Life – Pygame Implementation

This project is a fully interactive implementation of Conway’s Game of Life using Python and Pygame. It features a graphical interface, save/load functionality, settings for visual customization, and support for loading predefined patterns.

---

## 🎮 Features

- Customizable cell colors (alive/dead)
- Interactive main menu with buttons
- Pause and modify grid manually
- Save/load game state using `pickle`
- Load predefined patterns from files
- Clean grid and resume controls

---

## 📁 Project Structure

```bash
.
├── fonts/
│   └── PressStart2P.ttf
├── static_patterns/
│   └── *.pkl         # Predefined pattern files
├── savegame.pkl      # Save file (generated at runtime)
├── game_of_life.py   # Main script
```

---

## ⚙️ Configuration

```python
CELL_SIZE = 10
GRID_WIDTH = 80
GRID_HEIGHT = 60
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10
SAVE_FILE = "savegame.pkl"
```

---

## 🎨 Colors

Defined using RGB tuples:

```python
WHITE = (255, 255, 255)
DEAD_COLOR = (30, 30, 30)
ALIVE_COLOR = (0, 255, 0)
GRID_COLOR = (50, 50, 50)
BG_COLOR = (40, 40, 40)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER = (0, 150, 0)
```

---

## 🧩 Components

### `Button` Class

Reusable UI button with custom rendering and mouse click handling.

```python
class Button:
    def __init__(...)
    def draw(surface)
    def check_click(pos)
```

---

## 💾 Save/Load

### Save Grid

```python
def save_grid(grid)
```

Serializes and writes the grid to `savegame.pkl`.

### Load Grid

```python
def load_grid()
```

Loads grid from file or returns an empty grid.

---

## 🧠 Game Logic

### Core Loop

```python
def run_game(grid=None)
```

Main loop with support for:
- Pausing (`Space`)
- Clearing (`C`)
- Pause menu (`P`)
- Mouse-based grid editing when paused

### Update Logic

```python
def update_grid(grid)
```

Applies Conway’s rules to update the grid.

---

## 🧮 Neighbor Counting

```python
def count_neighbors(grid, y, x)
```

Counts 8-connected neighbors with wrap-around behavior.

---

## ⏸ Pause Menu

```python
def pause_menu()
```

Pause options:
- Continue
- Save
- Return to Main Menu

---

## 🎛 Settings Menu

```python
def show_settings()
```

Lets user pick alive/dead cell colors from a preset palette.

---

## 📂 Pattern Selection

```python
def choose_pattern_menu()
```

Lists `.pkl` patterns from `static_patterns/` directory and loads selected ones into the game.

---

## 🏠 Main Menu

```python
def main_menu()
```

Menu options:
- Start (empty grid)
- Load Save
- Choose Pattern
- Settings
- Quit

---

## 🧪 Entry Point

```python
if __name__ == "__main__":
    main_menu()
```

Starts the game by launching the main menu.

---

## ✅ Controls Summary

| Action          | Key/Button       |
|-----------------|------------------|
| Toggle Pause    | `Space`          |
| Clear Grid      | `C`              |
| Pause Menu      | `P`              |
| Edit Grid (Paused) | Left Mouse     |
| Save Grid       | Pause Menu → Save|
| Load Save       | Main Menu        |
| Change Colors   | Settings         |

---

## 📦 Dependencies

- `pygame`
- `numpy`
- `pickle`

Install via:

```bash
pip install -r requirements.txt
```

---

## 🔚 Notes

- Ensure `fonts/PressStart2P.ttf` exists or change the font path.
- Save and pattern files use Python's `pickle` and must not be tampered with externally.
- Settings and save/load are persistent within a session.
