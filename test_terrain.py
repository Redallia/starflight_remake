"""
Test terrain generation consistency
"""
from src.core.terrain_generator import TerrainGenerator, TerrainType

# Test planet data
test_planet = {
    'name': 'Aqua',
    'type': 'water',
    'seed': 2001,
    'terrain_params': {
        'has_surface': True,
        'water_coverage': 0.6,
        'elevation_scale': 0.3,
        'temperature': 0.5,
        'mineral_richness': 0.3
    }
}

print("Testing terrain generation consistency...")
print(f"Planet: {test_planet['name']}, Seed: {test_planet['seed']}")
print()

# Generate terrain twice with same planet data
generator1 = TerrainGenerator(test_planet)
terrain1 = generator1.generate(20, 20)

generator2 = TerrainGenerator(test_planet)
terrain2 = generator2.generate(20, 20)

# Check if they're identical
identical = True
for y in range(20):
    for x in range(20):
        if terrain1[y][x] != terrain2[y][x]:
            identical = False
            break
    if not identical:
        break

print(f"Generation consistency test: {'PASSED' if identical else 'FAILED'}")
print()

# Display a sample of the terrain
print("Sample terrain (10x10 from top-left):")
print("=" * 40)

# Terrain type to character mapping for display
terrain_chars = {
    TerrainType.DEEP_WATER: 'W',
    TerrainType.SHALLOW_WATER: 'w',
    TerrainType.SAND: '.',
    TerrainType.GRASS: '"',
    TerrainType.ROCK: '#',
    TerrainType.MOUNTAIN: '^',
    TerrainType.MINERAL: '$',
}

for y in range(10):
    line = ""
    for x in range(10):
        terrain_type = terrain1[y][x]
        char = terrain_chars.get(terrain_type, '?')
        line += char + " "
    print(line)

print("=" * 40)
print()

# Count terrain types
from collections import Counter
all_terrain = [cell for row in terrain1 for cell in row]
counts = Counter(all_terrain)

print("Terrain distribution (20x20 grid, 400 cells):")
for terrain_type, count in sorted(counts.items()):
    percentage = (count / 400) * 100
    print(f"  {terrain_type:20s}: {count:3d} ({percentage:5.1f}%)")
print()

# Test with different planet
print("\nTesting different planet (different seed)...")
test_planet2 = test_planet.copy()
test_planet2['name'] = 'Typhon'
test_planet2['seed'] = 3001
test_planet2['terrain_params'] = {
    'has_surface': True,
    'water_coverage': 0.2,  # Less water
    'elevation_scale': 0.7,  # More mountainous
    'temperature': 0.3,
    'mineral_richness': 0.5  # More minerals
}

generator3 = TerrainGenerator(test_planet2)
terrain3 = generator3.generate(20, 20)

# Check that different seed produces different terrain
different = False
for y in range(20):
    for x in range(20):
        if terrain1[y][x] != terrain3[y][x]:
            different = True
            break
    if different:
        break

print(f"Different seed produces different terrain: {'PASSED' if different else 'FAILED'}")
print()

print("Sample terrain for Typhon (10x10):")
print("=" * 40)
for y in range(10):
    line = ""
    for x in range(10):
        terrain_type = terrain3[y][x]
        char = terrain_chars.get(terrain_type, '?')
        line += char + " "
    print(line)
print("=" * 40)

# Count terrain types for second planet
all_terrain3 = [cell for row in terrain3 for cell in row]
counts3 = Counter(all_terrain3)

print("\nTerrain distribution for Typhon:")
for terrain_type, count in sorted(counts3.items()):
    percentage = (count / 400) * 100
    print(f"  {terrain_type:20s}: {count:3d} ({percentage:5.1f}%)")
