"""Simple configuration management for di.core.

This module defines pydantic models for configuration values and provides a
`ConfigManager` which loads and persists the configuration to a JSON file. The
configuration is intended to be shared across the core runtime, database and
individual skills.  A single global ``config_manager`` instance is created on
import so that other modules can easily access the loaded configuration.

The configuration file is stored as ``config.json`` in the current working
directory by default.  When the file does not exist or cannot be parsed a set
of default values is used.
"""

from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel


class CoreConfig(BaseModel):
    """Settings for the di.core runtime itself."""

    log_level: str = "INFO"


class DatabaseConfig(BaseModel):
    """Settings for the small key/value store used by skills."""

    path: str = "/tmp/di_base.json"


class UnscrewConfig(BaseModel):
    """Configuration for the example ``Unscrew`` skill."""

    default_torque: int = 5


class SkillsConfig(BaseModel):
    """Collection of per‑skill configuration sections."""

    Unscrew: UnscrewConfig = UnscrewConfig()


class AppConfig(BaseModel):
    """Top level configuration model grouping all sections."""

    core: CoreConfig = CoreConfig()
    database: DatabaseConfig = DatabaseConfig()
    skills: SkillsConfig = SkillsConfig()


class ConfigManager:
    """Load and persist configuration values."""

    def __init__(self, path: str | Path = "config.json") -> None:
        self._path = Path(path)
        if self._path.exists():
            try:
                self.config = AppConfig.model_validate_json(self._path.read_text())
            except Exception:  # noqa: BLE001 - fall back to defaults
                self.config = AppConfig()
        else:
            self.config = AppConfig()

    def save(self) -> None:
        """Persist the current configuration to disk."""

        self._path.write_text(self.config.model_dump_json(indent=2))

    def update(self, data: dict) -> AppConfig:
        """Update configuration with ``data`` and persist it."""

        self.config = self.config.model_copy(update=data)
        self.save()
        return self.config

    def get_skill(self, name: str):
        """Return configuration section for the given skill name."""

        return getattr(self.config.skills, name, None)


# Global instance used by the application
config_manager = ConfigManager()

