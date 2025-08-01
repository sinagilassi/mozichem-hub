# import libs
import logging
from typing import (
    Dict
)
from pyThermoDB.references import (
    ReferenceChecker,
    load_reference_from_str
)
# locals
from ..errors import (
    NoDatabookFoundError,
    ReferenceConfigGenerationError,
    ReferenceLinkGenerationError,
    NO_DATABOOK_FOUND_MSG,
    REFERENCE_CONFIG_GEN_ERROR_MSG,
    COMPONENT_REFERENCE_CONFIG_ERROR_MSG,
    COMPONENT_REFERENCE_LINK_ERROR_MSG
)
from ..models import (
    Component,
    ComponentReferenceConfig,
    ComponentReferenceLink,
    ReferenceThermoDB
)


class ReferenceThermoDBController():
    """
    Controller for managing the ReferenceThermoDB.
    """

    def __init__(self, reference_content: str):
        """
        Initialize the ReferenceThermoDBController.

        Parameters
        ----------
        reference_content : str
            The content of the reference to be managed.
        """
        # set
        self.reference_content = reference_content

        # NOTE: check if reference_content is a string
        if not isinstance(reference_content, str):
            raise TypeError("reference_content must be a string.")

        # SECTION: load the reference from string
        self.reference = load_reference_from_str(reference_content)

        # SECTION: create ReferenceChecker instance
        self.ReferenceChecker_ = ReferenceChecker(reference_content)

    def get_databook_names(self) -> list:
        """
        Get the names of the databooks in the reference.

        Returns
        -------
        list
            A list of databook names.
        """
        return self.ReferenceChecker_.get_databook_names()

    def get_default_databook_name(self) -> str:
        """
        Get the name of the first databook in the reference.

        Returns
        -------
        str
            The name of the first databook.
        """
        databook_names = self.get_databook_names()
        if not databook_names:
            logging.error(NO_DATABOOK_FOUND_MSG)
            raise NoDatabookFoundError(NO_DATABOOK_FOUND_MSG)

        # check if the first databook name is valid
        if not databook_names[0]:
            logging.error(NO_DATABOOK_FOUND_MSG)
            raise NoDatabookFoundError(NO_DATABOOK_FOUND_MSG)

        return databook_names[0]

    def generate_component_reference_config(
        self,
        component_name: str,
        component_formula: str,
        component_state: str,
    ) -> ComponentReferenceConfig:
        """
        Generate the reference configuration for a component.

        Parameters
        ----------
        component_name : str
            The name of the component.
        component_formula : str
            The formula of the component.
        component_state : str
            The state of the component (e.g., s, l, g).

        Returns
        -------
        ComponentReferenceConfig
            A dictionary containing the reference configuration for the component.

        Notes
        -----
        The `first databook` in the list of databooks will be used to generate the reference configuration.

        Example
        -------
        ```python
        CO2_reference_config = {
            'ideal-gas-heat-capacity': {
                'databook': 'CUSTOM-REF-1',
                'table': 'ideal-gas-heat-capacity'
                },
            'general-data': {
                'databook': 'CUSTOM-REF-1',
                'table': 'general-data'
                },
            'vapor-pressure': {
                'databook': 'CUSTOM-REF-1',
                'table': 'vapor-pressure'
                }
            }
        ```
        """
        try:
            # NOTE: selected databook
            selected_databook = self.get_default_databook_name()

            # SECTION: generate the reference config
            component_reference_config = \
                self.ReferenceChecker_.get_component_reference_config(
                    component_name=component_name,
                    component_formula=component_formula,
                    component_state=component_state,
                    databook_name=selected_databook
                )

            # check if the reference config is empty
            if not component_reference_config:
                logging.error(COMPONENT_REFERENCE_CONFIG_ERROR_MSG)
                raise ReferenceConfigGenerationError(
                    COMPONENT_REFERENCE_CONFIG_ERROR_MSG)

            # return
            return component_reference_config
        except NoDatabookFoundError:
            # Already logged above
            raise
        except Exception as e:
            logging.error(f"{REFERENCE_CONFIG_GEN_ERROR_MSG}: {e}")
            raise ReferenceConfigGenerationError(
                REFERENCE_CONFIG_GEN_ERROR_MSG) from e

    def generate_components_reference_config(
        self,
        components: list[Component]
    ) -> Dict[str, ComponentReferenceConfig]:
        """
        Generate the reference configuration for multiple components.

        Parameters
        ----------
        components : list[Component]
            A list of dictionaries containing component details.

        Returns
        -------
        dict[str, ComponentReferenceConfig]
            A dictionary containing the reference configuration for each component.
        """
        try:
            # SECTION: generate the reference config for each component
            reference_config = {}

            # iterate over components
            for component in components:
                ref_config = self.generate_component_reference_config(
                    component_name=component.name,
                    component_formula=component.formula,
                    component_state=component.state
                )
                reference_config[component.name] = ref_config

            return reference_config
        except NoDatabookFoundError:
            # Already logged above
            raise
        except Exception as e:
            logging.error(f"{REFERENCE_CONFIG_GEN_ERROR_MSG}: {e}")
            raise ReferenceConfigGenerationError(
                REFERENCE_CONFIG_GEN_ERROR_MSG) from e

    def generate_component_reference_link(
        self,
        component_name: str,
        component_formula: str,
        component_state: str,
    ) -> ComponentReferenceLink:
        """
        Generate the reference link for a specific databook. The first databook
        in the list of databooks will be used to generate the reference link.

        Parameters
        ----------
        component_name : str
            The name of the component.
        component_formula : str
            The formula of the component.
        component_state : str
            The state of the component (e.g., s, l, g).

        Returns
        -------
        dict[str, ComponentReferenceLink]
            A dictionary containing the reference link for the specified databook.
        """
        try:
            # SECTION: get the first databook name
            databook_name = self.get_default_databook_name()

            # SECTION: get the reference link
            reference_link: ComponentReferenceLink = \
                self.ReferenceChecker_.generate_reference_link(
                    databook_name=databook_name,
                    component_name=component_name,
                    component_formula=component_formula,
                    component_state=component_state
                )

            # res
            return reference_link
        except Exception as e:
            logging.error(f"{COMPONENT_REFERENCE_LINK_ERROR_MSG}: {e}")
            raise ReferenceLinkGenerationError(
                COMPONENT_REFERENCE_LINK_ERROR_MSG) from e

    def generate_components_reference_link(
        self,
        components: list[Component]
    ) -> Dict[str, ComponentReferenceLink]:
        """
        Generate the reference link for multiple components.

        Parameters
        ----------
        components : list[Component]
            A list of dictionaries containing component details.

        Returns
        -------
        dict[str, ComponentReferenceLink]
            A dictionary containing the reference link for each component.
        """
        try:
            # SECTION: generate the reference link for each component
            reference_link = {}

            # iterate over components
            for component in components:
                ref_link = self.generate_component_reference_link(
                    component_name=component.name,
                    component_formula=component.formula,
                    component_state=component.state
                )
                reference_link[component.name] = ref_link

            return reference_link
        except Exception as e:
            logging.error(f"{COMPONENT_REFERENCE_LINK_ERROR_MSG}: {e}")
            raise ReferenceLinkGenerationError(
                COMPONENT_REFERENCE_LINK_ERROR_MSG) from e

    def generate_components_reference_thermodb(
        self,
        components: list[Component]
    ) -> ReferenceThermoDB:
        """
        Generate the reference thermodynamic database (ReferenceThermoDB).

        Parameters
        ----------
        component_name : str
            The name of the component.
        component_formula : str
            The formula of the component.
        component_state : str
            The state of the component (e.g., s, l, g).
        """
        try:
            # SECTION: reference
            reference = {'reference': [self.reference_content]}

            # SECTION: reference contents
            reference_contents = [self.reference_content]

            # SECTION: generate reference config and link for each component
            # init components reference config
            components_reference_config = {}
            # init components reference link
            components_reference_link = {}

            # iterate over components
            for component in components:
                # NOTE: generate reference config
                component_reference_config = \
                    self.generate_component_reference_config(
                        component_name=component.name,
                        component_formula=component.formula,
                        component_state=component.state
                    )

                # NOTE: generate reference link
                component_reference_link = \
                    self.generate_component_reference_link(
                        component_name=component.name,
                        component_formula=component.formula,
                        component_state=component.state
                    )

                # ! component name-state
                component_name_state = f"{component.name}-{component.state}"
                # ! component formula-state
                component_formula_state = f"{component.formula}-{component.state}"

                # NOTE: save by name-state
                # add to components reference config
                components_reference_config[component_name_state] = \
                    component_reference_config
                # add to components reference link
                components_reference_link[component_name_state] = \
                    component_reference_link

                # NOTE: save by formula-state
                # add to components reference config
                components_reference_config[component_formula_state] = \
                    component_reference_config
                # add to components reference link
                components_reference_link[component_formula_state] = \
                    component_reference_link

            # SECTION: create ReferenceThermoDB instance
            reference_thermodb = ReferenceThermoDB(
                reference=reference,
                contents=reference_contents,
                config=components_reference_config,
                link=components_reference_link
            )

            # SECTION: return ReferenceThermoDB instance
            return reference_thermodb

        except Exception as e:
            logging.error(
                f"Failed to generate component reference thermodb: {e}")
            raise RuntimeError(
                "Failed to generate component reference thermodb.") from e
