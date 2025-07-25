# import libs
import logging
from typing import (
    Dict,
    Any,
    Callable,
    List,
    Annotated,
    Literal
)
import inspect
from pydantic import Field
import pyThermoFlash as ptf
# local
from ..models import (
    Temperature,
    Pressure,
    Component,
)
from .utils import (
    set_feed_specification,
    get_components_formulas,
)
from .hub import Hub
from ..errors import (
    PTFCalculationError,
    PTFInitializationError,
    PTFModelSourceError,
    PTFFeedSpecificationError,
)

# Configure logger
logger = logging.getLogger(__name__)


class PTFCore:
    """
    Core class for managing pyThermoFlash (PTF) functionalities.
    This class serves as a central point for PTF-related operations.
    """
    # NOTE: attributes
    # id = "PTFCore"

    def __init__(
        self,
        hub: Hub
    ):
        """
        Initialize the PTFCore instance.

        Parameters
        ----------
        hub : Hub
            Instance of the Hub class to manage references and models.
        """
        # NOTE: store the hub instance
        self.hub = hub

    @property
    def id(self):
        return self.__class__.__name__

    def list_functions(self) -> Dict[str, Callable[..., Any]]:
        return {
            name: getattr(self, name)
            for name, obj in inspect.getmembers(
                self.__class__, predicate=inspect.isfunction
            )
            if not name.startswith('__') and name != 'list_functions'
        }

    def calc_bubble_pressure_ideal_vapor_ideal_liquid(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ]
    ) -> str:
        """Calculates the bubble pressure of a mixture of components at a given temperature using Raoult's law (ideal vapor and ideal liquid)."""
        logger.info(
            f"Starting bubble pressure calculation for {len(components)} components at {temperature.value} {temperature.unit}"
        )

        try:
            # SECTION: components id
            # NOTE: formulas
            component_formulas = get_components_formulas(components)
            logger.debug(f"Component formulas: {component_formulas}")

            # SECTION: build model source
            try:
                model_source = self.hub.build_components_model_source(
                    components=components
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTFModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: constants
            # NOTE: equilibrium model
            equilibrium_model = 'raoult'

            # SECTION: initialize ptf
            # NOTE: set components mode: 'formula' or 'name'
            # ! formula
            try:
                vle = ptf.vle(
                    components=component_formulas,
                    model_source=model_source
                )
                logger.debug("PTF VLE initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize PTF VLE: {e}")
                raise PTFInitializationError(
                    f"Failed to initialize PTF VLE: {e}") from e

            # SECTION: set feed specification
            # NOTE: set feed mode: 'formula' or 'name'
            # ! formula
            try:
                N0s = set_feed_specification(
                    components=components,
                    feed_mode="formula"  # or 'name'
                )
                logger.debug(f"Feed specification set: {N0s}")
            except Exception as e:
                logger.error(f"Failed to set feed specification: {e}")
                raise PTFFeedSpecificationError(
                    f"Failed to set feed specification: {e}") from e

            # SECTION: model input
            model_inputs = {
                "mole_fraction": N0s,
                "temperature": [temperature.value, temperature.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = vle.bubble_pressure(
                    inputs=model_inputs,
                    equilibrium_model=equilibrium_model
                )
                logger.info(
                    "Bubble pressure calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTF bubble pressure calculation failed: {e}")
                raise PTFCalculationError(
                    f"PTF bubble pressure calculation failed: {e}") from e

            # return
            return str(res)
        except (
                PTFModelSourceError,
                PTFInitializationError,
                PTFFeedSpecificationError,
                PTFCalculationError):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in bubble pressure calculation: {e}")
            raise PTFCalculationError(
                f"Unexpected error in bubble pressure calculation: {e}"
            ) from e

    def calc_dew_pressure_ideal_vapor_ideal_liquid(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ]
    ) -> str:
        """Calculates the dew pressure of a mixture of components at a given temperature using Raoult's law (ideal vapor and ideal liquid)."""
        logger.info(
            f"Starting dew pressure calculation for {len(components)} components at {temperature.value} {temperature.unit}"
        )

        try:
            # SECTION: components id
            # NOTE: formulas
            component_formulas = get_components_formulas(components)
            logger.debug(f"Component formulas: {component_formulas}")

            # SECTION: build model source
            try:
                model_source = self.hub.build_components_model_source(
                    components=components
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTFModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: constants
            # NOTE: equilibrium model
            equilibrium_model = 'raoult'

            # SECTION: initialize ptf
            # NOTE: set components mode: 'formula' or 'name'
            # ! formula
            try:
                vle = ptf.vle(
                    components=component_formulas,
                    model_source=model_source
                )
                logger.debug("PTF VLE initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize PTF VLE: {e}")
                raise PTFInitializationError(
                    f"Failed to initialize PTF VLE: {e}") from e

            # SECTION: set feed specification
            # NOTE: set feed mode: 'formula' or 'name'
            # ! formula
            try:
                N0s = set_feed_specification(
                    components=components,
                    feed_mode="formula"  # or 'name'
                )
                logger.debug(f"Feed specification set: {N0s}")
            except Exception as e:
                logger.error(f"Failed to set feed specification: {e}")
                raise PTFFeedSpecificationError(
                    f"Failed to set feed specification: {e}") from e

            # SECTION: model input
            model_inputs = {
                "mole_fraction": N0s,
                "temperature": [temperature.value, temperature.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = vle.dew_pressure(
                    inputs=model_inputs,
                    equilibrium_model=equilibrium_model
                )
                logger.info("Dew pressure calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTF dew pressure calculation failed: {e}")
                raise PTFCalculationError(
                    f"PTF dew pressure calculation failed: {e}") from e

            # return
            return str(res)
        except (
                PTFModelSourceError,
                PTFInitializationError,
                PTFFeedSpecificationError,
                PTFCalculationError):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in dew pressure calculation: {e}")
            raise PTFCalculationError(
                f"Unexpected error in dew pressure calculation: {e}"
            ) from e

    def calc_bubble_temperature_ideal_vapor_ideal_liquid(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")
        ],
        solver_method: Annotated[
            Literal['root', 'least-squares', 'fsolve'],
            Field(
                default='root',
                description="Method to use for solving the bubble temperature calculation. Options are 'root', 'least-squares', or 'fsolve'."
            )
        ] = 'root'
    ) -> str:
        """Calculates the bubble temperature of a mixture of components at a given pressure using Raoult's law (ideal vapor and ideal liquid)."""
        logger.info(
            f"Starting bubble temperature calculation for {len(components)} components at {pressure.value} {pressure.unit} using {solver_method} solver"
        )

        try:
            # SECTION: components id
            # NOTE: formulas
            component_formulas = get_components_formulas(components)
            logger.debug(f"Component formulas: {component_formulas}")

            # SECTION: build model source
            try:
                model_source = self.hub.build_components_model_source(
                    components=components
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTFModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: constants
            # NOTE: equilibrium model
            equilibrium_model = 'raoult'

            # SECTION: initialize ptf
            # NOTE: set components mode: 'formula' or 'name'
            # ! formula
            try:
                vle = ptf.vle(
                    components=component_formulas,
                    model_source=model_source
                )
                logger.debug("PTF VLE initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize PTF VLE: {e}")
                raise PTFInitializationError(
                    f"Failed to initialize PTF VLE: {e}") from e

            # SECTION: set feed specification
            # NOTE: set feed mode: 'formula' or 'name'
            # ! formula
            try:
                N0s = set_feed_specification(
                    components=components,
                    feed_mode="formula"  # or 'name'
                )
                logger.debug(f"Feed specification set: {N0s}")
            except Exception as e:
                logger.error(f"Failed to set feed specification: {e}")
                raise PTFFeedSpecificationError(
                    f"Failed to set feed specification: {e}") from e

            # SECTION: model input
            model_inputs = {
                "mole_fraction": N0s,
                "pressure": [pressure.value, pressure.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = vle.bubble_temperature(
                    inputs=model_inputs,
                    equilibrium_model=equilibrium_model,
                    solver_method=solver_method
                )
                logger.info(
                    "Bubble temperature calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTF bubble temperature calculation failed: {e}")
                raise PTFCalculationError(
                    f"PTF bubble temperature calculation failed: {e}") from e

            # return
            return str(res)
        except (
            PTFModelSourceError,
            PTFInitializationError,
            PTFFeedSpecificationError,
            PTFCalculationError
        ):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in bubble temperature calculation: {e}")
            raise PTFCalculationError(
                f"Unexpected error in bubble temperature calculation: {e}"
            ) from e

    def calc_dew_temperature_ideal_vapor_ideal_liquid(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")
        ],
        solver_method: Annotated[
            Literal['root', 'least-squares', 'fsolve'],
            Field(
                default='root',
                description="Method to use for solving the dew temperature calculation. Options are 'root', 'least-squares', or 'fsolve'."
            )
        ] = 'least-squares'
    ) -> str:
        """Calculates the dew temperature of a mixture of components at a given pressure using Raoult's law (ideal vapor and ideal liquid)."""
        logger.info(
            f"Starting dew temperature calculation for {len(components)} components at {pressure.value} {pressure.unit} using {solver_method} solver"
        )

        try:
            # SECTION: components id
            # NOTE: formulas
            component_formulas = get_components_formulas(components)
            logger.debug(f"Component formulas: {component_formulas}")

            # SECTION: build model source
            try:
                model_source = self.hub.build_components_model_source(
                    components=components
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTFModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: constants
            # NOTE: equilibrium model
            equilibrium_model = 'raoult'

            # SECTION: initialize ptf
            # NOTE: set components mode: 'formula' or 'name'
            # ! formula
            try:
                vle = ptf.vle(
                    components=component_formulas,
                    model_source=model_source
                )
                logger.debug("PTF VLE initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize PTF VLE: {e}")
                raise PTFInitializationError(
                    f"Failed to initialize PTF VLE: {e}") from e

            # SECTION: set feed specification
            # NOTE: set feed mode: 'formula' or 'name'
            # ! formula
            try:
                N0s = set_feed_specification(
                    components=components,
                    feed_mode="formula"  # or 'name'
                )
                logger.debug(f"Feed specification set: {N0s}")
            except Exception as e:
                logger.error(f"Failed to set feed specification: {e}")
                raise PTFFeedSpecificationError(
                    f"Failed to set feed specification: {e}") from e

            # SECTION: model input
            model_inputs = {
                "mole_fraction": N0s,
                "pressure": [pressure.value, pressure.unit]
            }
            logger.debug(f"Model inputs: {model_inputs}")

            # SECTION: calc
            try:
                res = vle.dew_temperature(
                    inputs=model_inputs,
                    equilibrium_model=equilibrium_model,
                    solver_method=solver_method
                )
                logger.info(
                    "Dew temperature calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTF dew temperature calculation failed: {e}")
                raise PTFCalculationError(
                    f"PTF dew temperature calculation failed: {e}") from e

            # return
            return str(res)
        except (
            PTFModelSourceError,
            PTFInitializationError,
            PTFFeedSpecificationError,
            PTFCalculationError
        ):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in dew temperature calculation: {e}")
            raise PTFCalculationError(
                f"Unexpected error in dew temperature calculation: {e}"
            ) from e

    def calc_flash_isothermal_ideal_vapor_ideal_liquid(
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
            Field(..., description="Pressure of the system")
        ]
    ) -> str:
        """Calculates the flash calculation for a liquid mixture at a specified temperature, determining the vapor and liquid phase compositions using Raoult's law for ideal vapor and ideal liquid."""
        logger.info(
            f"Starting flash calculation for {len(components)} components at {temperature.value} {temperature.unit} and {pressure.value} {pressure.unit}"
        )

        try:
            # SECTION: components id
            # NOTE: formulas
            component_formulas = get_components_formulas(components)
            logger.debug(f"Component formulas: {component_formulas}")

            # SECTION: build model source
            try:
                model_source = self.hub.build_components_model_source(
                    components=components
                )
                logger.debug("Model source built successfully")
            except Exception as e:
                logger.error(f"Failed to build model source: {e}")
                raise PTFModelSourceError(
                    f"Failed to build model source: {e}") from e

            # SECTION: constants
            # NOTE: equilibrium model
            equilibrium_model = 'raoult'

            # SECTION: initialize ptf
            # NOTE: set components mode: 'formula' or 'name'
            # ! formula
            try:
                vle = ptf.vle(
                    components=component_formulas,
                    model_source=model_source
                )
                logger.debug("PTF VLE initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize PTF VLE: {e}")
                raise PTFInitializationError(
                    f"Failed to initialize PTF VLE: {e}") from e

            # SECTION: set feed specification
            # NOTE: set feed mode: 'formula' or 'name'
            # ! formula
            try:
                N0s = set_feed_specification(
                    components=components,
                    feed_mode="formula"  # or 'name'
                )
                logger.debug(f"Feed specification set: {N0s}")
            except Exception as e:
                logger.error(f"Failed to set feed specification: {e}")
                raise PTFFeedSpecificationError(
                    f"Failed to set feed specification: {e}") from e
            # SECTION: model input
            model_inputs = {
                "mole_fraction": N0s,
                "temperature": [temperature.value, temperature.unit],
                "pressure": [pressure.value, pressure.unit]
            }

            logger.debug(f"Model inputs: {model_inputs}")
            # SECTION: calc
            try:
                res = vle.flash_isothermal(
                    inputs=model_inputs,
                    equilibrium_model=equilibrium_model
                )
                logger.info("Flash calculation completed successfully")
                logger.debug(f"Result: {res}")
            except Exception as e:
                logger.error(f"PTF flash calculation failed: {e}")
                raise PTFCalculationError(
                    f"PTF flash calculation failed: {e}") from e
            # return
            return str(res)
        except (
            PTFModelSourceError,
            PTFInitializationError,
            PTFFeedSpecificationError,
            PTFCalculationError
        ):
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in flash calculation: {e}")
            raise PTFCalculationError(
                f"Unexpected error in flash calculation: {e}"
            ) from e
