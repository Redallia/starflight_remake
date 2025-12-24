# DataLoader Usage Guide

## Overview
The `DataLoader` class centralizes all JSON data loading, providing consistent path resolution and error handling.

## Basic Usage

### In a Game State

```python
from core.data_loader import DataLoader

class MyState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.data_loader = DataLoader()

    def on_enter(self):
        # Load various game data
        species_data = self.data_loader.load_static("species.json")
        menu_data = self.data_loader.load_static("menu", "main_menu.json")
        planet_types = self.data_loader.load_static("planetary_info", "planet_types.json")
```

## Methods

### `load_static(*path_parts)`
Loads static game data from `src/data/static/`

**Examples:**
```python
# Load from root of static directory
skills = data_loader.load_static("skills.json")
species = data_loader.load_static("species.json")
minerals = data_loader.load_static("minerals.json")

# Load from subdirectories
menu = data_loader.load_static("menu", "main_menu.json")
shields = data_loader.load_static("ship_equipment", "shields.json")
chemistry = data_loader.load_static("planetary_info", "planetary_chemistry.json")
```

**File locations:**
- `load_static("skills.json")` → `src/data/static/skills.json`
- `load_static("menu", "main_menu.json")` → `src/data/static/menu/main_menu.json`
- `load_static("planetary_info", "planet_types.json")` → `src/data/static/planetary_info/planet_types.json`

### `load_runtime(*path_parts)`
Loads runtime data from `src/data/` (save files, generated systems)

**Examples:**
```python
# Load star systems (may be procedurally generated)
systems = data_loader.load_runtime("star_systems.json")

# Load save file
save_data = data_loader.load_runtime("saves", "game_001.json")
```

**File locations:**
- `load_runtime("star_systems.json")` → `src/data/star_systems.json`
- `load_runtime("saves", "game_001.json")` → `src/data/saves/game_001.json`

### `save_runtime(data, *path_parts)`
Saves data to JSON file in runtime directory

**Examples:**
```python
# Save game state
game_state = {
    "player": {...},
    "ship": {...},
    "crew": [...]
}
data_loader.save_runtime(game_state, "saves", "game_001.json")

# Save generated star system
system_data = generate_star_system(seed=12345)
data_loader.save_runtime(system_data, "generated", "system_12345.json")
```

**Features:**
- Automatically creates parent directories if they don't exist
- Pretty-prints JSON with 2-space indentation
- Preserves UTF-8 encoding (for alien names with special characters)

### `get_data_path(*path_parts)`
Returns the absolute path to a data file without loading it

Useful for passing paths to external libraries (like image loaders):

**Example:**
```python
# Get path to a portrait image
portrait_path = data_loader.get_data_path("static", "portraits", "human.png")
image = pygame.image.load(str(portrait_path))
```

## Error Handling

The DataLoader provides clear error messages:

```python
try:
    data = data_loader.load_static("missing_file.json")
except FileNotFoundError as e:
    print(f"Error: {e}")
    # Error: Data file not found: /path/to/src/data/static/missing_file.json

try:
    data = data_loader.load_static("malformed.json")
except json.JSONDecodeError as e:
    print(f"Error: {e}")
    # Error: Invalid JSON in /path/to/malformed.json: Expecting value: line 1 column 1 (char 0)
```

## Migration from Old Code

**Before (manual path construction):**
```python
menu_path = Path(__file__).parent.parent / "data" / "static" / "menu" / "main_menu.json"
with open(menu_path, 'r') as f:
    menu_data = json.load(f)
```

**After (using DataLoader):**
```python
menu_data = self.data_loader.load_static("menu", "main_menu.json")
```

## Common Loading Patterns

### Loading All Equipment Types
```python
engines = data_loader.load_static("ship_equipment", "engines.json")
shields = data_loader.load_static("ship_equipment", "shields.json")
weapons = data_loader.load_static("ship_equipment", "weapons.json")
armor = data_loader.load_static("ship_equipment", "armor.json")
```

### Loading Planetary Data
```python
planet_types = data_loader.load_static("planetary_info", "planet_types.json")
planet_chemistry = data_loader.load_static("planetary_info", "planetary_chemistry.json")
```

### Loading Game Configuration
```python
species = data_loader.load_static("species.json")
factions = data_loader.load_static("factions.json")
ships = data_loader.load_static("ships.json")
skills = data_loader.load_static("skills.json")
```
