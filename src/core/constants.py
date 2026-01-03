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

# Spatial context types (spatial zones where you can move)
CONTEXT_HYPERSPACE = "hyperspace"
CONTEXT_OUTER_SYSTEM = "outer_system"
CONTEXT_INNER_SYSTEM = "inner_system"
CONTEXT_PLANETARY_SYSTEM = "planetary_system" # Any planet with moons
CONTEXT_SURFACE = "surface" # Any surface that the ship can land on
CONTEXT_ENCOUNTER = "encounter" # Future: Alien encounters

# Interaction Target Types (objects you can interact with)
INTERACTION_PLANET = "planet"
INTERACTION_MOON = "moon"
INTERACTION_ASTEROID = "asteroid"
INTERACTION_STATION = "station"

# =============================================================================
# Orbital System Constants
# =============================================================================

# Context grid dimensions (all navigation contexts use the same grid)
CONTEXT_GRID_SIZE = 100.0  # 100 units across (scaled down from 5000)
CONTEXT_CENTER = 50.0  # Center point (50, 50) for orbital calculations

# Standard orbital radii (used for all system contexts)
# Planets/moons are placed at these distances from the central object
SYSTEM_ORBITS = [16.0, 24.0, 32.0, 40.0]  # 4 orbital slots
# Central object sizes (visual radius for rendering)
CENTRAL_OBJECT_SIZE = 6.0  # Size of star, inner system zone, gas giant at center

# Movement and spacing
BOUNDARY_INSET = 1.0  # Distance from boundary to prevent immediate re-trigger
BOUNDARY_CLEARANCE = 0.11  # Distance to place ship outside boundary on exit
MOVEMENT_SPEED = 0.25  # Units per keypress (~8 presses to cross 1 unit)

# Rendering scale (separates game logic from visual presentation)
RENDER_SCALE = 100.0  # How many pixels per game unit (1 unit = 8 pixels)
# =============================================================================

# Local Space Regions (Kept for repurposing reason)
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