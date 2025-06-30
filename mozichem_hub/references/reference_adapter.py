# import libs
import yaml
import json
import logging
from typing import Dict, Any, Literal, Union
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
        # SECTION: check if the reference_config is a string
        # NOTE: set the reference config
        self.ReferenceConfig_ = ReferenceConfig()

    def config_from_str(
        self,
        reference_config: str,
        reference_config_type: Literal[
            "str", "dict"
        ] = "str",
    ) -> Dict[str, Dict[str, ComponentPropertySource]]:
        """
        Convert the reference configuration to the required format.

        Parameters
        ----------
        reference_config : str
            The reference configuration to be adapted. It can be a dictionary,
            a string, or None.

        Returns
        -------
        Dict[str, Dict[str, ComponentPropertySource]]
            The adapted reference configuration as a dictionary.
        """
        # NOTE: set the reference config
        if reference_config_type == "str":
            # ! convert string to dictionary
            res_dict = self.ReferenceConfig_.set_reference_config(
                reference_config)
        elif reference_config_type == "dict":
            # ! convert string-dictionary to dictionary
            reference_config = json.loads(reference_config)
            res_dict = reference_config
        else:
            logging.error(
                "Invalid reference_config_type: %s. "
                "Expected 'str' or 'dict'.", reference_config_type
            )

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

    def config_from_dict(
        self,
        reference_config: Dict[str, Dict[str, str]]
    ) -> Dict[str, Dict[str, ComponentPropertySource]]:
        """
        Convert the reference configuration from a dictionary to the required format (dictionary).

        Parameters
        ----------
        reference_config : Dict[str, Dict[str, str]]
            The reference configuration to be adapted.

        Returns
        -------
        Dict[str, Dict[str, ComponentPropertySource]]
            The adapted reference configuration as a dictionary.
        """
        # SECTION: check if the reference_config is a dictionary
        if not isinstance(reference_config, dict):
            raise ValueError(
                "The reference configuration must be a dictionary.")

        # NOTE: convert the dictionary to the required format
        # Convert single quotes to double quotes
        reference_config_str = str(reference_config)
        reference_config_str = reference_config_str.replace("'", '"')

        # return the adapted reference configuration
        return self.config_from_str(
            reference_config_str,
            reference_config_type="dict"
        )

    def build_reference_link(
        self,
        reference_config: Dict[str, Dict[str, ComponentPropertySource]]
    ) -> Union[str, None]:
        """
        Generate a reference link from the provided configuration.

        Parameters
        ----------
        reference_config : Dict[str, Dict[str, ComponentPropertySource]]
            The reference configuration to generate the link from.

        Returns
        -------
        str
            The generated reference link.
        """
        # NOTE: check if the reference config is empty
        if not reference_config:
            logging.warning("Reference configuration is empty.")
            return None

        # check length of the reference config
        if len(reference_config) == 0:
            logging.warning("Reference configuration is empty.")
            return None

        # NOTE: format the reference config to a dictionary with labels
        # Initialize the formatted dictionary
        formatted_dict = {}

        try:
            for component, sections in reference_config.items():
                formatted_dict[component] = {}
                for section, cps in sections.items():
                    if section.upper() not in ["DATA", "EQUATIONS"]:
                        continue
                    # Extract `label` or `labels`
                    if cps.labels:
                        formatted_dict[component][section.upper()] = cps.labels
                    elif cps.label:
                        formatted_dict[component][section.upper()] = {
                            cps.label: cps.label}

            # Dump with line breaks between top-level items
            return yaml.dump(
                formatted_dict,
                sort_keys=False,
                default_flow_style=False
            )
        except Exception as e:
            logging.error(
                "Failed to generate reference link. "
                "Please check the provided configuration. Error: %s", e
            )
            return None
