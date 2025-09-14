# import libs
import logging
from typing import (
    Literal,
    List,
    Dict,
    Union,
    Any
)
import pyThermoDB as ptdb
from pythermodb_settings.models import (
    ComponentConfig,
    CustomReference,
    Component,
    ReferencesThermoDB
)
from pyThermoDB import CompBuilder
import pyThermoLinkDB as ptldb
# locals
from .hub_manager import HubManager
from ..utils.component_utils import create_component_id
from ..models import ComponentThermoDB
# error messages
from ..errors import (
    HubInitializationError,
    HubThermoHubBuildError,
    HubThermoHubCleanError,
    HubComponentThermoDBRegistrationError,
    HubComponentsThermoDBRegistrationError,
    ComponentThermoDBBuildError,
    ModelSourceBuildError,
    HubComponentModelSourceBuildError,
    HubComponentsModelSourceBuildError,
    HUB_INITIALIZATION_ERROR_MSG,
    HUB_THERMO_HUB_BUILD_ERROR_MSG,
    HUB_THERMO_HUB_CLEAN_ERROR_MSG,
    HUB_COMPONENT_THERMODB_REGISTRATION_ERROR_MSG,
    HUB_COMPONENTS_THERMODB_REGISTRATION_ERROR_MSG,
    COMPONENT_THERMODB_BUILD_ERROR_MSG,
    MODEL_SOURCE_BUILD_ERROR_MSG,
    HUB_COMPONENT_MODEL_SOURCE_BUILD_ERROR_MSG,
    HUB_COMPONENTS_MODEL_SOURCE_BUILD_ERROR_MSG
)

# Configure logger
logger = logging.getLogger(__name__)


