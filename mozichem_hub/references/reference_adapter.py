# import libs
import yaml
import json
import logging
from typing import Dict, Any, Literal, Union
from pyThermoDB.references import ReferenceConfig, ReferenceChecker
from pyThermoDB.models import ComponentConfig, ComponentRule
# local
from ..models import ComponentPropertySource


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
                reference_config
            )
        elif reference_config_type == "dict":
            # ! convert string-dictionary to dictionary
            reference_config = json.loads(reference_config)
            res_dict = reference_config
        else:
            logging.error(
                "Invalid reference_config_type: %s. "
                "Expected 'str' or 'dict'.", reference_config_type
            )
            res_dict = None

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

            # NOTE: iterate over the dictionary and convert ComponentPropertySource to dict
            for key, value in res_dict.items():
                # NOTE: iterate over value
                if not isinstance(value, dict):
                    raise ValueError(
                        f"Expected a dictionary for key '{key}', "
                        f"but got {type(value)}."
                    )

                # ! init the inner dictionary
                inner_res: Dict[str, ComponentPropertySource] = {}

                # NOTE: iterate over the inner dictionary
                for inner_key, inner_value in value.items():
                    # inner res
                    if not inner_key:
                        break  # skip empty keys:

                    # check if the inner value is a ComponentPropertySource
                    if isinstance(inner_value, ComponentPropertySource):
                        # Convert ComponentPropertySource to dict
                        inner_res[inner_key] = inner_value
                    elif isinstance(inner_value, dict):
                        # If it's already a dict, just use it
                        inner_res[inner_key] = ComponentPropertySource(
                            **inner_value
                        )
                    else:
                        raise ValueError(
                            f"Unexpected type for key '{inner_key}': {type(inner_value)}"
                        )

                    # add to the result dictionary
                    res[key] = inner_res

            # NOTE: return the result
            return res
        except Exception as e:
            logging.error(f"Failed to adapt reference config: {e}")
            raise ValueError(f"Failed to adapt reference config: {e}") from e

    def config_from_dict(
        self,
        reference_config: dict
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
    ) -> Union[Dict[str, Dict[str, Dict[str, str]]], None]:
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

        Notes
        -----
        The reference link is created based on the provided configuration which contains:
        - label shows the universal symbol of the property (used in other apps)
        - labels show the universal symbols of the properties (used in other apps)

        ```python
        REFERENCE_CONFIG: Dict[str, ComponentPropertySource] = {
            'heat-capacity': ComponentPropertySource(
                databook='CUSTOM-REF-1',
                table='ideal-gas-molar-heat-capacity',
                mode='EQUATIONS',
                label='Cp_IG'
            ),
            'vapor-pressure': ComponentPropertySource(
                databook='CUSTOM-REF-1',
                table='vapor-pressure',
                mode='EQUATIONS',
                label='VaPr'
            ),
            'general': ComponentPropertySource(
                databook='CUSTOM-REF-1',
                table='general-data',
                mode='DATA',
                labels={
                    'critical-pressure': 'Pc',
                    'critical-temperature': 'Tc',
                    'acentric-factor': 'AcFa',
                }
            )
        }
        ```
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
            # iterate over the reference config
            for component, sections in reference_config.items():

                # init the component in the formatted dictionary
                formatted_dict[component] = {}

                # ! build DATA
                formatted_dict[component]['DATA'] = {}
                # ! build EQUATIONS
                formatted_dict[component]['EQUATIONS'] = {}

                # iterate over the sections of the component
                for section, cps in sections.items():

                    # NOTE: Extract `label` or `labels`
                    if cps.labels:
                        sets_ = cps.labels
                        formatted_dict[component]['DATA'].update(sets_)

                    if cps.label:
                        set_ = {section: cps.label}
                        formatted_dict[component]['EQUATIONS'].update(set_)

                # NOTE: check if the DATA section is empty
                if not formatted_dict[component]['DATA']:
                    # None
                    formatted_dict[component]['DATA'] = None

                # NOTE: check if the EQUATIONS section is empty
                if not formatted_dict[component]['EQUATIONS']:
                    # None
                    formatted_dict[component]['EQUATIONS'] = None

            # NOTE: return the formatted dictionary
            return formatted_dict
        except Exception as e:
            logging.error(
                "Failed to generate reference link. "
                "Please check the provided configuration. Error: %s", e
            )
            return None

    def str_from_reference_link(
            self,
            reference_link: Dict[str, Dict[str, ComponentRule]]
    ) -> str:
        """
        Convert the reference link to a string format.

        Parameters
        ----------
        reference_link : Dict[str, Dict[str, ComponentRule]]
            The reference link to be converted.

        Returns
        -------
        str
            The reference link as a string.
        """
        try:
            # Dump with line breaks between top-level items
            formatted_str = yaml.dump(
                reference_link,
                sort_keys=False,
                default_flow_style=False
            )

            # NOTE: return the formatted string
            return formatted_str.strip()
        except Exception as e:
            logging.error(
                "Failed to convert reference link to string. "
                "Please check the provided link. Error: %s", e
            )
            raise ValueError(
                f"Failed to convert reference link to string: {e}") from e

    def dict_from_reference_link(
            self,
            reference_link: str
    ) -> Dict[str, Dict[str, ComponentRule]]:
        """
        Convert the reference link from a string to a dictionary format.

        Parameters
        ----------
        reference_link : str
            The reference link to be converted.

        Returns
        -------
        Dict[str, Dict[str, Dict[str, str]]]
            The reference link as a dictionary.
        """
        try:
            # Load the YAML string into a dictionary
            return yaml.safe_load(reference_link)
        except yaml.YAMLError as e:
            logging.error(
                "Failed to convert reference link from string to dict. "
                "Please check the provided link. Error: %s", e
            )
            raise ValueError(
                f"Failed to convert reference link from string to dict: {e}") from e

    def to_reference_config(
        self,
        reference_config: Dict[str, Dict[str, ComponentPropertySource]]
    ) -> Dict[str, Dict[str, ComponentConfig]]:
        """
        Build the reference configuration from a string or dictionary.

        Parameters
        ----------
        reference_config : Dict[str, Dict[str, ComponentPropertySource]]
            The reference configuration to be built.

        Returns
        -------
        Dict[str, Dict[str, ComponentConfig]]
            The built reference configuration as a dictionary.

        Notes
        -----
        The reference configuration is used by PyThermoDB to access the databook, table as:
        ```python
        {
            "CO2": {
                "heat-capacity": {
                    "databook": "databook 1",
                    "table": "table 1",
                },
                "vapor-pressure": {
                    "databook": "databook 2",
                    "table": "table 2",
                },
                "general": {
                    "databook": "databook 2",
                    "table": "table 2",
                }
            }
        }
        ```
        """
        # NOTE: check if the reference config is empty
        if not reference_config:
            logging.warning("Reference configuration is empty.")
            return {}

        # NOTE: convert the dictionary to the required format
        try:
            # NOTE: initialize the result dictionary
            res: Dict[str, Dict[str, ComponentConfig]] = {}

            # Iterate over components and sections
            for component, sections in reference_config.items():
                res[component] = {}
                # Iterate over sections and extract databook and table
                for section, cps in sections.items():
                    # property name
                    prop_name = section
                    # Extract databook and table
                    if isinstance(cps, ComponentPropertySource):
                        # databook
                        databook = cps.databook
                        # table
                        table = cps.table

                        # prop
                        prop_ = {
                            'databook': databook,
                            'table': table
                        }

                        # add to component
                        res[component][prop_name] = prop_

                    else:
                        logging.warning(
                            f"Invalid ComponentPropertySource for {component} in section {section}. "
                            "Expected ComponentPropertySource instance."
                        )

            return res
        except Exception as e:
            logging.error(
                "Failed to build reference configuration. "
                "Please check the provided configuration. Error: %s", e
            )
            raise

    def extract_component_reference_config_from_reference_content(
        self,
        reference_content: str,
        component_name: str,
        component_formula: str,
        component_state: str
    ):
        '''
        Extract the component reference configuration from the reference content.

        Parameters
        ----------
        reference_content : str
            The reference content from which to extract the configuration.
        component_name : str
            The name of the component for which to extract the configuration.
        component_formula : str
            The formula of the component for which to extract the configuration.
        component_state : str
            The state of the component for which to extract the configuration.
        '''
        try:
            # NOTE: initialize the ReferenceChecker
            ReferenceChecker_ = ReferenceChecker(reference_content)

            # NOTE: get component reference config
            component_reference_config = \
                ReferenceChecker_.get_component_reference_config(
                    component_name=component_name,
                    component_formula=component_formula,
                    component_state=component_state,
                    databook_name='CUSTOM-REF-1',
                )

            # NOTE: check if the component reference config is empty
            if not component_reference_config:
                logging.warning(
                    f"No reference configuration found for component: {component_name}."
                )
                return None

            # NOTE: res
            return component_reference_config
        except Exception as e:
            logging.error(
                "Failed to extract reference configuration from content. "
                "Please check the provided content. Error: %s", e
            )
            raise ValueError(
                f"Failed to extract reference configuration from content: {e}") from e
