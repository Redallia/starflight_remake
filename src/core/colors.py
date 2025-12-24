"""
Centralized color palette for Starflight Remake

All UI colors defined in one place for consistency and easy tweaking.
Colors are defined as RGB tuples for use with pygame.
"""

# =============================================================================
# Background Colors
# =============================================================================
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
SPACE_BLACK = (5, 5, 15)  # Slightly blue-tinted black for space backgrounds

# =============================================================================
# UI Text Colors
# =============================================================================
TEXT_NORMAL = (200, 200, 200)      # Default text color
TEXT_HIGHLIGHT = (255, 255, 100)   # Selected/highlighted text (yellow)
TEXT_DISABLED = (100, 100, 100)    # Grayed out text
TEXT_TITLE = (255, 255, 255)       # Title text (white)
TEXT_WARNING = (255, 165, 0)       # Warning text (orange)
TEXT_ERROR = (255, 50, 50)         # Error text (red)
TEXT_SUCCESS = (100, 255, 100)     # Success text (green)

# =============================================================================
# HUD Colors (for game UI panels)
# =============================================================================
HUD_BORDER = (60, 120, 180)        # Blue border for UI panels
HUD_BACKGROUND = (20, 20, 40)      # Dark blue background for panels
HUD_DIVIDER = (80, 100, 120)       # Divider lines between sections

# =============================================================================
# Message Log Colors
# =============================================================================
MESSAGE_LOG_BG = (20, 20, 40)      # Background for message log
MESSAGE_NORMAL = (180, 180, 180)   # Normal message text
MESSAGE_IMPORTANT = (255, 255, 100) # Important notifications
MESSAGE_SYSTEM = (100, 200, 255)   # System messages

# =============================================================================
# Ship Status Colors
# =============================================================================
STATUS_HEALTHY = (0, 255, 0)       # Green - system operating normally
STATUS_DAMAGED = (255, 255, 0)     # Yellow - system damaged
STATUS_CRITICAL = (255, 0, 0)      # Red - system critical/failing
STATUS_OFFLINE = (100, 100, 100)   # Gray - system offline

# =============================================================================
# Fuel Gauge Colors
# =============================================================================
FUEL_FULL = (0, 255, 0)            # Green - plenty of fuel
FUEL_MEDIUM = (255, 255, 0)        # Yellow - running low
FUEL_LOW = (255, 165, 0)           # Orange - very low
FUEL_CRITICAL = (255, 0, 0)        # Red - almost empty

# =============================================================================
# Crew Health Colors
# =============================================================================
HEALTH_FULL = (0, 255, 0)          # Green - full health
HEALTH_INJURED = (255, 165, 0)     # Orange - injured
HEALTH_CRITICAL = (255, 0, 0)      # Red - critical condition
HEALTH_DEAD = (100, 100, 100)      # Gray - deceased

# =============================================================================
# Map/Navigation Colors
# =============================================================================
MAP_BACKGROUND = (10, 10, 30)      # Dark blue-black for star maps
MAP_GRID = (40, 60, 80)            # Grid lines
MAP_STAR = (255, 255, 200)         # Star icons (yellow-white)
MAP_PLANET = (100, 150, 200)       # Planet icons (blue)
MAP_SHIP = (255, 255, 100)         # Player ship (yellow)
MAP_NEBULA = (150, 100, 255)       # Nebula regions (purple)
MAP_FLUX = (255, 100, 255)         # Flux points (magenta)

# =============================================================================
# Planetary Surface Colors
# =============================================================================
TERRAIN_WATER = (50, 100, 200)     # Ocean/water
TERRAIN_LAND = (100, 150, 80)      # Land/ground
TERRAIN_MOUNTAIN = (120, 100, 80)  # Mountains
TERRAIN_ICE = (200, 220, 255)      # Ice/snow
TERRAIN_LAVA = (255, 100, 0)       # Lava/molten
TERRAIN_DESERT = (200, 180, 120)   # Desert sand

# =============================================================================
# Scan/Analysis Colors
# =============================================================================
SCAN_MINERAL = (255, 215, 0)       # Gold - mineral deposits
SCAN_FLORA = (100, 255, 100)       # Green - plant life
SCAN_FAUNA = (255, 150, 100)       # Orange - animal life
SCAN_RUIN = (180, 100, 255)        # Purple - ancient ruins
SCAN_SETTLEMENT = (100, 200, 255)  # Blue - alien settlements

# =============================================================================
# Faction/Relationship Colors
# =============================================================================
FACTION_ALLIED = (0, 255, 0)       # Green - friendly
FACTION_NEUTRAL = (200, 200, 200)  # Gray - neutral
FACTION_UNFRIENDLY = (255, 165, 0) # Orange - unfriendly
FACTION_HOSTILE = (255, 0, 0)      # Red - hostile

# =============================================================================
# Menu/Selection Colors
# =============================================================================
MENU_BACKGROUND = BLACK
MENU_TEXT = TEXT_NORMAL
MENU_SELECTED = TEXT_HIGHLIGHT
MENU_DISABLED = TEXT_DISABLED
MENU_TITLE = TEXT_TITLE

# =============================================================================
# Combat Colors (for future use)
# =============================================================================
WEAPON_BEAM = (255, 0, 0)          # Red laser beams
WEAPON_MISSILE = (255, 165, 0)     # Orange missiles
SHIELD_ACTIVE = (100, 200, 255)    # Blue shield glow
EXPLOSION = (255, 100, 0)          # Orange explosion

# =============================================================================
# Utility Functions
# =============================================================================

def lerp_color(color1, color2, t):
    """
    Linear interpolation between two colors

    Args:
        color1: Starting color (R, G, B)
        color2: Ending color (R, G, B)
        t: Interpolation factor (0.0 to 1.0)

    Returns:
        tuple: Interpolated color (R, G, B)

    Example:
        # Get color halfway between green and red
        mid_color = lerp_color(FUEL_FULL, FUEL_CRITICAL, 0.5)
    """
    t = max(0.0, min(1.0, t))  # Clamp t to [0, 1]
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)


def get_fuel_color(fuel_percentage):
    """
    Get appropriate color for fuel level

    Args:
        fuel_percentage: Fuel level from 0.0 to 1.0

    Returns:
        tuple: RGB color appropriate for fuel level
    """
    if fuel_percentage > 0.75:
        return FUEL_FULL
    elif fuel_percentage > 0.50:
        return FUEL_MEDIUM
    elif fuel_percentage > 0.25:
        return FUEL_LOW
    else:
        return FUEL_CRITICAL


def get_health_color(health_percentage):
    """
    Get appropriate color for health level

    Args:
        health_percentage: Health level from 0.0 to 1.0

    Returns:
        tuple: RGB color appropriate for health level
    """
    if health_percentage <= 0:
        return HEALTH_DEAD
    elif health_percentage < 0.25:
        return HEALTH_CRITICAL
    elif health_percentage < 0.75:
        return HEALTH_INJURED
    else:
        return HEALTH_FULL
