# Technical Documentation Index

## Core Technical Documents

These documents define fundamental systems and should be treated as **single sources of truth**. Other documents should reference these rather than redefining the same concepts.

### 1. [Coordinate Systems](coordinate_systems.md) 🎯
**The foundation** - read this first!

Defines:
- Standard Cartesian coordinate system (NOT inverted Y)
- Grid dimensions (5000×5000)
- Angular conventions (0° = East, 90° = North, etc.)
- Boundary definitions
- Rendering considerations (Pygame Y-inversion)

**Reference this when**: Positioning objects, calculating movement, implementing collision detection, rendering to screen.

### 2. [Context Transitions](context_transitions.md)
**How navigation contexts connect**

Defines:
- Entering/exiting child contexts (push/pop)
- Coordinate space transformations
- Ship positioning on transitions
- Exit positioning algorithms
- Inner/outer system special cases

**Reference this when**: Implementing boundary collisions, entering subsystems, returning to parent contexts.

### 3. [Proximity and Orbit](proximity_and_orbit.md)
**Planet interactions**

Defines:
- Proximity detection vs. orbit entry
- Pause-and-prompt behavior
- Slingshot mechanics
- Orbit state transitions
- Input handling during proximity

**Reference this when**: Implementing planet collision, orbit entry/exit, proximity pause system.

---

## Other Technical Documents

### [State Architecture](state_architecture.md)
Game state pattern, state manager, how states transition.

### [Game Overview](game_overview.md)
High-level technical overview of the entire system.

### [Data Loader Usage](data_loader_usage.md)
How to load JSON data files using DataLoader.

### [Input Manager Usage](input_manager_usage.md)
Input handling system and key mappings.

### [Colors Usage](colors_usage.md)
Color constants and palette definitions.

---

## Design Documents That Reference Technical Docs

These design documents should reference the core technical docs above:

- **[Navigation Context Framework](../design/navigation_context_framework.md)**: Should reference `coordinate_systems.md` and `context_transitions.md`
- **[Space Navigation State](../design/states/space_navigation.md)**: Should reference all three core technical docs
- **[Orbit State](../design/states/orbit.md)**: Should reference `proximity_and_orbit.md`

---

## Document Maintenance

When updating these documents:

1. **Core technical docs** (coordinate_systems, context_transitions, proximity_and_orbit):
   - These are single sources of truth
   - Changes here may require updates to referencing docs
   - Update version/date at top of file when changed

2. **Referencing docs**:
   - Should NOT duplicate information from core docs
   - Should link to core docs for detailed info
   - Can provide context-specific applications of core concepts

3. **Extracting duplicate info**:
   - If you find coordinate system details in another doc, move them to `coordinate_systems.md`
   - Replace with a reference: "See [Coordinate Systems](../technical/coordinate_systems.md) for details"

---

## Quick Reference

| I need to... | Read this doc |
|-------------|---------------|
| Understand the coordinate system | [Coordinate Systems](coordinate_systems.md) |
| Position objects in the grid | [Coordinate Systems](coordinate_systems.md) |
| Handle boundary collisions | [Context Transitions](context_transitions.md) |
| Enter/exit gas giant subsystems | [Context Transitions](context_transitions.md) |
| Implement planet proximity | [Proximity and Orbit](proximity_and_orbit.md) |
| Handle orbit entry/exit | [Proximity and Orbit](proximity_and_orbit.md) |
| Understand game states | [State Architecture](state_architecture.md) |
| Load data files | [Data Loader Usage](data_loader_usage.md) |
