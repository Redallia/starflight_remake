# Design Specification

## Overview
This document captures the architectural patterns, coding conventions, and design decisions for the Starflight Remake project.

## Project Architecture

### Directory Structure
```
starflight_remake/
├── src/
│   ├── core/           # Pure game logic (Godot-portable)
│   ├── ui/             # Pygame-specific rendering
│   └── main.py         # Entry point
├── docs/
│   ├── design/         # Game design documents
│   └── technical/      # Technical specifications
└── tests/
```

### Core Design Principles

1. **Separation of Concerns**
   - `core/` contains pure game logic with no Pygame dependencies
   - `ui/` contains all Pygame-specific rendering and input
   - Easy migration path to Godot

2. **Model-View Separation**
   - GameState holds all game data
   - Screens read from GameState and display
   - Screens call GameState methods to modify state

3. **Screen Lifecycle Pattern**
   - `on_enter()` - Initialize when screen becomes active
   - `update(delta_time, input_handler)` - Game logic per frame
   - `render(screen)` - Visual output per frame
   - `on_exit()` - Cleanup when leaving screen

## Core Systems

### GameState (`core/game_state.py`)
Central data model for all game state.

**Current Properties:**
- `fuel: float` - Current fuel (0-100)
- `max_fuel: float` - Max fuel capacity (100)
- `credits: int` - Player currency (starts at 1000)
- `cargo_capacity: int` - Max cargo space (50)
- `cargo_used: int` - Current cargo used (0)
- `cargo: dict` - Resource inventory {resource_type: quantity}
- `location: str` - Current location ("starport", "space", "orbit", "planet_surface")

**Key Methods:**
- `can_launch()` - Check if fuel > 0
- `launch_to_space()` - Transition to space
- `return_to_starport()` - Return to starport
- `get_cargo_free_space()` - Calculate available cargo space
- `get_status_summary()` - Format status for UI display

**Design Notes:**
- Pure data object, no dependencies
- Simple getter/setter methods
- Encapsulates location state machine
- Future: Extract Ship as separate class

### ScreenManager (`core/screen_manager.py`)
Manages screen registration and transitions.

**Key Methods:**
- `add_screen(name, screen)` - Register a screen
- `change_screen(name)` - Switch to different screen
- `update(delta_time, input_handler)` - Update current screen
- `render(screen)` - Render current screen

**Screen Lifecycle:**
```
on_enter() → update() (loop) → render() (loop) → on_exit() → next screen
```

### InputHandler (`core/input_handler.py`)
Abstracts input handling from Pygame.

**Key Methods:**
- `update(events)` - Process Pygame events
- `is_key_pressed(key)` - Check if key currently held
- `is_key_just_pressed(key)` - Check if key pressed this frame
- `is_key_just_released(key)` - Check if key released this frame

**Convenience Methods:**
- `is_up_pressed()` - W key
- `is_down_pressed()` - S key
- `is_left_pressed()` - A key
- `is_right_pressed()` - D key
- `is_confirm_pressed()` - Enter or Space (just pressed)
- `is_cancel_pressed()` - ESC (just pressed)

**Usage Guidelines:**
- Use `is_key_just_pressed()` for single actions (menu selection)
- Use `is_key_pressed()` for continuous actions (movement)

### Renderer (`ui/renderer.py`)
Centralizes all Pygame drawing operations.

**Available Fonts:**
- `default_font` - 24pt
- `large_font` - 36pt
- `small_font` - 18pt

**Drawing Methods:**
- `clear(color)` - Fill screen with color
- `draw_text(text, x, y, color, font)`
- `draw_text_centered(text, x, y, color, font)`
- `draw_rect(x, y, width, height, color, filled)`
- `draw_circle(x, y, radius, color, filled)`
- `draw_line(x1, y1, x2, y2, color, width)`
- `draw_grid(x, y, cell_size, rows, cols, color)`

## Screen Implementation Pattern

### Base Screen Class
All screens must inherit from `Screen` base class and implement:

