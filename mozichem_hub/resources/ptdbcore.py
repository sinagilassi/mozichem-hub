# import libs
from typing import (
    Annotated,
    Dict,
    Any,
    Callable,
    Union)
import inspect
from pydantic import Field
import pyThermoDB as ptdb
# local
from ..models import (
    Component,
)
from .utils import (
    set_feed_specification,
    get_components_formulas,
    get_components_names,
)
from .hub import Hub


class PTDBCore:
    """
    Core class for managing PyThermoDB (PTDB) functionalities.
    This class serves as a central point for PTDB-related operations.
    """
    # NOTE: attributes
    id = "PTDBCore"

    def __init__(self, hub: Hub):
        """
        Initialize the PTDBCore instance.
        """
        # NOTE: store the hub instance
        self.hub = hub

        # NOTE: initialize the PTDB database
        self.tdb = ptdb.init()

    def list_functions(self) -> Dict[str, Callable[..., Any]]:
        return {
            name: getattr(self, name)
            for name, obj in inspect.getmembers(
                self.__class__, predicate=inspect.isfunction
            )
            if not name.startswith('__') and name != 'list_functions'
        }

    def get_databooks_descriptions(
        self
    ):
        """Get the descriptions of all available databooks in the PTDB database."""
        try:
            # SECTION: get databooks descriptions
            return str(self.tdb.list_descriptions(res_format='json'))
        except Exception as e:
            raise RuntimeError(
                f"Failed to get databooks descriptions: {e}") from e

    def get_databook_information(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ]
    ):
        """Get information about a specific databook."""
        try:
            # SECTION: get databook information
            return str(self.tdb.databook_info(databook, res_format='json'))
        except Exception as e:
            raise RuntimeError(
                f"Failed to get databook information for {databook}: {e}") from e

    def verify_component_availability(
        self,
        component: Annotated[
            Component,
            Field(..., description="Component name and properties")
        ],
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ],
        table: Annotated[
            Union[str, int],
            Field(..., description="Table name or id such as 'Vapor Pressure' or 1")
        ]
    ) -> str:
        """Verify if a component is available in the PTDB database for a specific databook and table."""
        try:
            # NOTE: extract component name
            component_name, _, _ = (
                component.name, component.formula, component.state)

            # SECTION: check availability
            return str(self.tdb.check_component(
                component_name=component_name,
                databook=databook,
                table=table,
                res_format='json',
            ))
        except Exception as e:
            raise RuntimeError(
                f"Failed to verify component availability: {e}") from e

    def search_component_for_thermodynamic_properties(
        self,
        component: Annotated[
            Component,
            Field(..., description="Component name and properties")
        ],
    ) -> str:
        """Search for thermodynamic properties of a component in the PTDB database."""
        try:
            # NOTE: extract component name
            (
                component_name, component_formula, _
            ) = component.name, component.formula, component.state

            # SECTION: search term
            search_terms = [component_name, component_formula]

            # SECTION: check
            res = self.tdb.search_databook(
                search_terms,
                res_format='json',
                search_mode='exact'
            )

            # return
            return str(res)
        except Exception as e:
            raise RuntimeError(
                f"Failed to verify component thermodynamic properties: {e}") from e

    def get_list_databooks(
        self
    ):
        """Get the list of all available databooks in the PTDB database."""
        try:
            # SECTION: get databooks
            return self.tdb.list_databooks()
        except Exception as e:
            raise RuntimeError(f"Failed to list databooks: {e}") from e

    def get_list_tables(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ]
    ):
        """Get the list of all tables in a specific databook."""
        try:
            # SECTION: get tables
            return str(self.tdb.list_tables(databook, res_format='json'))
        except Exception as e:
            raise RuntimeError(
                f"Failed to list tables in {databook}: {e}") from e

    def get_table_information(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ],
        table: Annotated[
            Union[str, int],
            Field(..., description="Table name or id such as 'Vapor Pressure' or 1")
        ]
    ):
        """
        Get information about a specific table in a databook. It returns the table type including Equations, Data, Matrix-Equations, and Matrix-Data.
        Moreover, it returns the number of each type of data in the table.
        """
        try:
            # SECTION: get table information
            return str(self.tdb.table_info(databook, table, res_format='json'))
        except Exception as e:
            raise RuntimeError(
                f"Failed to get table information for {table} in {databook}: {e}") from e

    def get_table_structure(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ],
        table: Annotated[
            Union[str, int],
            Field(..., description="Table name or id such as 'Vapor Pressure' or 1")
        ]
    ):
        """Get the structure of a specific table in a databook."""
        try:
            # SECTION: get table structure
            return str(self.tdb.select_table(databook, table))
        except Exception as e:
            raise RuntimeError(
                f"Failed to get table structure for {table} in {databook}: {e}") from e

    def get_table_data(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ],
        table: Annotated[
            Union[str, int],
            Field(..., description="Table name or id such as 'Vapor Pressure' or 1")
        ]
    ):
        """Get the data of a specific table in a databook."""
        try:
            # SECTION: get table data
            return str(self.tdb.table_data(databook, table, res_format='json'))
        except Exception as e:
            raise RuntimeError(
                f"Failed to get table data for {table} in {databook}: {e}") from e

    def get_databook_id(
        self,
        databook: Annotated[
            str,
            Field(..., description="Databook name such as 'Perry's Chemical Engineers' Handbook'")
        ]
    ) -> str:
        """Get the ID of a specific databook."""
        try:
            # SECTION: get databook ID
            return str(self.tdb.get_databook_id(databook, res_format='json'))
        except Exception as e:
            raise RuntimeError(
                f"Failed to get databook ID for {databook}: {e}") from e

    def get_table_id(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ],
        table: Annotated[
            str,
            Field(..., description="Table name such as 'Vapor Pressure'")
        ]
    ) -> str:
        """Get the ID of a specific table in a databook."""
        try:
            # SECTION: get table ID
            return str(self.tdb.get_table_id(
                databook,
                table,
                res_format='json'
            )
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to get table ID for {table} in {databook}: {e}") from e

    def get_table_description(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ],
        table: Annotated[
            str,
            Field(..., description="Table name such as 'Vapor Pressure'")
        ]
    ) -> str:
        """Get the description of a specific table in a databook."""
        try:
            # SECTION: get table description
            return str(self.tdb.table_description(
                databook,
                table,
                res_format='json'
            )
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to get table description for {table} in {databook}: {e}") from e

    def get_equation_structure(
        self,
        databook: Annotated[
            Union[str, int],
            Field(..., description="Databook name or id such as 'Perry's Chemical Engineers' Handbook' or 1")
        ],
        table: Annotated[
            str,
            Field(..., description="Table name such as 'Vapor Pressure'")
        ]
    ) -> str:
        """Get the equation structure of a specific table in a databook."""
        try:
            # SECTION: get equation structure
            eq_ = self.tdb.equation_load(
                databook,
                table,
            )

            # NOTE: return the equation structure as a string
            return str(eq_.eqs_structure())
        except Exception as e:
            raise RuntimeError(
                f"Failed to get equation structure for {table} in {databook}: {e}") from e
