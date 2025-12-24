# State-Based Architecture

## Overview
The game uses a state machine pattern where each major screen/mode is a separate state. The StateManager handles transitions between states.

## Core Components

### GameState (base class)
Located: `src/core/game_state.py`

Base class that all game states inherit from. Defines the interface:
- `handle_event(event)` - Process pygame events
- `update(dt)` - Update logic (dt = delta time in seconds)
- `render(surface)` - Draw to screen
- `on_enter()` - Called when state becomes active
- `on_exit()` - Called when leaving state

### StateManager
Located: `src/core/state_manager.py`

Manages state registration and transitions:
- `register_state(name, state)` - Add a state to the manager
- `change_state(name)` - Switch to a different state
- `get_current_state()` - Get the active state

### Main Loop
Located: `src/main.py`

Simplified main loop that:
1. Initializes Pygame and creates window
2. Creates StateManager
3. Registers all game states
4. Sets initial state
5. Game loop:
   - Handle events (QUIT, ESC, VIDEORESIZE, then pass to current state)
   - Update current state
   - Render current state
   - Display and tick

## Current States

### MainMenuState
Located: `src/states/main_menu_state.py`

The initial state. Loads menu configuration from `src/data/static/menu/main_menu.json` and displays:
- Title: "STARFLIGHT"
- Options: New Game, Load Game (disabled), Exit Game
- Navigation: W/S, Up/Down, Numpad 8/2
- Selection: Enter or Space

## Adding New States

To add a new state (e.g., Starport):

1. Create `src/states/starport_state.py`:
```python
from core.game_state import GameState

class StarportState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        # Initialize state-specific data

    def handle_event(self, event):
        # Handle input
        pass

    def update(self, dt):
        # Update logic
        pass

    def render(self, surface):
        # Render starport UI
        pass

    def on_enter(self):
        # Setup when entering starport
        pass
```

2. Register in `src/main.py`:
```python
from states.starport_state import StarportState

state_manager.register_state("starport", StarportState(state_manager))
```

3. Transition from another state:
```python
self.state_manager.change_state("starport")
```

## Planned States

Based on design docs, future states will include:
- **StarportState** - Ship management, crew, upgrades
- **SpaceNavigationState** - Flying in local space (HYPERSPACE or LOCAL_SPACE context)
- **OrbitState** - Planet orbit, scanning, landing selection
- **SurfaceState** - Terrain vehicle exploration
- **CommunicationsState** - Alien dialogue
- **CombatState** - Ship combat encounters

Each state encapsulates its own:
- Input handling
- Update logic
- Rendering
- Data loading

This keeps the code modular and maintainable.