class Hub(HubManager):
    """
    Hub class for building and managing the thermodynamic properties
    """
    # NOTE: attributes

    def __init__(
            self,
            references_thermodb: ReferencesThermoDB,
    ):
        """
        Initialize the Hub instance.

        Parameters
        ----------
        references_thermodb : ReferencesThermoDB
            The references thermodynamic database.


        Notes
        -----
        The ReferenceThermoDB contains:
            - reference: Dict[str, List[str]]
            - contents: List[str]
            - configs: Dict[str, ComponentConfig]
            - rules: Dict[str, ComponentRule]
            - labels: Optional[List[str]]
            - ignore_labels: Optional[List[str]]
            - ignore_props: Optional[List[str]]

        """
        logger.info("Initializing Hub instance")

        try:
            # LINK: initialize parent class
            super().__init__(references_thermodb)

            # SECTION: Initialize the ThermoHub
            logger.debug("Building ThermoHub instance")
            self.thermo_hub = self.build_thermo_hub()

            logger.info("Hub instance initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Hub: {e}")
            raise HubInitializationError(HUB_INITIALIZATION_ERROR_MSG) from e

    def build_thermo_hub(self):
        """
        Initialize the ThermoHub instance.
        """
        logger.debug("Building ThermoHub instance")

        try:
            # Initialize the ThermoHub
            self.thermo_hub = ptldb.init()
            logger.debug("ThermoHub instance built successfully")
            return self.thermo_hub

        except Exception as e:
            logger.error(f"Failed to build ThermoHub: {e}")
            raise HubThermoHubBuildError(
                HUB_THERMO_HUB_BUILD_ERROR_MSG
            ) from e

    def clean_thermo_hub(self):
        """
        Clean the ThermoHub, it remains.
        """
        logger.debug("Cleaning ThermoHub instance")

        try:
            # clean the ThermoHub
            self.thermo_hub.clean()
            logger.debug("ThermoHub cleaned successfully")

        except Exception as e:
            logger.error(f"Failed to clean ThermoHub: {e}")
            raise HubThermoHubCleanError(
                HUB_THERMO_HUB_CLEAN_ERROR_MSG
            ) from e

    def register_component_thermodb(
        self,
        component_thermodb: ComponentThermoDB
    ):
        """
        Register the component thermodynamic database in the ThermoHub.

        Parameters
        ----------
        component : ComponentThermoDB
            The component thermodynamic database to register.
            - component: Component
            - thermodb: CompBuilder
            - component_key: Literal['name', 'formula']

        Returns
        -------
        bool
            True if registration is successful, False otherwise.
        """
        logger.debug("Registering component thermodynamic database")

        try:
            # NOTE: extract component
            component = component_thermodb.component
            thermodb = component_thermodb.thermodb
            # component_key = component_thermodb.component_key

            # NOTE: set component identity
            component_identity = create_component_id(
                component=component
            )

            name_state = component_identity.name_state
            formula_state = component_identity.formula_state

            logger.debug(
                f"Registering component: {name_state} / {formula_state}")

            # SECTION: create component reference rule
            # ! by name-state
            component_reference_rule_by_name = \
                self._set_component_reference_rule(
                    component_id=name_state
                )
            # ! by formula-state
            component_reference_rule_by_formula = \
                self._set_component_reference_rule(
                    component_id=formula_state
                )

            # SECTION: register the component thermodynamic database
            # NOTE: by name
            self.thermo_hub.add_thermodb(
                name=name_state,
                data=thermodb,
                rules=component_reference_rule_by_name
            )

            # NOTE: by formula
            self.thermo_hub.add_thermodb(
                name=formula_state,
                data=thermodb,
                rules=component_reference_rule_by_formula
            )

            logger.debug(
                f"Component thermodynamic database registered "
                f"successfully: {name_state} / {formula_state}"
            )
            return True

        except Exception as e:
            logger.error(
                f"Failed to register component thermodynamic database: {e}"
            )
            raise HubComponentThermoDBRegistrationError(
                HUB_COMPONENT_THERMODB_REGISTRATION_ERROR_MSG
            ) from e

    def build_component_thermodb(
        self,
        component: Component | List[Component],
        component_key: Literal[
            'Name-State', 'Formula-State'
        ] = 'Name-State'
    ) -> Union[
        ComponentThermoDB,
        List[ComponentThermoDB]
    ]:
        """
        Build the component thermodynamic database.

        Parameters
        ----------
        component : Component | List[Component]
            The component or list of components for which to build the
            thermodynamic database.
            - If a single Component is provided, it will be treated as a
              single component.
            - If a list of Components is provided, each item must be a
              Component.
        component_key : Literal['Name-State', 'Formula-State'], optional
            The mode to build the thermodynamic database, either by 'Name-State'
            or 'Formula-State'.
            Default is 'Name-State'.

        Returns
        -------
        Union[ComponentThermoDB, List[ComponentThermoDB]]
            The component thermodynamic database.
        """
        logger.info("Building component thermodynamic database")

        try:
            # SECTION: check input type
            if isinstance(component, Component):
                # NOTE: if input is a string, treat it as a single Component
                component_ = [component]
            elif isinstance(component, list):
                # NOTE: if input is a list, treat it as a list of Components
                component_ = component
                for comp in component_:
                    if not isinstance(comp, Component):
                        raise TypeError(
                            "All items in the list must be Components.")
            else:
                raise TypeError(
                    "Input must be a Component or a list of Components.")

            # SECTION: build process
            # initialize the component thermodynamic database
            components_thermodb: List[ComponentThermoDB] = []

            # check reference
            if self.reference is None:
                raise ValueError(
                    "Reference is not set. Please provide a valid reference."
                )

            # NOTE: loop through each component
            for component in component_:
                # NOTE: input configuration
                component_name = component.name.strip()
                component_formula = component.formula.strip()
                component_state = component.state.strip().lower()

                # SECTION: build the component thermodynamic database
                # NOTE: check build mode
                if component_key == 'Name-State':  # ! >> name-state
                    # NOTE: component reference config
                    component_id = create_component_id(
                        component=component
                    ).name_state

                    # >>> get the component reference config
                    component_reference_config_: Dict[str, ComponentConfig] = \
                        self._set_component_reference_config(
                            component_id=component_id
                    )

                    # >>> get the component reference
                    component_reference_: CustomReference = \
                        self._set_component_reference(
                            component_id=component_id
                        )

                    # >>> get ignore labels
                    # ! by default, empty list
                    component_ignore_labels_: List[str] = self._set_component_ignore_labels(
                        component_id=component_id
                    )

                    # ! by name (older version)
                    # component_thermodb: CompBuilder = ptdb.build_component_thermodb(
                    #     component_name=component_name,
                    #     reference_config=component_reference_config,
                    #     custom_reference=self.reference
                    # )

                    # ! by name (newer version)
                    component_thermodb: CompBuilder = ptdb.check_and_build_component_thermodb(
                        component=component,
                        reference_config=component_reference_config_,
                        custom_reference=component_reference_,
                        component_key=component_key,
                        ignore_state_props=component_ignore_labels_,
                    )
                elif component_key == 'Formula-State':  # ! >> formula-state
                    # NOTE: component reference config
                    component_id = create_component_id(
                        component=component
                    ).formula_state

                    # get the component reference config
                    component_reference_config_: Dict[str, ComponentConfig] = \
                        self._set_component_reference_config(
                            component_id=component_id
                    )

                    # >>> get the component reference
                    component_reference_: CustomReference = \
                        self._set_component_reference(
                            component_id=component_id
                        )

                    # >>> get ignore labels
                    # ! by default, empty list
                    component_ignore_labels_: List[str] = self._set_component_ignore_labels(
                        component_id=component_id
                    )

                    # ! by formula (older version)
                    # component_thermodb = ptdb.build_component_thermodb(
                    #     component_name=component_formula,
                    #     reference_config=component_reference_config,
                    #     custom_reference=self.reference,
                    #     component_key='Formula'
                    # )

                    # ! by formula (newer version)
                    component_thermodb = ptdb.check_and_build_component_thermodb(
                        component=component,
                        reference_config=component_reference_config_,
                        custom_reference=component_reference_,
                        component_key=component_key,
                        ignore_state_props=component_ignore_labels_,
                    )
                else:
                    raise ValueError(
                        f"Invalid build mode: {component_key}. Use 'name' or 'formula'.")

                # NOTE: save the component thermodynamic database
                components_thermodb.append(
                    ComponentThermoDB(
                        component=component,
                        thermodb=component_thermodb,
                        component_key=component_key
                    )
                )

            # SECTION: check thermodb items
            if len(components_thermodb) == 1:
                # NOTE: if only one component, return the thermodb directly
                components_thermodb_: ComponentThermoDB = components_thermodb[0]
                return components_thermodb_

            # NOTE: return
            return components_thermodb

        except Exception as e:
            logger.error(
                f"Failed to build thermodynamic database: {e}"
            )
            raise ComponentThermoDBBuildError(
                COMPONENT_THERMODB_BUILD_ERROR_MSG
            ) from e

    def build_model_source(self) -> Dict[str, Dict[str, Any]]:
        """
        Build the model source for the ThermoHub.

        Parameters
        ----------
        None

        Returns
        -------
        model_source : dict
            The model source dictionary.
            - datasource: dict
                Contains the thermodynamic database.
            - equationsource: dict
                Contains the equations of state and their parameters.
        """
        logger.debug("Building model source for ThermoHub")

        try:
            # SECTION: config the thermodb rule
            if self.thermodb_rules is not None:
                logger.debug("Configuring thermodb rule")
                self.thermo_hub.config_thermodb_rule(self.thermodb_rules)

            # SECTION: build the datasource and equationsource
            logger.debug("Building datasource and equationsource")
            datasource, equationsource = self.thermo_hub.build()

            # SECTION: build the model source
            model_source = {
                'datasource': datasource,
                'equationsource': equationsource
            }

            logger.debug("Model source built successfully")
            return model_source

        except Exception as e:
            logger.error(f"Failed to build model source: {e}")
            raise ModelSourceBuildError(
                MODEL_SOURCE_BUILD_ERROR_MSG
            ) from e

    def register_components_thermodb(
        self,
        components_thermodb: List[ComponentThermoDB]
    ) -> bool:
        """
        Register multiple component thermodynamic databases in the ThermoHub.

        Parameters
        ----------
        components_thermodb : List[ComponentThermoDB]
            List of component thermodynamic databases to register.

        Returns
        -------
        bool
            True if registration is successful, False otherwise.
        """
        logger.info(
            f"Registering {len(components_thermodb)} component "
            "thermodynamic databases"
        )

        try:
            # SECTION: loop through each component thermodynamic database
            for i, component_thermodb in enumerate(components_thermodb):
                logger.debug(
                    f"Registering component {i+1}/{len(components_thermodb)}"
                )
                self.register_component_thermodb(component_thermodb)

            logger.info(
                f"Successfully registered {len(components_thermodb)} "
                "component thermodynamic databases"
            )
            return True

        except Exception as e:
            logger.error(
                f"Failed to register components thermodynamic databases: {e}"
            )
            raise HubComponentsThermoDBRegistrationError(
                HUB_COMPONENTS_THERMODB_REGISTRATION_ERROR_MSG
            ) from e

    def build_component_model_source(
        self,
        component: Component,
        component_key: Literal[
            'Name-State', 'Formula-State'
        ] = 'Name-State'
    ) -> Dict[str, Any]:
        """
        Build the model source for a component or list of components.

        Parameters
        ----------
        component : Component
            The component for which to build the model source.
        component_key : Literal['Name-State', 'Formula-State'], optional
            The mode to build the model source, either by 'Name-State' or
            'Formula-State'.
            Default is 'Name-State'.

        Returns
        -------
        Dict[str, Any]
            The model source dictionary.
        """
        logger.info(f"Building model source for component: {component.name}")

        try:
            # SECTION: build the component thermodynamic database
            logger.debug("Building component thermodynamic database")
            components_thermodb = self.build_component_thermodb(
                component=component,
                component_key=component_key
            )

            # SECTION: register the component thermodynamic database
            if isinstance(components_thermodb, ComponentThermoDB):
                # NOTE: if only one component, register it directly
                logger.debug(
                    "Registering single component thermodynamic database"
                )
                self.register_component_thermodb(components_thermodb)
            else:
                # NOTE: if multiple components, register them all
                error_msg = (
                    "Multiple components provided, please register them "
                    "individually."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            # SECTION: build the model source
            logger.debug("Building model source")
            model_source = self.build_model_source()

            logger.info(
                f"Model source built successfully for component: "
                f"{component.name}"
            )
            return model_source

        except Exception as e:
            logger.error(
                f"Failed to build component model source for "
                f"'{component.name}': {e}"
            )
            raise HubComponentModelSourceBuildError(
                HUB_COMPONENT_MODEL_SOURCE_BUILD_ERROR_MSG
            ) from e

    def build_components_model_source(
        self,
        components: List[Component],
        component_key: Literal[
            'Name-State', 'Formula-State'
        ] = 'Name-State'
    ) -> Dict:
        """
        Build the model source for multiple components.

        Parameters
        ----------
        components : List[Component]
            The list of components for which to build the model source.
        component_key : Literal['Name-State', 'Formula-State'], optional
            The mode to build the model source, either by 'Name-State' or
            'Formula-State'.
            Default is 'Name-State'.

        Returns
        -------
        Dict[str, Any]
            The model source dictionary.
        """
        component_names = [comp.name for comp in components]
        logger.info(
            f"Building model source for {len(components)} components: "
            f"{', '.join(component_names)}"
        )

        try:
            # SECTION: build the component thermodynamic databases
            logger.debug("Building component thermodynamic databases")
            components_thermodb = self.build_component_thermodb(
                component=components,
                component_key=component_key
            )

            # SECTION: register the component thermodynamic databases
            if isinstance(components_thermodb, ComponentThermoDB):
                # NOTE: if only one component, register it directly
                error_msg = (
                    "Only one component provided, please use "
                    "build_component_model_source."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)
            else:
                # NOTE: if multiple components, register them all
                logger.debug(
                    "Registering multiple component thermodynamic databases"
                )
                self.register_components_thermodb(components_thermodb)

            # SECTION: build the model source
            logger.debug("Building model source")
            model_source = self.build_model_source()

            logger.info(
                f"Model source built successfully for {len(components)} "
                "components"
            )
            return model_source

        except Exception as e:
            logger.error(
                f"Failed to build components model source for "
                f"{len(components)} components: {e}"
            )
            raise HubComponentsModelSourceBuildError(
                HUB_COMPONENTS_MODEL_SOURCE_BUILD_ERROR_MSG
            ) from e
