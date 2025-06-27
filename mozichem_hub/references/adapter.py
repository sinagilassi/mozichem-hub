# import libs
import logging
from typing import Dict, Any
from pyThermoDB.references import ReferenceConfig
# local
from .models import ComponentPropertySource


class ReferencesAdapter:
    """
    This class is responsible for adapting the references to the required format.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the ReferencesAdapter.
        """
        # NOTE: set the reference config
        self.reference_config = ReferenceConfig()

    def adapt_reference_config(
        self,
        reference_config: str
    ) -> Dict[str, Any]:
        """ Adapt the reference configuration to the required format.
        """
        # NOTE: set the reference config
        res_dict = self.reference_config.set_reference_config(reference_config)

        try:
            # NOTE: check if the result is a valid dictionary
            if not isinstance(res_dict, dict):
                raise ValueError(
                    "The reference configuration is not a valid dictionary.")

            # NOTE: check if the dictionary is empty
            if not res_dict:
                raise ValueError(
                    "The reference configuration is empty or invalid.")

            # SECTION: convert ComponentPropertySource to dict
            # init the result dictionary
            res: Dict[str, Any] = {}

            # iterate over the dictionary and convert ComponentPropertySource to dict
            for key, value in res_dict.items():
                if isinstance(value, ComponentPropertySource):
                    res[key] = value.model_dump()
                elif isinstance(value, dict):
                    # If it's already a dict, just use it
                    res[key] = value
                else:
                    raise ValueError(
                        f"Unexpected type for key '{key}': {type(value)}")

            return res
        except Exception as e:
            logging.error(f"Failed to adapt reference config: {e}")
            raise ValueError(f"Failed to adapt reference config: {e}") from e
