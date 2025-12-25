# Game States Documentation

This directory contains specifications for each major game state in Starflight Remake.

## State Overview

| State | Status | Priority | Description |
|-------|--------|----------|-------------|
| [Main Menu](main_menu.md) | ✅ Implemented | MVP | Initial screen with New/Load/Exit |
| [Starport](starport.md) | ✅ Basic | MVP | Hub for ship/crew management (currently simple menu) |
| [Space Navigation](space_navigation.md) | 🚧 Placeholder | MVP | Flying through space (hyperspace & system space) |
| [Orbit](orbit.md) | ❌ Not started | MVP | Orbiting planets, scanning, landing |
| [Surface](surface.md) | ❌ Not started | MVP | Terrain vehicle exploration, resource gathering |
| [Communications](communications.md) | ❌ Not started | MVP | Alien dialogue and derelict interaction |
| [Combat](combat.md) | ❌ Not started | Post-MVP | Ship combat (design TBD) |

## State Flow

```
Main Menu
    ↓ (New Game)
Starport ←→ Space Navigation ←→ Orbit ←→ Surface
              ↓                    ↑
         Communications      (Hostile encounter)
              ↓
         Combat (future)
```

## Implementation Status Legend
- ✅ **Implemented**: Functional, though may be basic or placeholder
- 🚧 **In Progress**: Partially implemented
- ❌ **Not Started**: Design documented but no code yet
- 🔮 **Future**: Post-MVP, lower priority

## HUD Usage

States are categorized by whether they use the standard 4-area HUD:

### Uses Standard HUD
- Space Navigation (hyperspace & system space)
- Orbit
- Communications

### Uses Modified HUD
- Surface (different layout, shallower menus)

### No HUD (Full-Screen)
- Main Menu
- Starport (currently menu, future: side-scroller)
- Combat (TBD)

## Reading These Docs

Each state document includes:
- **Overview**: What the state is for
- **State Information**: Technical details (name, implementation status)
- **HUD Layout**: What appears in each area (if using HUD)
- **Input Handling**: How player controls work
- **State Transitions**: How you get to/from this state
- **Data Requirements**: What data is needed
- **Game State Requirements**: What runtime state must exist
- **Implementation Phases**: Suggested build order
- **Notes**: Design considerations and open questions

## Contributing

When adding or updating state docs:
1. Keep the structure consistent with existing docs
2. Update this README's status table
3. Note dependencies on other states or systems
4. Flag open design questions that need resolution
5. Link to related docs (HUD spec, data schemas, etc.)
