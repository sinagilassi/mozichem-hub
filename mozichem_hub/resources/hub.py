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
import pyThermoLinkDB as ptldb
# locals
from ..models import (
    Component,
    ComponentThermoDB,
)
from ..models import (
    ReferenceThermoDB
)
from ..errors import (
    HubInitializationError,
    HubThermoHubBuildError,
    HubThermoHubCleanError,
    HubComponentReferenceConfigError,
    HubComponentReferenceRuleError,
    HubComponentThermoDBRegistrationError,
    HubComponentsThermoDBRegistrationError,
    ComponentThermoDBBuildError,
    ModelSourceBuildError,
    HubComponentModelSourceBuildError,
    HubComponentsModelSourceBuildError,
    HUB_INITIALIZATION_ERROR_MSG,
    HUB_THERMO_HUB_BUILD_ERROR_MSG,
    HUB_THERMO_HUB_CLEAN_ERROR_MSG,
    HUB_COMPONENT_REFERENCE_CONFIG_ERROR_MSG,
    HUB_COMPONENT_REFERENCE_RULE_ERROR_MSG,
    HUB_COMPONENT_THERMODB_REGISTRATION_ERROR_MSG,
    HUB_COMPONENTS_THERMODB_REGISTRATION_ERROR_MSG,
    COMPONENT_THERMODB_BUILD_ERROR_MSG,
    MODEL_SOURCE_BUILD_ERROR_MSG,
    HUB_COMPONENT_MODEL_SOURCE_BUILD_ERROR_MSG,
    HUB_COMPONENTS_MODEL_SOURCE_BUILD_ERROR_MSG
)

# Configure logger
logger = logging.getLogger(__name__)


