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
# HUD Layout (Four-Area Standard Layout)
# Based on hud_specification.md
# =============================================================================

# Main View - Left side, large area
MAIN_VIEW_X = 0
MAIN_VIEW_Y = 0
MAIN_VIEW_WIDTH = 500
MAIN_VIEW_HEIGHT = 450

# Auxiliary View - Upper-right corner
AUX_VIEW_X = 500
AUX_VIEW_Y = 0
AUX_VIEW_WIDTH = 300
AUX_VIEW_HEIGHT = 200

# Control Panel - Right side, middle
CONTROL_PANEL_X = 500
CONTROL_PANEL_Y = 200
CONTROL_PANEL_WIDTH = 300
CONTROL_PANEL_HEIGHT = 250

# Message Log - Bottom, full width
MESSAGE_LOG_X = 0
MESSAGE_LOG_Y = 450
MESSAGE_LOG_WIDTH = 800
MESSAGE_LOG_HEIGHT = 150

# =============================================================================
# Coordinate System Sizes
# Based on navigation_specification.md
# =============================================================================

# Hyperspace (sector-level)
HYPERSPACE_GRID_WIDTH = 125  # tiles
HYPERSPACE_GRID_HEIGHT = 110  # tiles
HYPERSPACE_TILE_SIZE = 10  # units per tile
HYPERSPACE_WIDTH = HYPERSPACE_GRID_WIDTH * HYPERSPACE_TILE_SIZE  # 1250 units
HYPERSPACE_HEIGHT = HYPERSPACE_GRID_HEIGHT * HYPERSPACE_TILE_SIZE  # 1100 units

# Planetary Surface (terrain vehicle exploration)
PLANETARY_GRID_WIDTH = 500  # tiles
PLANETARY_GRID_HEIGHT = 200  # tiles
PLANETARY_TILE_SIZE = 10  # units per tile
PLANETARY_SURFACE_WIDTH = PLANETARY_GRID_WIDTH * PLANETARY_TILE_SIZE  # 5000 units
PLANETARY_SURFACE_HEIGHT = PLANETARY_GRID_HEIGHT * PLANETARY_TILE_SIZE  # 2000 units

# Local Space (star systems) - TBD, will vary by system
# These are placeholders until actual values are determined
LOCAL_SPACE_OUTER_SYSTEM_SIZE = 1000  # TBD
LOCAL_SPACE_INNER_SYSTEM_SIZE = 500  # TBD
LOCAL_SPACE_PLANETARY_SYSTEM_SIZE = 200  # TBD

# =============================================================================
# Crew Skills
# Based on species.json
# =============================================================================
SKILL_MIN = 0
SKILL_MAX = 250

# Skill types (for reference)
SKILL_SCIENCE = "science"
SKILL_NAVIGATION = "navigation"
SKILL_ENGINEERING = "engineering"
SKILL_COMMUNICATION = "communication"
SKILL_MEDICINE = "medicine"

# =============================================================================
# Game Balance (Starting Values)
# These are initial estimates - adjust based on playtesting
# =============================================================================
STARTING_CREDITS = 1000
STARTING_FUEL = 500
STARTING_CARGO_CAPACITY = 50

# =============================================================================
# Fuel Consumption
# Based on navigation_specification.md
# =============================================================================

# Fuel cost per coordinate unit in hyperspace (varies by engine class)
FUEL_PER_UNIT_ENGINE_CLASS_1 = 1.0
FUEL_PER_UNIT_ENGINE_CLASS_2 = 0.75
FUEL_PER_UNIT_ENGINE_CLASS_3 = 0.5

# Local space movement (negligible fuel cost)
FUEL_PER_UNIT_LOCAL_SPACE = 0.0

# Surface movement (terrain vehicle)
FUEL_PER_UNIT_FLAT_TERRAIN = 0.5  # TBD
FUEL_PER_UNIT_ELEVATED_TERRAIN = 1.0  # TBD
FUEL_PER_UNIT_MOUNTAIN_TERRAIN = 2.0  # TBD
FUEL_PER_UNIT_LIQUID_TERRAIN = 3.0  # TBD

