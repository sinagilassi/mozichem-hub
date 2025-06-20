# import libs
import pyThermoDB as ptdb
import pyThermoLinkDB as ptldb

# locals


class ThermoDB:
    """
    ThermoDB class for building and managing the thermodynamic properties
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the ThermoDB instance.
        """
        # SECTION: Initialize the ThermoLinkDB instance
        # thermodb
        self.thermo_hub = ptldb.init()

    def build_component_thermodb(
        self,
        component_name: str,
        component_formula: str,
        component_state: str
    ) -> dict:
        """
        Build the component thermodynamic database.

        Parameters
        ----------
        component_name : str
            Name of the component.
        component_formula : str
            Chemical formula of the component.
        component_state : str
            State of the component ('g', 'l', 's').

        Returns
        -------
        dict
            A dictionary containing the thermodynamic properties of the component.
        """
        try:
            # Build the thermodynamic database for the component
            thermodb = ptdb.build_component_thermodb(
                component_name=component_name,
                property_source=property_source,

            )
            return thermodb
        except Exception as e:
            raise ValueError(
                f"Failed to build thermodynamic database: {e}") from e
    )