```python
class MyScreen(Screen):
    def __init__(self, screen_manager, game_state):
        super().__init__()
        self.screen_manager = screen_manager
        self.game_state = game_state

    def on_enter(self):
        # Initialize screen-specific state
        pass

    def update(self, delta_time, input_handler):
        # Handle input and game logic
        # Use delta_time for frame-rate independence
        pass

    def render(self, screen):
        from ui.renderer import Renderer
        renderer = Renderer(screen)
        renderer.clear((0, 0, 0))
        # Drawing calls here

    def on_exit(self):
        # Cleanup if needed
        pass
```

### Current Screens
- **MainMenuScreen** - Navigation with W/S, selection with Enter/Space
- **StarportScreen** - Hub with status display and menu options
- **SpaceScreen** - Space navigation (currently placeholder)

### Screen Transition Flow
```
Main Menu → (New Game) → Starport → (Launch) → Space → (Return) → Starport
```

## Game Loop (`main.py`)

### Main Loop Structure
```python
while running:
    delta_time = clock.tick(60) / 1000.0  # Convert ms to seconds

    # Input
    events = pygame.event.get()
    input_handler.update(events)

    # Update
    screen_manager.update(delta_time, input_handler)

    # Render
    screen_manager.render(screen)
    pygame.display.flip()
```

**Key Points:**
- 60 FPS target
- Variable delta_time for frame-rate independence
- All timing should use delta_time
- ESC quits from main menu only

## Coding Conventions

### Naming
- **Classes:** PascalCase (`GameState`, `ScreenManager`)
- **Methods:** snake_case (`launch_to_space`, `is_key_pressed`)
- **Constants:** UPPER_CASE (`WINDOW_WIDTH`, `FPS`)

### Imports
- Use relative imports within src/ (`from core.game_state import GameState`)
- Import Renderer inline in render methods if needed

### Documentation
- Module docstrings explain purpose
- Class docstrings describe responsibility
- Method docstrings document parameters and behavior
- Comments for non-obvious logic

### Color Conventions
- **Background:** (0, 0, 0) for space, (0, 0, 20) for menus
- **Text:** (255, 255, 255) normal, (255, 255, 0) selected
- **Accents:** (100, 200, 255) titles, (150, 150, 150) instructions

## Phase 2: Space Navigation Specifications

### Grid System
- **Coordinate Grid:** 50x50 for planetary systems
- **Movement Grid:** 500x500 (10:1 ratio to coordinates)
- **Display:** Show only coordinate position to player
- **Camera:** Centered on player ship

### Movement System
- **Controls:** WASD for directional movement
- **Speed:** TBD based on playtesting
- **Fuel Consumption:** Per movement action
- **Position Tracking:** Both movement grid (internal) and coordinate grid (displayed)

### Visual Elements
- **Starfield:** Random star dots with parallax scrolling
- **Ship:** Simple sprite/representation
- **Planets:** TBD count and placement
- **HUD:** Display coordinates, fuel, cargo

### Implementation Approach

**Step 1: Extend GameState**
- Add ship position (movement grid coordinates)
- Add coordinate conversion methods
- Add fuel consumption logic

**Step 2: Implement SpaceScreen**
- WASD movement handling
- Starfield rendering with parallax
- Ship rendering at screen center
- Coordinate display in HUD
- Fuel consumption

**Step 3: Add Planets**
- Planet data structure
- Planet rendering in space
- Proximity detection
- Orbit transition preparation

## Future Considerations

### Planned Improvements
- Extract Ship as dedicated class
- Create Entity/GameObject base class
- Implement configuration loader (JSON)
- Add resource/asset manager
- Add logging system
- Input mapping/rebinding system

### Migration Path to Godot
- Core logic is pure Python (no Pygame dependencies)
- Screen lifecycle maps to Godot scenes
- InputHandler abstracts input source
- Renderer is isolated replacement target

## Development Workflow

### Adding New Features
1. Extend GameState with necessary data
2. Create/modify Screen subclass
3. Register screen in main.py
4. Implement update/render logic
5. Test transitions between screens

### Testing
- Manual playtesting for MVP
- Focus on game feel and balance
- Test all screen transitions
- Verify fuel/cargo calculations

## References
- [MVP Definition](../design/mvp.md)
- [Architecture Overview](architecture.md)
- [Game Loops](../design/game_loops.md)
