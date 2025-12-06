# Planet Generation System

## Overview

The planet generation system creates procedural planetary data for exploration in the Starflight remake. It uses a seed-based approach to ensure consistent, deterministic generation while avoiding hand-crafted data for each planet.

## Architecture

### Components

1. **Planet Data Storage** (`src/data/star_systems.json`)
   - Stores base planet configuration
   - Includes seed for procedural generation
   - Defines terrain parameters

2. **Terrain Generation** (`src/core/terrain_generator.py`)
   - Generates surface terrain using Perlin noise
   - Creates elevation, moisture, and mineral maps
   - Uses planet seed for deterministic results

3. **Sensor Data Generation** (`src/core/sensor_data_generator.py`) *(To be implemented)*
   - Generates atmospheric, hydrospheric, and lithospheric composition
   - Calculates planet mass and density metrics
   - Uses planet seed and terrain params for consistency

## Planet Types

The system supports five world types based on the original Starflight classification:

- **Magma**: Volcanic, high temperature, molten surface areas
- **Rocky**: Earth-like terrestrial worlds with solid surfaces
- **Liquid**: Water-dominated worlds, high hydrosphere coverage
- **Frozen**: Ice worlds, low temperature, frozen volatiles
- **Gas Giant**: Massive atmospheric planets, no solid surface

### Extensibility

The planet type system is designed to be extensible. New types can be added by:
1. Adding new type templates to `PLANET_TEMPLATES` dictionary
2. Defining appropriate composition pools and generation parameters
3. No changes to core generation logic required

## Planet Data Structure

Each planet in `star_systems.json` contains:

```json
{
  "name": "Planet Name",
  "coord_x": 15,
  "coord_y": 35,
  "radius": 4,
  "color": [80, 150, 220],
  "type": "rocky",
  "seed": 2001,
  "terrain_params": {
    "has_surface": true,
    "water_coverage": 0.6,
    "elevation_scale": 0.3,
    "temperature": 0.5,
    "mineral_richness": 0.3
  }
}
```

### Key Fields

- **seed**: Random seed for all procedural generation (terrain, sensor data)
- **type**: Planet classification (magma, rocky, liquid, frozen, gas_giant)
- **terrain_params**: Parameters influencing generation algorithms
  - `has_surface`: Whether planet can be landed on
  - `water_coverage`: Percentage of surface covered by liquids (0.0-1.0)
  - `elevation_scale`: Terrain roughness factor
  - `temperature`: Temperature level (0.0 = frozen, 1.0 = hot)
  - `mineral_richness`: Mineral deposit density (0.0-1.0)

## Sensor Data Generation

### Overview

When the Science Officer activates sensors while in orbit, the system generates comprehensive planetary data. This data is deterministic (same planet always produces same readings) and derived from the planet's seed and terrain parameters.

### Generated Data

**Numerical Metrics (Auxiliary View Display):**
- **Mass**: Planet mass in tons (derived from type and size)
- **Bio**: Biological density percentage (0-100%)
- **Min**: Mineral density percentage (0-100%)

**Composition Data (Text Display):**
- **Atmosphere**: Gaseous components in decreasing order of abundance
- **Hydrosphere**: Liquid surface components
- **Lithosphere**: Mineral composition of planetary crust

### Generation Algorithm

The sensor data generator uses a template-based approach:

1. **Select Template**: Choose generation parameters based on planet type
2. **Initialize RNG**: Create seeded random generator using planet seed
3. **Calculate Metrics**:
   - Mass: Random value within type-appropriate range
   - Bio: Based on water coverage, temperature, and type modifier
   - Min: Based on mineral_richness parameter with variation
4. **Select Compositions**:
   - Atmosphere: 2-4 components from type-appropriate pool
   - Hydrosphere: 1-3 components based on water_coverage
   - Lithosphere: Minerals present in generated terrain or from pool

### Mineral Types

The system uses real mineral names from the original Starflight:

- Lead
- Iron
- Cobalt
- Nickel
- Copper
- Zinc
- Molybdenum
- Tin
- Magnesium
- Aluminum
- Titanium
- Chromium
- Antimony
- Promethium
- Mercury
- Tungsten
- Silver
- Gold
- Platinum
- Plutonium
- Rodnium

### Atmospheric Components

A fixed pool of realistic atmospheric gases:
- Nitrogen
- Oxygen
- Carbon Dioxide
- Argon
- Helium
- Hydrogen
- Methane
- Ammonia
- Water Vapor
- Sulfur Dioxide
- Chlorine
- Neon

