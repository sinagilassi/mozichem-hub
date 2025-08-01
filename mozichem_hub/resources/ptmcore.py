# import libs
import logging
from typing import (
    Dict,
    Any,
    Callable,
    List,
)
import inspect
from typing import Annotated, Literal
from pydantic import Field
import pyThermoModels as ptm
# local
from ..models import (
    Temperature,
    Pressure,
    Component,
)
from .utils import set_feed_specification
from .hub import Hub
from ..descriptors import MCPDescriptor
# from ..config import MCP_MODULES
from .reference_utils import initialize_custom_reference
from ..errors import (
    PTMCalculationError,
    PTMInitializationError,
    PTMModelSourceError,
    PTMComponentError,
    PTMFeedSpecificationError,
    PTMReferenceError,
    PTMFugacityError,
    PTMRootsAnalysisError,
)

# Configure logger
logger = logging.getLogger(__name__)


class PTMCore:
    """
    Core class for managing pyThermoModels (PTM) functionalities.
    This class serves as a central point for PTM-related operations.
    """
    # NOTE: attributes

    def __init__(
        self,
        hub: Hub
    ):
        """
        Initialize the PTMCore instance.

        Parameters
        ----------
        hub : Hub
            Instance of the Hub class to manage references and models.
        """
        # NOTE: store the hub instance
        self.hub = hub

        # SECTION: build eos
        self.eos = ptm.eos()

    @property
    def id(self):
        return self.__class__.__name__

    def list_functions(self) -> Dict[str, Callable[..., Any]]:
        """List all functions in the PTMCore class."""
        return {
            name: getattr(self, name)
            for name, obj in inspect.getmembers(
                self.__class__, predicate=inspect.isfunction
            )
            if not name.startswith('__') and name != 'list_functions'
        }

    def get_method_dependencies(self, method_name: str) -> Dict[str, Any]:
        """
        Get the method dependencies for a specific PTMCore method.

        Parameters
        ----------
        method_name : str
            Name of the method to get dependencies for.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the method dependencies.
        """
        # SECTION: get dependencies
        dependencies = MCPDescriptor.mcp_method_dependencies(
            mcp_id=self.id,
            method_name=method_name
        )

        # NOTE: check if dependencies are empty
        if not dependencies:
            raise ValueError(
                f"No dependencies found for method '{method_name}' in PTMCore."
            )

        # return dependencies
        return dependencies

    def get_method_reference_config(self, method_name: str) -> Dict[str, Any]:
        """
        Get the method reference config for a specific PTMCore method.

        Parameters
        ----------
        method_name : str
            Name of the method to get configuration for.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the method configuration.
        """
        # SECTION: get config
        config = MCPDescriptor.mcp_method_reference_config(
            mcp_id=self.id,
            method_name=method_name
        )

        # NOTE: check if config is empty
        if not config:
            raise ValueError(
                f"No configuration found for method '{method_name}' in PTMCore."
            )

        # return config
        return config

    def get_method_reference_inputs(self, method_name: str) -> Dict[str, Any]:
        """
        Get the method summary for a specific PTMCore method. It provides which inputs are required for the method. These inputs should be defined in the reference content.

        Parameters
        ----------
        method_name : str
            Name of the method to get summary for.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the method summary.
        """
        # SECTION: get summary
        reference_inputs = MCPDescriptor.mcp_method_reference_inputs(
            mcp_id=self.id,
            method_name=method_name
        )

        # NOTE: check if summary is empty
        if not reference_inputs:
            raise ValueError(
                f"No summary found for method '{method_name}' in PTMCore."
            )

        # return summary
        return reference_inputs

    def calc_gas_component_fugacity(
        self,
        component: Annotated[
            Component,
            Field(..., description="Component name and properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")],
        eos_model: Annotated[
            Literal['PR', 'SRK', 'RK', 'vdW'],
            Field(description="EOS model to use, e.g., 'SRK', 'PR'", default="SRK")
        ],
        solver_method: Annotated[
            Literal['ls', 'fsolve', 'root'],
            Field(
                description="Solver method for fugacity calculation, e.g., 'least-square method', 'fsolve', 'root'",
                default="fsolve"
            )
        ] = "ls",
        custom_reference_content: Annotated[
            str,
            Field(
                default='None',
                description=(
                    "Custom reference content provided by PyThermoDB, this consists of data and equations for all components."
                )
            )
        ] = 'None',
        custom_reference_config: Annotated[
            str,
            Field(
                default='None',
                description=(
                    "Custom reference configuration provided by PyThermoDB, this consists of the reference for data and equations for each component."
                )
            )
        ] = 'None'
    ) -> dict:
        """Calculates the fugacity of a gas-phase component at given temperature and pressure"""
        logger.info(
            f"Starting gas component fugacity calculation for {component.name} using {eos_model} EOS at {temperature.value} {temperature.unit}, {pressure.value} {pressure.unit}"
        )

        try:
            # NOTE: extract component name
            (
                component_name, _, _
            ) = component.name, component.formula, component.state
            logger.debug(
                f"Component details: {component_name}, {component.formula}, {component.state}")

            # component name - state
            component_ = f"{component_name}-{component.state}"

            # SECTION: reinitialize hub if needed
            # NOTE: this is to ensure that the hub is initialized with custom reference content and config
            try:
                self.hub = initialize_custom_reference(
                    hub=self.hub,
                    components=component,
                    custom_reference_content=custom_reference_content,
                    custom_reference_config=custom_reference_config
                )
                logger.debug("Custom reference initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize custom reference: {e}")
                raise PTMReferenceError(
                    f"Failed to initialize custom reference: {e}") from e

            # SECTION: build model source
            try:
                model_source = self.hub.build_component_model_source(
                    component=component
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTMModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: model input
            model_inputs = {
                "component": component_,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = self.eos.cal_fugacity(
                    model_name=eos_model,
                    model_input=model_inputs,
                    model_source=model_source,
                    solver_method=solver_method
                )
                logger.info(
                    "Gas component fugacity calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTM fugacity calculation failed: {e}")
                raise PTMFugacityError(
                    f"PTM fugacity calculation failed: {e}") from e

            # return
            return res
        except (
            PTMReferenceError,
            PTMModelSourceError,
            PTMFugacityError
        ):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in gas component fugacity calculation: {e}")
            raise PTMCalculationError(
                f"Unexpected error in gas component fugacity calculation: {e}"
            ) from e

    def calc_liquid_component_fugacity(
        self,
        component: Annotated[
            Component,
            Field(..., description="Component name and properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")],
        eos_model: Annotated[
            Literal['PR', 'SRK', 'RK', 'vdW'],
            Field(description="EOS model to use, e.g., 'SRK', 'PR'", default="SRK")
        ],
        solver_method: Annotated[
            Literal['ls', 'fsolve', 'root'],
            Field(
                description="Solver method for fugacity calculation, e.g., 'least-square method', 'fsolve', 'root'",
                default="fsolve"
            )
        ] = "ls",
        liquid_fugacity_mode: Annotated[
            Literal['EOS', 'Poynting'],
            Field(
                description="Mode for liquid fugacity calculation, 'EOS' or 'Poynting'",
                default="EOS"
            )
        ] = "EOS"
    ) -> dict:
        """Calculates the fugacity of a liquid-phase component at given temperature and pressure"""
        logger.info(
            f"Starting liquid component fugacity calculation for {component.name} using {eos_model} EOS at {temperature.value} {temperature.unit}, {pressure.value} {pressure.unit}"
        )

        try:
            # NOTE: extract component name
            (
                component_name, _, _
            ) = component.name, component.formula, component.state
            logger.debug(
                f"Component details: {component_name}, {component.formula}, {component.state}")

            # component name - state
            component_ = f"{component_name}-{component.state}"

            # SECTION: build model source
            try:
                model_source = self.hub.build_component_model_source(
                    component=component
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTMModelSourceError(
                    f"Failed to build model source: {e}") from e

            # NOTE: set phase
            phase = "LIQUID"

            # SECTION: model input
            model_inputs = {
                "phase": phase,
                "component": component_,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = self.eos.cal_fugacity(
                    model_name=eos_model,
                    model_input=model_inputs,
                    model_source=model_source,
                    liquid_fugacity_mode=liquid_fugacity_mode,
                    solver_method=solver_method
                )
                logger.info(
                    "Liquid component fugacity calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTM liquid fugacity calculation failed: {e}")
                raise PTMFugacityError(
                    f"PTM liquid fugacity calculation failed: {e}") from e

            # return
            return res
        except (PTMModelSourceError, PTMFugacityError):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in liquid component fugacity calculation: {e}")
            raise PTMCalculationError(
                f"Unexpected error in liquid component fugacity calculation: {e}"
            ) from e

    def calc_fugacity_gas_mixture(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")],
        eos_model: Annotated[
            Literal['PR', 'SRK', 'RK', 'vdW'],
            Field(description="EOS model to use, e.g., 'SRK', 'PR'", default="SRK")
        ],
    ) -> dict:
        """Calculates the fugacity of a gaseous mixture of components at given temperature and pressure."""
        logger.info(
            f"Starting gas mixture fugacity calculation for {len(components)} components using {eos_model} EOS at {temperature.value} {temperature.unit}, {pressure.value} {pressure.unit}"
        )

        try:
            # SECTION: set feed specification
            try:
                N0s = set_feed_specification(
                    components=components,
                    feed_mode="formula"
                )
                logger.debug(f"Feed specification set: {N0s}")
            except Exception as e:
                logger.error(f"Failed to set feed specification: {e}")
                raise PTMFeedSpecificationError(
                    f"Failed to set feed specification: {e}") from e

            # SECTION: build model source
            try:
                model_source = self.hub.build_components_model_source(
                    components=components
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTMModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: model input
            model_inputs = {
                "feed-specification": N0s,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = self.eos.cal_fugacity_mixture(
                    model_name=eos_model,
                    model_input=model_inputs,
                    model_source=model_source
                )
                logger.info(
                    "Gas mixture fugacity calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(
                    f"PTM gas mixture fugacity calculation failed: {e}")
                raise PTMFugacityError(
                    f"PTM gas mixture fugacity calculation failed: {e}") from e

            # return
            return res
        except (
            PTMFeedSpecificationError,
            PTMModelSourceError,
            PTMFugacityError
        ):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in gas mixture fugacity calculation: {e}")
            raise PTMCalculationError(
                f"Unexpected error in gas mixture fugacity calculation: {e}"
            ) from e

    def component_eos_roots_analysis(
        self,
        component: Annotated[
            Component,
            Field(..., description="Component name and properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")],
        eos_model: Annotated[
            Literal['PR', 'SRK', 'RK', 'vdW'],
            Field(description="EOS model to use, e.g., 'SRK', 'PR'", default="SRK")
        ]
    ) -> dict:
        """Analyzes the roots of the EOS for a given component at specified temperature and pressure."""
        logger.info(
            f"Starting EOS roots analysis for {component.name} using {eos_model} EOS at {temperature.value} {temperature.unit}, {pressure.value} {pressure.unit}"
        )

        try:
            # NOTE: extract component name
            (
                component_name, _, _
            ) = component.name, component.formula, component.state
            logger.debug(
                f"Component details: {component_name}, {component.formula}, {component.state}")

            # SECTION: build model source
            try:
                model_source = self.hub.build_component_model_source(
                    component=component
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTMModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: model input
            model_inputs = {
                "component": f"{component_name}-{component.state}",
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = self.eos.check_eos_roots_single_component(
                    model_name=eos_model,
                    model_input=model_inputs,
                    model_source=model_source
                )
                logger.info("EOS roots analysis completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTM EOS roots analysis failed: {e}")
                raise PTMRootsAnalysisError(
                    f"PTM EOS roots analysis failed: {e}") from e

            # return
            return res
        except (
            PTMModelSourceError,
            PTMRootsAnalysisError
        ):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in EOS roots analysis: {e}")
            raise PTMCalculationError(
                f"Unexpected error in EOS roots analysis: {e}"
            ) from e

    def multi_component_eos_roots_analysis(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")],
        eos_model: Annotated[
            Literal['PR', 'SRK', 'RK', 'vdW'],
            Field(description="EOS model to use, e.g., 'SRK', 'PR'", default="SRK")
        ]
    ) -> dict:
        """Analyzes the roots of the EOS for a mixture of components at specified temperature and pressure."""
        logger.info(
            f"Starting multi-component EOS roots analysis for {len(components)} components using {eos_model} EOS at {temperature.value} {temperature.unit}, {pressure.value} {pressure.unit}"
        )

        try:
            # SECTION: set feed specification
            try:
                N0s = set_feed_specification(
                    components=components,
                    feed_mode="formula"
                )
                logger.debug(f"Feed specification set: {N0s}")
            except Exception as e:
                logger.error(f"Failed to set feed specification: {e}")
                raise PTMFeedSpecificationError(
                    f"Failed to set feed specification: {e}") from e

            # SECTION: build model source
            try:
                model_source = self.hub.build_components_model_source(
                    components=components
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTMModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: model input
            model_inputs = {
                "feed-specification": N0s,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = self.eos.check_eos_roots_multi_component(
                    model_name=eos_model,
                    model_input=model_inputs,
                    model_source=model_source
                )
                logger.info(
                    "Multi-component EOS roots analysis completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(
                    f"PTM multi-component EOS roots analysis failed: {e}")
                raise PTMRootsAnalysisError(
                    f"PTM multi-component EOS roots analysis failed: {e}") from e

            # return
            return res
        except (
            PTMFeedSpecificationError,
            PTMModelSourceError,
            PTMRootsAnalysisError
        ):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in multi-component EOS roots analysis: {e}")
            raise PTMCalculationError(
                f"Unexpected error in multi-component EOS roots analysis: {e}"
            ) from e
