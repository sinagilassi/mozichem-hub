# import libs
from typing import (
    Dict,
    Optional,
)
# local
from ..utils import Loader
from ..config import app_settings


class ThermoSymbols:
    """
    This class contains the symbols used in the MoziChem MCP.
    It is used to define the properties of the components.
    """
    # NOTE: attributes

    def __init__(self):
        '''
        Initialize the ThermoSymbols class with the symbols, all symbols are loaded from symbols.yml file.
        Then the symbols are loaded into the class attributes.
        '''
        # NOTE: set the symbols folder and source file
        self.symbols_folder: str = app_settings.symbols_folder
        self.symbols_source: str = app_settings.symbols_source

        # NOTE: initialize loader
        self.Loader_ = Loader()

        # Load symbols from YAML file
        self._symbols: Dict[str, str] = self._load_yaml()

    def _load_yaml(self) -> Dict[str, str]:
        '''
        Load the symbols from the YAML file and return them as a dictionary.
        '''
        try:
            symbols_ = self.Loader_.load_yml(
                target_folder=self.symbols_folder,
                target_file=self.symbols_source
            )

            # convert the symbols to lowercase
            if "SYMBOLS" not in symbols_:
                raise KeyError(
                    "The 'SYMBOLS' key is missing in the YAML file.")

            # Convert all keys to lowercase
            symbols_ = {k.lower(): v for k, v in symbols_["SYMBOLS"].items()}

            # return the symbols
            return symbols_

        except Exception as e:
            raise Exception(f"Failed to load symbols: {e}") from e

    def get_symbol(self, property_name: str) -> Optional[str]:
        """Get the symbol associated with a property name (e.g., 'temperature' → 'T')."""
        return self._symbols.get(property_name.lower(), None)

    def has_property(self, property_name: str) -> bool:
        """Check if a given property is defined."""
        return property_name.lower() in self._symbols

    def list_properties(self) -> list:
        """List all available property names."""
        return list(self._symbols.keys())

    def as_dict(self) -> Dict[str, str]:
        """Return the entire symbol mapping."""
        return self._symbols

    def __getitem__(self, property_name: str) -> str:
        """Enable dict-style access: symbols['pressure'] → 'P'."""
        key = property_name.lower()
        if key not in self._symbols:
            raise KeyError(f"'{property_name}' not found in symbols.")
        return self._symbols[key]

    def __repr__(self):
        return f"ThermoSymbols(properties={self.list_properties()})"