# =============================================================================
# Ship Systems
# =============================================================================

# Maximum crew roster size
MAX_CREW_SIZE = 6

# Ship roles
ROLE_CAPTAIN = "captain"
ROLE_SCIENCE_OFFICER = "science_officer"
ROLE_NAVIGATOR = "navigator"
ROLE_ENGINEER = "engineer"
ROLE_COMMUNICATIONS = "communications"
ROLE_DOCTOR = "doctor"

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

# Local Space Regions
REGION_INNER_SYSTEM = "inner_system"
REGION_OUTER_SYSTEM = "outer_system"
REGION_GAS_GIANT = "gas_giant"

# Special locations
LOCATION_STARPORT = "starport"

# Sub-states
SUB_STATE_NONE = "none"
SUB_STATE_MANEUVERING = "maneuvering"
SUB_STATE_LANDING_MODE = "landing_mode"
SUB_STATE_SCANNING = "scanning"
SUB_STATE_COMMUNICATIONS = "communications"

# Body types (for LOCAL_SPACE context)
BODY_TYPE_STAR = "star"
BODY_TYPE_PLANET = "planet"
BODY_TYPE_MOON = "moon"
BODY_TYPE_GAS_GIANT = "gas_giant"
BODY_TYPE_ASTEROID = "asteroid"
BODY_TYPE_STATION = "station"

# =============================================================================
# Encounter Types
# =============================================================================
DISPOSITION_HOSTILE = "hostile"
DISPOSITION_NEUTRAL = "neutral"
DISPOSITION_FRIENDLY = "friendly"

# =============================================================================
# Modal Types
# Based on hud_specification.md
# =============================================================================
MODAL_CARGO = "cargo"
MODAL_STARMAP = "starmap"
MODAL_COMMUNICATIONS = "communications"
MODAL_TRADE = "trade"
MODAL_MESSAGES = "messages"
MODAL_SHIP_STATUS = "ship_status"

# =============================================================================
# Planetary Coordinates
# Based on navigation_specification.md - directional notation
# =============================================================================

# Surface coordinates use directional notation centered on (0,0)
# East/West: 250W to 250E (derived from PLANETARY_GRID_WIDTH / 2)
# North/South: 100N to 100S (derived from PLANETARY_GRID_HEIGHT / 2)
PLANETARY_COORD_MAX_EAST = PLANETARY_GRID_WIDTH // 2  # 250E
PLANETARY_COORD_MAX_WEST = PLANETARY_GRID_WIDTH // 2  # 250W
PLANETARY_COORD_MAX_NORTH = PLANETARY_GRID_HEIGHT // 2  # 100N
PLANETARY_COORD_MAX_SOUTH = PLANETARY_GRID_HEIGHT // 2  # 100S

# =============================================================================
# Health and Status Thresholds
# =============================================================================

# Health percentage thresholds for color coding
HEALTH_THRESHOLD_HEALTHY = 0.75  # Above this = healthy (green)
HEALTH_THRESHOLD_INJURED = 0.25  # Below healthy, above this = injured (orange)
# Below injured threshold = critical (red)

# Fuel percentage thresholds for color coding
FUEL_THRESHOLD_FULL = 0.75  # Above this = full (green)
FUEL_THRESHOLD_MEDIUM = 0.50  # Above this = medium (yellow)
FUEL_THRESHOLD_LOW = 0.25  # Above this = low (orange)
# Below low threshold = critical (red)

# =============================================================================
# Terrain Types (for surface exploration)
# =============================================================================
TERRAIN_TYPE_WATER = "water"
TERRAIN_TYPE_LAND = "land"
TERRAIN_TYPE_MOUNTAIN = "mountain"
TERRAIN_TYPE_ICE = "ice"
TERRAIN_TYPE_LAVA = "lava"
TERRAIN_TYPE_DESERT = "desert"

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
