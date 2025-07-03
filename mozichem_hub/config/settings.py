# PACKAGE INFORMATION
# --------------------
# import libs
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

__version__ = "0.1.0"
__description__ = "MoziChem-Hub"
__author__ = "Sina Gilassi"
__author_email__ = "sina.gilassi@gmail.com"


class Settings(BaseSettings):
    """Application settings for Mozichem Hub."""

    # Package metadata
    version: str = __version__
    description: str = __description__
    author: str = __author__

    # NOTE: dependencies
    dependencies: list[str] = Field(
        default_factory=lambda: [
            "pydantic",
            "pydantic-settings",
            "fastmcp",
            "pyyaml",
            "pythermodb",
            "pythermolinkdb",
            "pythermomodels",
        ],
        description="List of dependencies required by the application."
    )

    # Directory where the application is running
    base_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent)

    # Directory for storing data files
    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent / "data")

    # Directory for configuration files
    config_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent / "config")

    # symbols for the application
    symbols_folder: str = Field(
        default="references",
        description="Folder name for storing symbols."
    )

    symbols_source: str = Field(
        default="symbols.yml",
        description="Source file name for symbols."
    )

    class Config:
        """Pydantic configuration."""
        env_prefix = "mozichem_hub_"
        case_sensitive = True


def get_config() -> Settings:
    """
    Get the application settings.

    Returns
    -------
    Settings
        The application settings.
    """
    return Settings()


# Initialize settings
app_settings = get_config()

# log
# res_ = app_settings.model_dump()
# print(res_)
# print(type(res_))

# res_ = app_settings.data_dir
# print(f"Data directory: {res_}")
# print(type(res_))

# dependencies = app_settings.dependencies
# print(f"Dependencies: {dependencies}, {type(dependencies)}")
