"""
Sensor data generation system for planetary scanning
Generates consistent, deterministic sensor readings using planet seeds
"""
from dataclasses import dataclass
from typing import List
import random


@dataclass
class SensorData:
    """Container for planetary sensor scan results"""
    mass: int  # Mass in tons
    bio_density: float  # Biological density 0-100%
    mineral_density: float  # Mineral density 0-100%
    atmosphere: List[str]  # Atmospheric components in order of abundance
    hydrosphere: List[str]  # Liquid surface components
    lithosphere: List[str]  # Mineral composition


# Mineral types (from original Starflight)
MINERALS = [
    "Lead", "Iron", "Cobalt", "Nickel", "Copper", "Zinc", "Molybdenum",
    "Tin", "Magnesium", "Aluminum", "Titanium", "Chromium", "Antimony",
    "Promethium", "Mercury", "Tungsten", "Silver", "Gold", "Platinum",
    "Plutonium", "Rodnium"
]

# Atmospheric gases
ATMOSPHERIC_GASES = [
    "Nitrogen", "Oxygen", "Carbon Dioxide", "Argon", "Helium", "Hydrogen",
    "Methane", "Ammonia", "Water Vapor", "Sulfur Dioxide", "Chlorine", "Neon"
]

# Hydrospheric liquids
HYDROSPHERE_LIQUIDS = [
    "Water", "Ice", "Salt Water", "Methane", "Ammonia", "Liquid Nitrogen",
    "Liquid Hydrogen", "Sulfuric Acid", "Molten Rock"
]


# Planet type templates
PLANET_TEMPLATES = {
    "magma": {
        "atmosphere_pool": ["Carbon Dioxide", "Sulfur Dioxide", "Nitrogen", "Argon", "Water Vapor"],
        "atmosphere_weights": [3, 2, 1, 1, 1],  # CO2 and SO2 more likely
        "hydrosphere_pool": ["Molten Rock", "Sulfuric Acid", "Water"],
        "hydrosphere_weights": [4, 2, 1],
        "mass_range": (100_000_000, 600_000_000),  # Medium rocky mass
        "bio_modifier": 0.05,  # Very low life
        "bio_base": 2.0,  # Base bio percentage before modifiers
        "typical_minerals": ["Iron", "Magnesium", "Titanium", "Tungsten", "Platinum", "Chromium"],
    },
    "rocky": {
        "atmosphere_pool": ["Nitrogen", "Oxygen", "Carbon Dioxide", "Argon", "Water Vapor", "Neon"],
        "atmosphere_weights": [3, 2, 2, 1, 1, 1],  # Earth-like distribution
        "hydrosphere_pool": ["Water", "Ice", "Salt Water"],
        "hydrosphere_weights": [3, 1, 2],
        "mass_range": (200_000_000, 1_000_000_000),  # Earth-like
        "bio_modifier": 1.0,  # Normal life potential
        "bio_base": 20.0,
        "typical_minerals": ["Iron", "Copper", "Nickel", "Aluminum", "Zinc", "Lead", "Silver", "Gold"],
    },
    "liquid": {
        "atmosphere_pool": ["Nitrogen", "Oxygen", "Water Vapor", "Argon", "Carbon Dioxide"],
        "atmosphere_weights": [3, 2, 2, 1, 1],
        "hydrosphere_pool": ["Water", "Salt Water", "Ice"],
        "hydrosphere_weights": [4, 3, 1],
        "mass_range": (300_000_000, 1_200_000_000),  # Slightly larger than rocky
        "bio_modifier": 1.5,  # High life potential
        "bio_base": 40.0,
        "typical_minerals": ["Magnesium", "Aluminum", "Cobalt", "Tin", "Nickel"],
    },
    "frozen": {
        "atmosphere_pool": ["Nitrogen", "Argon", "Methane", "Neon", "Helium"],
        "atmosphere_weights": [3, 2, 2, 1, 1],
        "hydrosphere_pool": ["Ice", "Frozen Nitrogen", "Frozen Methane", "Ammonia"],
        "hydrosphere_weights": [4, 2, 2, 1],
        "mass_range": (50_000_000, 500_000_000),  # Smaller, lower density
        "bio_modifier": 0.2,  # Very low life
        "bio_base": 5.0,
        "typical_minerals": ["Platinum", "Plutonium", "Antimony", "Mercury", "Rodnium"],
    },
    "gas_giant": {
        "atmosphere_pool": ["Hydrogen", "Helium", "Methane", "Ammonia", "Water Vapor"],
        "atmosphere_weights": [5, 4, 2, 1, 1],  # Dominated by H and He
        "hydrosphere_pool": ["Liquid Hydrogen", "Liquid Helium", "Ammonia"],
        "hydrosphere_weights": [4, 3, 1],
        "mass_range": (10_000_000_000, 100_000_000_000),  # Massive
        "bio_modifier": 0.0,  # No life
        "bio_base": 0.0,
        "typical_minerals": [],  # No accessible surface minerals
    }
}


