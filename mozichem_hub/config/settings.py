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

    # Directory where the application is running
    base_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent)

    # Directory for storing data files
    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent / "data")

    # Directory for configuration files
    config_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent / "config")

    class Config:
        """Pydantic configuration."""
        env_prefix = "mozichem_hub_"
        case_sensitive = True