class Hub:
    """
    Hub class for building and managing the thermodynamic properties
    """
    # NOTE: attributes

    def __init__(
            self,
            reference_thermodb: ReferenceThermoDB,
    ):
        """
        Initialize the Hub instance.
        """
        logger.info("Initializing Hub instance")

        try:
            # NOTE: set
            self.reference_thermodb = reference_thermodb
            # LINK: set the references
            self.reference: Dict[str, Any] = reference_thermodb.reference
            # LINK: content of the reference thermodynamic database
            # ! [not used]
            self.reference_contents: List[str] = reference_thermodb.contents
            # LINK: configuration for the thermodynamic database
            # ! [consists ALL and component-specific configurations]
            self.reference_config: Dict[
                str, Dict[str, Dict[str, str]]
            ] = reference_thermodb.config
            # LINK: rule for the thermodynamic database
            # ! [consists ALL and component-specific configurations]
            self.thermodb_rule: Dict[
                str, Dict[str, Dict[str, str]]
            ] = reference_thermodb.link

            # SECTION: Initialize the ThermoHub
            logger.debug("Building ThermoHub instance")
            self.thermo_hub = self.build_thermo_hub()

            logger.info("Hub instance initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Hub: {e}")
            raise HubInitializationError(HUB_INITIALIZATION_ERROR_MSG) from e

    def _set_component_reference_config(
        self,
        component_id: str
    ) -> Dict[str, Dict[str, str]]:
        """
        Set the reference configuration for a specific component.
        Parameters
        ----------
        component_id : str
            The ID of the component for which to set the reference
            configuration.
        Returns
        -------
        Dict[str, Dict[str, str]]
            The reference configuration for the specified component.
        """
        logger.debug(f"Setting reference config for component: {component_id}")

        try:
            # SECTION: get the reference configuration for the component
            component_reference_config = self.reference_config.get(
                component_id,
                None
            )

            # NOTE: if not found, get ALL
            if component_reference_config is None:
                logger.debug(
                    f"Component '{component_id}' config not found, "
                    "using ALL config"
                )
                component_reference_config = self.reference_config.get(
                    'ALL',
                    None
                )

                # check if ALL is also not found
                if component_reference_config is None:
                    error_msg = (
                        f"Component '{component_id}' not found in "
                        "the reference configuration."
                    )
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            # SECTION: return the reference configuration
            logger.debug(
                f"Reference config set successfully for "
                f"component: {component_id}"
            )
            return component_reference_config

        except Exception as e:
            logger.error(
                f"Failed to set component reference config for "
                f"'{component_id}': {e}"
            )
            raise HubComponentReferenceConfigError(
                HUB_COMPONENT_REFERENCE_CONFIG_ERROR_MSG
            ) from e

    def _set_component_reference_rule(
        self,
        component_id: str
    ) -> Dict[str, Dict[str, str]]:
        """
        Set the reference rule for a specific component.

        Parameters
        ----------
        component_id : str
            The ID of the component for which to set the reference rule.

        Returns
        -------
        Dict[str, Dict[str, str]]
            The reference rule for the specified component, or None if not
            found.
        """
        logger.debug(f"Setting reference rule for component: {component_id}")

        try:
            # SECTION: get the reference rule for the component
            component_reference_rule = self.thermodb_rule.get(
                component_id, None)

            # NOTE: if not found, get ALL
            if component_reference_rule is None:
                logger.debug(
                    f"Component '{component_id}' rule not found, "
                    "using ALL rule"
                )
                component_reference_rule = self.thermodb_rule.get(
                    'ALL', None)

                # check if ALL is also not found
                if component_reference_rule is None:
                    error_msg = (
                        f"Component '{component_id}' not found in "
                        "the reference rule."
                    )
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            logger.debug(
                f"Reference rule set successfully for "
                f"component: {component_id}"
            )
            return component_reference_rule

        except Exception as e:
            logger.error(
                f"Failed to set component reference rule for "
                f"'{component_id}': {e}"
            )
            raise HubComponentReferenceRuleError(
                HUB_COMPONENT_REFERENCE_RULE_ERROR_MSG
            ) from e

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
            - build_mode: Literal['name', 'formula']

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
            # build_mode = component_thermodb.build_mode

            # NOTE: extract component name
            component_name = component.name.strip()
            component_formula = component.formula.strip()
            component_state = component.state.strip().lower()

            # NOTE: set name
            name_ = f"{component_name}-{component_state}"
            formula_ = f"{component_formula}-{component_state}"

            logger.debug(f"Registering component: {name_} / {formula_}")

            # SECTION: create component reference rule
            # ! by name
            component_reference_rule_by_name = \
                self._set_component_reference_rule(
                    component_id=name_
                )
            # ! by formula
            component_reference_rule_by_formula = \
                self._set_component_reference_rule(
                    component_id=formula_
                )

            # SECTION: register the component thermodynamic database
            # NOTE: by name
            self.thermo_hub.add_thermodb(
                name=name_,
                data=thermodb,
                rules=component_reference_rule_by_name
            )

            # NOTE: by formula
            self.thermo_hub.add_thermodb(
                name=formula_,
                data=thermodb,
                rules=component_reference_rule_by_formula
            )

            logger.debug(
                f"Component thermodynamic database registered "
                f"successfully: {name_} / {formula_}"
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
        build_mode: Literal[
            'name', 'formula'
        ] = 'name'
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
        build_mode : Literal['name', 'formula'], optional
            The mode to build the thermodynamic database, either by 'name'
            or 'formula'.
            Default is 'name'.

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
                if build_mode == 'name':
                    # NOTE: component reference config
                    component_id = f"{component_name}-{component_state}"

                    # !get the component reference config
                    component_reference_config = \
                        self._set_component_reference_config(
                            component_id=component_id
                        )

                    # ! by name
                    component_thermodb = ptdb.build_component_thermodb(
                        component_name=component_name,
                        reference_config=component_reference_config,
                        custom_reference=self.reference

                    )
                elif build_mode == 'formula':
                    # NOTE: component reference config
                    component_id = f"{component_formula}-{component_state}"

                    # get the component reference config
                    component_reference_config = \
                        self._set_component_reference_config(
                            component_id=component_id
                        )

                    # ! by formula
                    component_thermodb = ptdb.build_component_thermodb(
                        component_name=component_formula,
                        reference_config=component_reference_config,
                        custom_reference=self.reference
                    )
                else:
                    raise ValueError(
                        f"Invalid build mode: {build_mode}. Use 'name' or 'formula'.")

                # NOTE: save the component thermodynamic database
                components_thermodb.append(
                    ComponentThermoDB(
                        component=component,
                        thermodb=component_thermodb,
                        build_mode=build_mode
                    )
                )

            # SECTION: check thermodb items
            if len(components_thermodb) == 1:
                # NOTE: if only one component, return the thermodb directly
                components_thermodb_ = components_thermodb[0]
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
            if self.thermodb_rule is not None:
                logger.debug("Configuring thermodb rule")
                self.thermo_hub.config_thermodb_rule(self.thermodb_rule)

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
        build_mode: Literal[
            'name', 'formula'
        ] = 'name'
    ) -> Dict[str, Any]:
        """
        Build the model source for a component or list of components.

        Parameters
        ----------
        component : Component
            The component for which to build the model source.
        build_mode : Literal['name', 'formula'], optional
            The mode to build the model source, either by 'name' or 'formula'.
            Default is 'name'.

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
                build_mode=build_mode
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
        build_mode: Literal[
            'name', 'formula'
        ] = 'name'
    ) -> Dict:
        """
        Build the model source for multiple components.

        Parameters
        ----------
        components : List[Component]
            The list of components for which to build the model source.
        build_mode : Literal['name', 'formula'], optional
            The mode to build the model source, either by 'name' or 'formula'.
            Default is 'name'.

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
                build_mode=build_mode
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