def generate_sensor_data(planet: dict) -> SensorData:
    """
    Generate sensor data for a planet using its seed for deterministic results

    Args:
        planet: Planet dictionary with seed, type, and terrain_params

    Returns:
        SensorData object with all scan results
    """
    seed = planet.get('seed', 0)
    planet_type = planet.get('type', 'rocky')
    terrain_params = planet.get('terrain_params', {})

    # Get template for this planet type
    template = PLANET_TEMPLATES.get(planet_type, PLANET_TEMPLATES['rocky'])

    # Create seeded random generator for deterministic results
    rng = random.Random(seed)

    # Generate mass
    mass = int(rng.uniform(*template['mass_range']))

    # Generate bio density
    bio_density = _calculate_bio_density(terrain_params, template, rng)

    # Generate mineral density
    mineral_density = _calculate_mineral_density(terrain_params, rng)

    # Generate atmosphere composition
    atmosphere = _generate_atmosphere(template, rng)

    # Generate hydrosphere composition
    hydrosphere = _generate_hydrosphere(terrain_params, template, rng)

    # Generate lithosphere (minerals)
    lithosphere = _generate_lithosphere(template, rng)

    return SensorData(
        mass=mass,
        bio_density=bio_density,
        mineral_density=mineral_density,
        atmosphere=atmosphere,
        hydrosphere=hydrosphere,
        lithosphere=lithosphere
    )


def _calculate_bio_density(terrain_params: dict, template: dict, rng: random.Random) -> float:
    """Calculate biological density based on planet conditions"""
    # Start with template base
    bio = template['bio_base']

    # Apply type modifier
    bio *= template['bio_modifier']

    # Water coverage increases bio potential
    water_coverage = terrain_params.get('water_coverage', 0.3)
    bio *= (0.5 + water_coverage)

    # Temperature affects bio (optimal around 0.4-0.6)
    temperature = terrain_params.get('temperature', 0.5)
    temp_factor = 1.0 - abs(temperature - 0.5) * 1.5
    temp_factor = max(0.1, temp_factor)
    bio *= temp_factor

    # Add some random variation
    bio += rng.uniform(-10, 10)

    # Clamp to 0-100
    return max(0.0, min(100.0, bio))


def _calculate_mineral_density(terrain_params: dict, rng: random.Random) -> float:
    """Calculate mineral density based on planet parameters"""
    # Base from terrain params
    mineral_richness = terrain_params.get('mineral_richness', 0.5)
    mineral_density = mineral_richness * 100

    # Add random variation
    mineral_density += rng.uniform(-15, 15)

    # Clamp to 0-100
    return max(0.0, min(100.0, mineral_density))


def _generate_atmosphere(template: dict, rng: random.Random) -> List[str]:
    """Generate atmospheric composition using weighted selection"""
    pool = template['atmosphere_pool']
    weights = template['atmosphere_weights']

    # Select 2-4 components
    num_components = rng.randint(2, 4)
    num_components = min(num_components, len(pool))

    # Weighted selection without replacement
    selected = []
    available_pool = list(pool)
    available_weights = list(weights)

    for _ in range(num_components):
        # Weighted random choice
        component = rng.choices(available_pool, weights=available_weights, k=1)[0]
        selected.append(component)

        # Remove from pool
        idx = available_pool.index(component)
        available_pool.pop(idx)
        available_weights.pop(idx)

    return selected


def _generate_hydrosphere(terrain_params: dict, template: dict, rng: random.Random) -> List[str]:
    """Generate hydrosphere composition based on water coverage"""
    water_coverage = terrain_params.get('water_coverage', 0.3)

    # If very low water coverage, return minimal or no hydrosphere
    if water_coverage < 0.1:
        return ["None"]

    pool = template['hydrosphere_pool']
    weights = template['hydrosphere_weights']

    # More water = more components
    if water_coverage > 0.7:
        num_components = rng.randint(2, 3)
    elif water_coverage > 0.4:
        num_components = rng.randint(1, 2)
    else:
        num_components = 1

    num_components = min(num_components, len(pool))

    # Weighted selection without replacement
    selected = []
    available_pool = list(pool)
    available_weights = list(weights)

    for _ in range(num_components):
        component = rng.choices(available_pool, weights=available_weights, k=1)[0]
        selected.append(component)

        idx = available_pool.index(component)
        available_pool.pop(idx)
        available_weights.pop(idx)

    return selected


def _generate_lithosphere(template: dict, rng: random.Random) -> List[str]:
    """Generate mineral composition from template's typical minerals"""
    typical_minerals = template['typical_minerals']

    # Gas giants have no accessible minerals
    if not typical_minerals:
        return ["None"]

    # Select 3-6 minerals from typical set
    num_minerals = rng.randint(3, 6)
    num_minerals = min(num_minerals, len(typical_minerals))

    # Random selection from typical minerals
    selected = rng.sample(typical_minerals, num_minerals)

    # Occasionally add a rare mineral from the full pool
    if rng.random() < 0.3:  # 30% chance
        rare_minerals = [m for m in MINERALS if m not in selected]
        if rare_minerals:
            selected.append(rng.choice(rare_minerals))

    return selected
