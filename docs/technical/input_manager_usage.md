# InputManager Usage Guide

## Overview
The `InputManager` class provides an abstraction layer between raw pygame events and game actions. This makes it easy to:
- Avoid repeating key bindings across states
- Support multiple keys for the same action
- Add controller/gamepad support later
- Allow players to rebind keys

## Basic Usage

### In a Game State

```python
from core.input_manager import InputManager

class MyState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.input_manager = InputManager()

    def handle_event(self, event):
        # Convert event to action
        action = self.input_manager.get_action(event)

        # Handle the action
        if action == "menu_up":
            self.selected_index -= 1
        elif action == "menu_down":
            self.selected_index += 1
        elif action == "confirm":
            self.handle_selection()
```

## Available Actions

### Menu Navigation
- `menu_up` - W, Up Arrow, Numpad 8
- `menu_down` - S, Down Arrow, Numpad 2
- `menu_left` - A, Left Arrow, Numpad 4
- `menu_right` - D, Right Arrow, Numpad 6
- `confirm` - Enter, Space
- `cancel` - Escape, Backspace

### Ship Navigation
- `nav_up` - W, Up Arrow, Numpad 8
- `nav_down` - S, Down Arrow, Numpad 2
- `nav_left` - A, Left Arrow, Numpad 4
- `nav_right` - D, Right Arrow, Numpad 6
- `nav_toggle` - Space (toggle navigation mode on/off)

More actions will be added as needed (weapons, shields, scanning, etc.)

## Methods

### `get_action(event)`
Converts a pygame event to a game action (if it matches a binding)

**Returns:** Action name (string) or None

```python
def handle_event(self, event):
    action = self.input_manager.get_action(event)
    if action == "menu_up":
        # Handle up action
        pass
```

### `is_key_pressed(action)`
Checks if any key for an action is currently pressed

Useful for continuous input like ship movement:

```python
def update(self, dt):
    # Continuous movement while key is held
    if self.input_manager.is_key_pressed("nav_up"):
        self.ship_y -= self.speed * dt
    if self.input_manager.is_key_pressed("nav_down"):
        self.ship_y += self.speed * dt
```

### `add_binding(action, key)`
Add an additional key binding to an action

```python
# Add 'J' as an alternative "up" key
input_manager.add_binding("menu_up", pygame.K_j)
```

### `remove_binding(action, key)`
Remove a key binding from an action

```python
# Remove Space from confirm action
input_manager.remove_binding("confirm", pygame.K_SPACE)
```

### `get_bindings_for_action(action)`
Get all keys bound to an action

```python
keys = input_manager.get_bindings_for_action("menu_up")
# Returns: [pygame.K_w, pygame.K_UP, pygame.K_KP8]
```

### `get_action_display_name(action)`
Get a human-readable name for displaying controls

```python
name = input_manager.get_action_display_name("confirm")
# Returns: "RETURN" (the name of the first bound key)

# Useful for showing controls to player:
print(f"Press {name} to select")
# Output: "Press RETURN to select"
```

## Usage Patterns

### Menu-Based State (like MainMenu, Starport)

```python
def handle_event(self, event):
    action = self.input_manager.get_action(event)

    if action == "menu_up":
        self.selected_index = (self.selected_index - 1) % len(self.options)
    elif action == "menu_down":
        self.selected_index = (self.selected_index + 1) % len(self.options)
    elif action == "confirm":
        self.handle_selection()
    elif action == "cancel":
        self.return_to_previous_state()
```

### Ship Navigation State

```python
def handle_event(self, event):
    action = self.input_manager.get_action(event)

    if action == "nav_toggle":
        self.navigation_active = not self.navigation_active

def update(self, dt):
    if not self.navigation_active:
        return

    # Continuous movement using is_key_pressed
    if self.input_manager.is_key_pressed("nav_up"):
        self.move_ship(0, -1, dt)
    if self.input_manager.is_key_pressed("nav_down"):
        self.move_ship(0, 1, dt)
    if self.input_manager.is_key_pressed("nav_left"):
        self.move_ship(-1, 0, dt)
    if self.input_manager.is_key_pressed("nav_right"):
        self.move_ship(1, 0, dt)
```

### Modal Dialog (use menu navigation)

```python
def handle_event(self, event):
    action = self.input_manager.get_action(event)

    if action == "menu_left":
        self.selected_button = "no"
    elif action == "menu_right":
        self.selected_button = "yes"
    elif action == "confirm":
        if self.selected_button == "yes":
            self.execute_action()
        self.close_dialog()
    elif action == "cancel":
        self.close_dialog()
```

## Migration from Old Code

**Before (direct key checking):**
```python
def handle_event(self, event):
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_w, pygame.K_UP, pygame.K_KP8):
            self.selected_index -= 1
        elif event.key in (pygame.K_s, pygame.K_DOWN, pygame.K_KP2):
            self.selected_index += 1
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.handle_selection()
```

**After (using InputManager):**
```python
def handle_event(self, event):
    action = self.input_manager.get_action(event)

    if action == "menu_up":
        self.selected_index -= 1
    elif action == "menu_down":
        self.selected_index += 1
    elif action == "confirm":
        self.handle_selection()
```

## Benefits

1. **No key repetition** - Define bindings once, use everywhere
2. **Multiple keys per action** - W/Up/Numpad8 all work for "up"
3. **Easy to extend** - Add gamepad support by updating InputManager
4. **Rebindable** - Players can customize controls later
5. **Readable code** - `if action == "menu_up"` is clearer than checking key codes
6. **Context-aware** - Same keys can mean different things in different contexts
