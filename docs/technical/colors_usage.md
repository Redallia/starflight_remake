# Colors Module Usage Guide

## Overview
All game colors are centralized in `src/core/colors.py` for consistency and easy tweaking. This prevents magic numbers scattered throughout the codebase.

## Basic Usage

```python
from core.colors import TEXT_NORMAL, TEXT_HIGHLIGHT, BLACK

# Use in pygame rendering
surface.fill(BLACK)
text = font.render("Hello", True, TEXT_NORMAL)
highlight_text = font.render("Selected", True, TEXT_HIGHLIGHT)
```

## Color Categories

### Background Colors
- `BLACK` - Pure black (0, 0, 0)
- `DARK_GRAY` - Dark gray (40, 40, 40)
- `SPACE_BLACK` - Slightly blue-tinted black for space (5, 5, 15)

### UI Text
- `TEXT_NORMAL` - Default text (200, 200, 200)
- `TEXT_HIGHLIGHT` - Selected/highlighted (255, 255, 100) - Yellow
- `TEXT_DISABLED` - Grayed out (100, 100, 100)
- `TEXT_TITLE` - Title text (255, 255, 255) - White
- `TEXT_WARNING` - Warnings (255, 165, 0) - Orange
- `TEXT_ERROR` - Errors (255, 50, 50) - Red
- `TEXT_SUCCESS` - Success messages (100, 255, 100) - Green

### Menu (Aliases for convenience)
- `MENU_TEXT` = `TEXT_NORMAL`
- `MENU_SELECTED` = `TEXT_HIGHLIGHT`
- `MENU_DISABLED` = `TEXT_DISABLED`
- `MENU_TITLE` = `TEXT_TITLE`
- `MENU_BACKGROUND` = `BLACK`

### HUD/Panels
- `HUD_BORDER` - Panel borders (60, 120, 180) - Blue
- `HUD_BACKGROUND` - Panel backgrounds (20, 20, 40) - Dark blue
- `HUD_DIVIDER` - Section dividers (80, 100, 120)

### Ship Status
- `STATUS_HEALTHY` - Green (0, 255, 0)
- `STATUS_DAMAGED` - Yellow (255, 255, 0)
- `STATUS_CRITICAL` - Red (255, 0, 0)
- `STATUS_OFFLINE` - Gray (100, 100, 100)

### Fuel Gauge
- `FUEL_FULL` - Green
- `FUEL_MEDIUM` - Yellow
- `FUEL_LOW` - Orange
- `FUEL_CRITICAL` - Red

### Health
- `HEALTH_FULL` - Green
- `HEALTH_INJURED` - Orange
- `HEALTH_CRITICAL` - Red
- `HEALTH_DEAD` - Gray

### Map/Navigation
- `MAP_BACKGROUND` - Dark space (10, 10, 30)
- `MAP_GRID` - Grid lines (40, 60, 80)
- `MAP_STAR` - Star icons (255, 255, 200) - Yellow-white
- `MAP_PLANET` - Planets (100, 150, 200) - Blue
- `MAP_SHIP` - Player ship (255, 255, 100) - Yellow
- `MAP_NEBULA` - Nebulae (150, 100, 255) - Purple
- `MAP_FLUX` - Flux points (255, 100, 255) - Magenta

### Terrain
- `TERRAIN_WATER` - Ocean (50, 100, 200)
- `TERRAIN_LAND` - Ground (100, 150, 80)
- `TERRAIN_MOUNTAIN` - Mountains (120, 100, 80)
- `TERRAIN_ICE` - Ice/snow (200, 220, 255)
- `TERRAIN_LAVA` - Lava (255, 100, 0)
- `TERRAIN_DESERT` - Desert (200, 180, 120)

### Scans
- `SCAN_MINERAL` - Gold (255, 215, 0)
- `SCAN_FLORA` - Green (100, 255, 100)
- `SCAN_FAUNA` - Orange (255, 150, 100)
- `SCAN_RUIN` - Purple (180, 100, 255)
- `SCAN_SETTLEMENT` - Blue (100, 200, 255)

### Factions
- `FACTION_ALLIED` - Green (0, 255, 0)
- `FACTION_NEUTRAL` - Gray (200, 200, 200)
- `FACTION_UNFRIENDLY` - Orange (255, 165, 0)
- `FACTION_HOSTILE` - Red (255, 0, 0)

## Utility Functions

### `lerp_color(color1, color2, t)`
Linear interpolation between two colors

```python
from core.colors import lerp_color, FUEL_FULL, FUEL_CRITICAL

# Gradually transition from green to red
fuel_percentage = 0.3  # 30% fuel
t = 1.0 - fuel_percentage  # 0.7 (closer to red)
fuel_color = lerp_color(FUEL_FULL, FUEL_CRITICAL, t)
```

### `get_fuel_color(fuel_percentage)`
Get appropriate color for fuel level (0.0 to 1.0)

```python
from core.colors import get_fuel_color

current_fuel = 450
max_fuel = 1000
fuel_color = get_fuel_color(current_fuel / max_fuel)
# Returns FUEL_MEDIUM (yellow) for 45%
```

**Ranges:**
- > 75% → `FUEL_FULL` (green)
- 50-75% → `FUEL_MEDIUM` (yellow)
- 25-50% → `FUEL_LOW` (orange)
- < 25% → `FUEL_CRITICAL` (red)

### `get_health_color(health_percentage)`
Get appropriate color for health level (0.0 to 1.0)

```python
from core.colors import get_health_color

health_color = get_health_color(crew_member.health / crew_member.max_health)
```

**Ranges:**
- 0% → `HEALTH_DEAD` (gray)
- 1-24% → `HEALTH_CRITICAL` (red)
- 25-74% → `HEALTH_INJURED` (orange)
- 75-100% → `HEALTH_FULL` (green)

## Examples

### Rendering a Health Bar
```python
from core.colors import get_health_color, DARK_GRAY

def render_health_bar(surface, x, y, width, height, current_hp, max_hp):
    # Background
    pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height))

    # Foreground (health)
    health_pct = current_hp / max_hp
    health_width = int(width * health_pct)
    health_color = get_health_color(health_pct)
    pygame.draw.rect(surface, health_color, (x, y, health_width, height))
```

### Status Indicator
```python
from core.colors import STATUS_HEALTHY, STATUS_DAMAGED, STATUS_CRITICAL

def get_system_color(damage_level):
    if damage_level == 0:
        return STATUS_HEALTHY
    elif damage_level < 50:
        return STATUS_DAMAGED
    else:
        return STATUS_CRITICAL
```

### Faction Name Display
```python
from core.colors import FACTION_ALLIED, FACTION_NEUTRAL, FACTION_HOSTILE

def render_faction_name(faction, standing):
    if standing >= 75:
        color = FACTION_ALLIED
    elif standing >= 25:
        color = FACTION_NEUTRAL
    else:
        color = FACTION_HOSTILE

    return font.render(faction.name, True, color)
```

## Modifying the Palette

To change the game's color scheme, edit `src/core/colors.py`. All UI will automatically update.

**Example - Make menus more blue-tinted:**
```python
# In colors.py
MENU_TEXT = (180, 180, 255)       # Slightly blue instead of gray
MENU_SELECTED = (100, 200, 255)   # Blue instead of yellow
```

All menus across the game will immediately use the new colors.
