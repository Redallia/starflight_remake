"""
Game-wide constants for Starflight Remake

All numerical constants, grid sizes, and configuration values in one place.
"""

# =============================================================================
# Display Settings
# =============================================================================
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
FPS = 60

# =============================================================================
# Context Types
# Based on game_state_specifications.md
# =============================================================================

# Game modes (top level)
GAME_MODE_MAIN_MENU = "main_menu"
GAME_MODE_PLAYING = "playing"
GAME_MODE_GAME_OVER = "game_over"

# Spatial context types (for context stack)
CONTEXT_HYPERSPACE = "hyperspace"
CONTEXT_LOCAL_SPACE = "local_space"
CONTEXT_ORBIT = "orbit"
CONTEXT_SURFACE = "surface"
CONTEXT_DOCKED = "docked"

# =============================================================================
# Orbital System Constants
# =============================================================================

# Context grid dimensions (all navigation contexts use the same grid)
CONTEXT_GRID_SIZE = 500
CONTEXT_CENTER = 250  # Center point (250, 250) for orbital calculations

# Standard orbital radii (used for all system contexts)
# Planets/moons are placed at these distances from the central object
SYSTEM_ORBITS = [80, 120, 160, 200]  # 4 orbital slots

# Central object sizes (visual radius for rendering)
CENTRAL_OBJECT_SIZE = 30  # Size of star, inner system zone, gas giant at center
# =============================================================================
# 
# =============================================================================

# Local Space Regions
REGION_INNER_SYSTEM = "inner_system"
REGION_OUTER_SYSTEM = "outer_system"
REGION_GAS_GIANT = "gas_giant"

# Special locations
LOCATION_STARPORT = "starport"

# Body types (for LOCAL_SPACE context)
BODY_TYPE_STAR = "star"
BODY_TYPE_PLANET = "planet"
BODY_TYPE_MOON = "moon"
BODY_TYPE_GAS_GIANT = "gas_giant"
BODY_TYPE_ASTEROID = "asteroid"
BODY_TYPE_STATION = "station"

# =============================================================================
# Planet Types
# Based on planet_types.json
# =============================================================================
PLANET_TYPE_CRATERED = "cratered"
PLANET_TYPE_MOLTEN = "molten"
PLANET_TYPE_OCEAN = "ocean"
PLANET_TYPE_ROCKY = "rocky"
PLANET_TYPE_FROZEN = "frozen"
PLANET_TYPE_GAS_GIANT = "gas_giant"
PLANET_TYPE_ICE_GIANT = "ice_giant"

# =============================================================================
# Spectral Classes (for stars)
# Based on stellar_classes.json
# =============================================================================
SPECTRAL_CLASS_O = "O"  # Blue giants
SPECTRAL_CLASS_B = "B"  # Hot blue
SPECTRAL_CLASS_A = "A"  # White
SPECTRAL_CLASS_F = "F"  # Yellow-white
SPECTRAL_CLASS_G = "G"  # Yellow (Sol-like)
SPECTRAL_CLASS_K = "K"  # Orange
SPECTRAL_CLASS_M = "M"  # Red dwarf

# =============================================================================
# Ship Systems
# =============================================================================

# Default Ship roles
ROLE_CAPTAIN = "captain"
ROLE_SCIENCE_OFFICER = "science_officer"
ROLE_NAVIGATOR = "navigator"
ROLE_ENGINEER = "engineer"
ROLE_COMMUNICATIONS = "communications"
ROLE_DOCTOR = "doctor"