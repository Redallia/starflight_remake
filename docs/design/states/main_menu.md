# Main Menu State

## Overview
The initial screen shown when the game launches. Players can start a new game, load a saved game, or exit.

## State Information
- **State Name**: `main_menu`
- **Implementation**: `src/states/main_menu_state.py`
- **Uses HUD**: No (full-screen menu)
- **Status**: ✅ Implemented

## Visual Layout
Full-screen menu with centered title and vertically stacked options.

```
┌─────────────────────────────────────┐
│                                     │
│          STARFLIGHT                 │
│                                     │
│         > New Game                  │
│           Load Game                 │
│           Exit Game                 │
│                                     │
└─────────────────────────────────────┘
```

## Menu Options
- **New Game**: Creates new game state, transitions to Starport
- **Load Game**: (Future) Shows save file selection
- **Exit Game**: Quits application

## Input Handling
- **W/S, Up/Down, Numpad 8/2**: Navigate menu
- **Space/Enter**: Select option
- **ESC**: Quit game (handled globally in main loop)

## State Transitions
- **To Starport**: When "New Game" is selected
- **To LoadGame**: (Future) When "Load Game" is selected

## Data Requirements
- Menu configuration: `src/data/static/menu/main_menu.json`

## Notes
- First state loaded when game starts
- Creates initial game state when "New Game" is selected
- No game state required to display this screen
