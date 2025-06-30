# import libs
import logging
import yaml
from typing import (
    Optional,
    Dict,
    List,
    Union)
# local
from .contents import REFERENCE_CONTENT
from .config import REFERENCE_CONFIGS
from .link import REFERENCE_LINK
from .models import (
    References,
    ReferenceThermoDB,
    ComponentPropertySource
)
from .reference_adapter import ReferencesAdapter


class ReferencesInitializer:
    """
    This class is responsible for setting up the necessary references
    that will be used throughout the hub.
    """
    # NOTE: attributes

    def __init__(
        self,
        references: Optional[References] = None,
    ):
        """
        Initialize the references.
        """
        # LINK: initialize the ReferencesAdapter
        self.ReferencesAdapter_ = ReferencesAdapter()

        # SECTION: local reference
        # NOTE: load local reference
        self.local_references = self.__load_local_reference()

        # SECTION: set reference
        self.reference_thermodb = self.initialize_references(references)

    @property
    def reference_contents(self) -> List[str]:
        """
        Get the reference content.
        """
        return self.reference_thermodb.contents

    @property
    def reference_config(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Get the reference configuration.
        """
        return self.reference_thermodb.config

    @property
    def reference_link(self) -> str:
        """
        Get the reference rule.
        """
        return self.reference_thermodb.link

    def initialize_references(
        self,
        references: Optional[References] = None,
    ) -> ReferenceThermoDB:
        """
        Analyze the custom reference for the ThermoHub.

        Parameters
        ----------
        references : Optional[References]
            The custom references to be included in the ThermoHub.
            If None, only the local reference will be used.

        Returns
        -------
        dict
            The custom reference dictionary.
        """
        try:

            # SECTION: set default reference
            reference_thermodb = self.__generate_reference_thermodb(
                external_references=references
            )

            # return
            return reference_thermodb
        except Exception as e:
            raise ValueError(
                f"Failed to analyze custom reference: {e}") from e

    def __load_local_reference(self):
        """
        Load the local reference content, configuration, and rule.

        Returns
        -------
        str, Dict[str, Dict[str, ComponentPropertySource]], str
            The local reference content, configuration, and rule.
        """
        try:
            # Load the local reference content
            reference_content = REFERENCE_CONTENT

            # Load the local reference configuration
            reference_config = REFERENCE_CONFIGS

            # load the local reference link
            # reference_link = REFERENCE_LINK
            # ? from reference config
            reference_link = self.ReferencesAdapter_.build_reference_link(
                reference_config=reference_config
            )

            # local references
            local_references = References(
                contents=[reference_content],
                config=reference_config,
                link=reference_link
            )

            # result
            return local_references
        except Exception as e:
            raise ValueError(f"Failed to load local reference: {e}") from e

    def __generate_reference_thermodb(
        self,
        external_references: Union[References, None] = None
    ) -> ReferenceThermoDB:
        """
        Generate the ReferenceThermoDB object.

        Parameters
        ----------
        external_references : References
            The external references to be included in the ReferenceThermoDB.

        """
        try:
            # SECTION: set local reference content and config
            local_reference_content = self.local_references.contents or []
            local_reference_config = self.local_references.config or {}
            local_reference_link = self.local_references.link or ''

            # SECTION: check if external references are provided
            if external_references is None:
                # NOTE: reference
                reference = {
                    'reference': local_reference_content,
                }
                # NOTE: transform reference config
                local_reference_config = self._transform_reference_config(
                    local_reference_config
                )
                # Create the ReferenceThermoDB object
                reference_thermodb = ReferenceThermoDB(
                    reference=reference,
                    contents=local_reference_content,
                    config=local_reference_config,
                    link=local_reference_link
                )
            else:
                # SECTION: external reference
                # NOTE: set external reference content, config, and link
                external_reference_content = external_references.contents \
                    if external_references.contents else []
                external_reference_config = external_references.config \
                    if external_references.config else {}
                external_reference_link = external_references.link \
                    if external_references.link else ''

                # SECTION: merge local and external references
                # Combine local reference content with external references
                reference_contents = \
                    local_reference_content + external_reference_content
                reference_config = {
                    **local_reference_config,
                    **external_reference_config
                }
                reference_link = (
                    local_reference_link or
                    external_reference_link
                )

                # NOTE: reference
                reference = {
                    'reference': reference_contents,
                }

                # NOTE: transform reference config
                reference_config = self._transform_reference_config(
                    reference_config
                )

                # Create the ReferenceThermoDB object
                reference_thermodb = ReferenceThermoDB(
                    reference=reference,
                    contents=reference_contents,
                    config=reference_config,
                    link=reference_link
                )

            # res
            return reference_thermodb
        except Exception as e:
            raise ValueError(
                f"Failed to generate ReferenceThermoDB: {e}") from e

    def _get_reference_link(
        self,
    ) -> str:
        """
        Get the reference link.

        Returns
        -------
        str
            The reference link.
        """
        try:
            return self.reference_link
        except Exception as e:
            raise ValueError(f"Failed to select reference link: {e}") from e

    def _get_reference_thermodb(
        self,
    ) -> ReferenceThermoDB:
        """
        Get the reference thermodynamic database.

        Returns
        -------
        ReferenceThermoDB
            The reference thermodynamic database.
        """
        try:
            return self.reference_thermodb
        except Exception as e:
            raise ValueError(
                f"Failed to select reference thermodynamic database: {e}") from e

    def _transform_reference_config(
        self,
        reference_config: Dict[str, Dict[str, ComponentPropertySource]]
    ) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Build the reference configuration from a string or dictionary.

        Parameters
        ----------
        reference_config : Dict[str, Dict[str, ComponentPropertySource]]
            The reference configuration to be built.

        Returns
        -------
        Dict[str, Dict[str, str]]
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
            res: Dict[str, Dict[str, Dict[str, str]]] = {}

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
