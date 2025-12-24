"""
Centralized data loading utility for Starflight
"""
import json
from pathlib import Path


class DataLoader:
    """
    Handles loading game data from JSON files

    Provides consistent path resolution and error handling for:
    - Static game data (species, ships, planets, etc.)
    - Runtime data (save files, generated systems)
    """

    def __init__(self):
        """Initialize the data loader with the data directory root"""
        # Get the src/data directory relative to this file
        # This file is in src/core, so go up one level then into data
        self.data_root = Path(__file__).parent.parent / "data"
        self.static_root = self.data_root / "static"

    def load_static(self, *path_parts):
        """
        Load static game data from the static directory

        Args:
            *path_parts: Path components relative to src/data/static/
                        Examples:
                        - load_static("species.json")
                        - load_static("menu", "main_menu.json")
                        - load_static("planetary_info", "planet_types.json")

        Returns:
            dict: Parsed JSON data

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
        """
        file_path = self.static_root / Path(*path_parts)
        return self._load_json(file_path)

    def load_runtime(self, *path_parts):
        """
        Load runtime game data (save files, procedurally generated data)

        Args:
            *path_parts: Path components relative to src/data/
                        Examples:
                        - load_runtime("star_systems.json")
                        - load_runtime("saves", "game_001.json")

        Returns:
            dict: Parsed JSON data

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
        """
        file_path = self.data_root / Path(*path_parts)
        return self._load_json(file_path)

    def _load_json(self, file_path):
        """
        Internal method to load and parse a JSON file

        Args:
            file_path: Absolute path to the JSON file

        Returns:
            dict: Parsed JSON data

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {file_path}: {e.msg}",
                e.doc,
                e.pos
            )

    def save_runtime(self, data, *path_parts):
        """
        Save runtime game data to JSON file

        Args:
            data: Data to serialize to JSON
            *path_parts: Path components relative to src/data/

        Example:
            save_runtime(game_state, "saves", "game_001.json")
        """
        file_path = self.data_root / Path(*path_parts)

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_data_path(self, *path_parts):
        """
        Get the absolute path to a data file without loading it

        Useful for passing paths to other systems (like image loaders)

        Args:
            *path_parts: Path components relative to src/data/

        Returns:
            Path: Absolute path to the file
        """
        return self.data_root / Path(*path_parts)