### Hydrospheric Components

Liquid surface materials:
- Water
- Ice
- Salt Water
- Methane
- Ammonia
- Liquid Nitrogen
- Liquid Hydrogen
- Sulfuric Acid
- Molten Rock (magma worlds)

## Planet Type Templates

Each planet type has associated generation parameters:

### Example Template Structure

```python
{
    "type_name": {
        "atmosphere_pool": ["Gas1", "Gas2", ...],
        "hydrosphere_pool": ["Liquid1", "Liquid2", ...],
        "mass_range": (min_tons, max_tons),
        "bio_modifier": 0.0-2.0,
        "typical_minerals": ["Mineral1", "Mineral2", ...]
    }
}
```

### Type-Specific Characteristics

**Magma Worlds:**
- High temperature, volcanic activity
- Atmosphere: CO2, SO2, dust
- Hydrosphere: Molten rock, minimal liquid water
- Mass: Medium (rocky composition)
- Bio: Very low (0-10%)

**Rocky Worlds:**
- Earth-like terrestrial planets
- Atmosphere: N2, O2, CO2, Ar (varied)
- Hydrosphere: Water, ice (coverage varies)
- Mass: Medium (0.1-2.0 Earth masses)
- Bio: Low to high (0-80%, depends on conditions)

**Liquid Worlds:**
- Ocean-dominated surfaces
- Atmosphere: Water vapor, N2, O2
- Hydrosphere: Water, dissolved minerals
- Mass: Medium to high
- Bio: High (30-90%)

**Frozen Worlds:**
- Low temperature ice worlds
- Atmosphere: Thin, frozen volatiles
- Hydrosphere: Ice, frozen CO2, frozen methane
- Mass: Low to medium
- Bio: Very low (0-15%)

**Gas Giants:**
- Massive atmospheric planets
- Atmosphere: H2, He, CH4, NH3
- Hydrosphere: Liquid hydrogen, liquid helium
- Mass: Very high (50-1000 Earth masses)
- Bio: None (0%)
- Has_surface: False (not landable)

## Data Caching

Sensor data is generated on first scan and cached in game state:

```python
game_state.scanned_planets = {
    "Planet Name": SensorData(...),
    ...
}
```

This ensures:
- Consistent readings across multiple scans
- No regeneration overhead
- Data persists through game session

## Integration Points

### Terrain Generator
- Already generates mineral maps using planet seed
- Lithosphere composition can be derived from actual terrain data
- Ensures sensor readings match surface reality

### Auxiliary View Panel
- Will display Mass/Bio/Min numerical readouts
- Updates when sensor scan completes

### Message Log
- Displays atmospheric, hydrospheric, lithospheric composition
- Shows in order of abundance/importance

### Game State
- Tracks which planets have been scanned
- Stores cached sensor data
- Knows current orbiting planet

## Scientific Realism

The system prioritizes realistic planetary science:

- Gas giants cannot support surface life (bio = 0)
- Atmospheric composition matches planet type and temperature
- Hydrosphere presence depends on temperature and volatiles
- Mineral distribution reflects planetary differentiation
- Mass correlates with planet size and composition

Future expansions may include:
- Exotic life forms in extreme environments
- Specialized research stations at gas giants
- Atmospheric mining opportunities
- More complex biosphere modeling

## Future Enhancements

Potential additions to the system:

1. **Atmospheric Pressure**: Add pressure readings (millibars/atmospheres)
2. **Gravity**: Calculate surface gravity from mass and radius
3. **Radiation Levels**: Solar radiation and magnetosphere data
4. **Anomalies**: Special features (ruins, artifacts, unique formations)
5. **Weather Systems**: Dynamic atmospheric conditions
6. **Seasonal Variations**: Axial tilt and orbital effects
7. **Moon Systems**: Satellite generation for planets
8. **Ring Systems**: Planetary rings for gas giants
9. **Tectonic Activity**: Seismic and volcanic activity metrics
10. **Biosphere Detail**: Species count, ecosystem complexity

## Implementation Status

- [x] Planet data structure defined
- [x] Terrain generation system implemented
- [ ] Sensor data generator module
- [ ] Planet type templates
- [ ] Sensor action handler
- [ ] Auxiliary view integration
- [ ] Message log composition display
- [ ] Scan state caching in game state
