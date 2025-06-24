# import libs
from typing import (
    Literal,
    List,
    Optional,
    Tuple,
    Dict,
    Union,
    Any
)
import pyThermoDB as ptdb
import pyThermoLinkDB as ptldb
# locals
from .models import (
    Component,
    ComponentThermoDB,
)
from ..references import (
    Reference,
    ReferenceLink,
    ReferenceThermoDB
)


class Hub:
    """
    Hub class for building and managing the thermodynamic properties
    """
    # NOTE: attributes

    def __init__(
            self,
            reference_thermodb: ReferenceThermoDB,
            reference: Reference,
            reference_link: ReferenceLink
    ):
        """
        Initialize the Hub instance.
        """
        # NOTE: set
        self.reference_thermodb = reference_thermodb
        # Reference for the thermodynamic database
        self.reference = reference
        # content of the reference thermodynamic database
        self.reference_content = reference.content
        # Configuration for the thermodynamic database
        self.reference_config = reference.config
        # Rule for the thermodynamic database
        self.thermodb_rule = reference_link.rule

        # SECTION: Initialize the ThermoHub
        self.thermo_hub = self.build_thermo_hub()

    def build_thermo_hub(self):
        """
        Initialize the ThermoHub instance.
        """
        try:
            # Initialize the ThermoHub
            self.thermo_hub = ptldb.init()
            return self.thermo_hub
        except Exception as e:
            raise ValueError(
                f"Failed to initialize ThermoHub: {e}") from e

    def clean_thermo_hub(self):
        """
        Clean the ThermoHub, it remains.
        """
        try:
            # clean the ThermoHub
            self.thermo_hub.clean()
        except Exception as e:
            raise ValueError(
                f"Failed to clean ThermoHub: {e}") from e

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

            # SECTION: register the component thermodynamic database
            # NOTE: by name
            self.thermo_hub.add_thermodb(
                name_,
                thermodb
            )

            # NOTE: by formula
            self.thermo_hub.add_thermodb(
                formula_,
                thermodb
            )

            return True
        except Exception as e:
            raise ValueError(
                f"Failed to register component thermodynamic database: {e}"
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
            The component or list of components for which to build the thermodynamic database.
            - If a single Component is provided, it will be treated as a single component.
            - If a list of Components is provided, each item must be a Component.
        build_mode : Literal['name', 'formula'], optional
            The mode to build the thermodynamic database, either by 'name' or 'formula'.
            Default is 'name'.

        Returns
        -------
        Union[ComponentThermoDB, List[ComponentThermoDB]]
            The component thermodynamic database.
        """
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

            # NOTE: loop through each component
            for component in component_:
                # NOTE: input configuration
                component_name = component.name.strip()
                component_formula = component.formula.strip()
                component_state = component.state.strip().lower()

                # SECTION: build the component thermodynamic database
                # NOTE: check build mode
                if build_mode == 'name':
                    # ! by name
                    component_thermodb = ptdb.build_component_thermodb(
                        component_name=component_name,
                        property_source=self.reference_config,
                        custom_reference=self.reference_thermodb.reference

                    )
                elif build_mode == 'formula':
                    # ! by formula
                    component_thermodb = ptdb.build_component_thermodb(
                        component_name=component_formula,
                        property_source=self.reference_config,
                        custom_reference=self.reference_thermodb.reference
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
            raise ValueError(
                f"Failed to build thermodynamic database: {e}") from e

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
        try:
            # SECTION: config the thermodb rule
            if self.thermodb_rule is not None:
                self.thermo_hub.config_thermodb_rule(self.thermodb_rule)

            # SECTION: build the datasource and equationsource
            datasource, equationsource = self.thermo_hub.build()

            # SECTION: build the model source
            model_source = {
                'datasource': datasource,
                'equationsource': equationsource
            }

            return model_source
        except Exception as e:
            raise ValueError(
                f"Failed to build model source: {e}") from e

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
        try:
            # SECTION: loop through each component thermodynamic database
            for component_thermodb in components_thermodb:
                self.register_component_thermodb(component_thermodb)

            return True
        except Exception as e:
            raise ValueError(
                f"Failed to register components thermodynamic databases: {e}"
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
        try:
            # SECTION: build the component thermodynamic database
            components_thermodb = self.build_component_thermodb(
                component=component,
                build_mode=build_mode
            )

            # SECTION: register the component thermodynamic database
            if isinstance(components_thermodb, ComponentThermoDB):
                # NOTE: if only one component, register it directly
                self.register_component_thermodb(components_thermodb)
            else:
                # NOTE: if multiple components, register them all
                raise ValueError(
                    "Multiple components provided, please register them individually."
                )

            # SECTION: build the model source
            model_source = self.build_model_source()

            return model_source
        except Exception as e:
            raise ValueError(
                f"Failed to build component model source: {e}") from e

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
        try:
            # SECTION: build the component thermodynamic databases
            components_thermodb = self.build_component_thermodb(
                component=components,
                build_mode=build_mode
            )

            # SECTION: register the component thermodynamic databases
            if isinstance(components_thermodb, ComponentThermoDB):
                # NOTE: if only one component, register it directly
                raise ValueError(
                    (
                        "Only one component provided, please use "
                        "build_component_model_source."
                    )
                )
            else:
                # NOTE: if multiple components, register them all
                self.register_components_thermodb(components_thermodb)

            # SECTION: build the model source
            model_source = self.build_model_source()

            return model_source
        except Exception as e:
            raise ValueError(
                f"Failed to build components model source: {e}") from e
