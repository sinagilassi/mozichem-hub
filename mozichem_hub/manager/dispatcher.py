# import libs
from typing import (
    List,
    Dict,
    Annotated,
    Literal,
    Optional,
    Any,
    Callable
)
# locals
from ..references import (
    Reference,
    ReferenceLink,
    ReferenceThermoDB
)
from .hub import Hub
from .ptmcore import PTMCore
from .builder import ToolBuilder
from ..config import MCP_MODULES
from .models import MoziTool


class FunctionDispatcher(ToolBuilder):
    """
    Dispatcher class for defining functions in the MoziChem Hub.
    """
    # NOTE: attributes

    def __init__(
        self,
        reference_thermodb: ReferenceThermoDB,
        reference: Reference,
        reference_link: ReferenceLink
    ):
        """
        Initialize the Dispatcher instance.

        Parameters
        ----------
        reference_thermodb : ReferenceThermoDB
            ReferenceThermoDB instance containing the thermodynamic database.
        reference : Reference
            Reference instance containing the reference data.
        reference_link : ReferenceLink
            ReferenceLink instance containing the reference link data.
        """
        # SECTION: Initialize the ToolBuilder
        ToolBuilder.__init__(self)

        # SECTION: Initialize the Hub
        self.Hub_ = Hub(
            reference_thermodb=reference_thermodb,
            reference=reference,
            reference_link=reference_link
        )

        # SECTION: Initialize function source
        # ptm
        self.MCP_PTMCore_ = PTMCore(self.Hub_)

    def _get_local_functions(self) -> Dict[str, Dict[str, Callable[..., Any]]]:
        """
        Get all local functions available in the MoziChem Hub.

        Returns
        -------
        Dict[str, Any]
            Dictionary of local function names and their implementations.
        """
        try:
            # NOTE: init dict
            functions = {}

            # SECTION: get function list from all modules
            # NOTE: get all modules from MCP_MODULES
            module_classes = [
                module["class"] for module in MCP_MODULES
            ]

            # SECTION: get all classes starts with 'MCP_'
            mcp_registered = {
                name: getattr(self, name)
                for name in dir(self)
                if name.startswith("MCP_") and not name.startswith("__")
            }

            # SECTION: iterate over all modules
            for mcp_name, mcp_class in mcp_registered.items():
                # NOTE: check if the class is in module_classes
                if mcp_name in module_classes:
                    # ! function is registered in the module
                    # ! Dict[str, Callable]
                    # add the class to the functions dict
                    functions[mcp_name] = mcp_class.list_functions()

            # return
            return functions
        except Exception as e:
            raise Exception(f"Failed to get local function list: {e}") from e

    def retrieve_mozi_tools(self) -> Dict[str, List[MoziTool]]:
        """
        Get all mozi tools available in the MoziChem Hub.

        Returns
        -------
        List[str]
            List of function names.
        """
        try:
            # NOTE:
            mozi_tools: Dict[str, List[MoziTool]] = {}

            # SECTION: get local function from the Hub
            local_functions: Dict[str, Any] = self._get_local_functions()

            # SECTION: convert to MoziTools
            # NOTE: convert local functions to MoziTools

            # looping through each local function
            for mcp_name, functions in local_functions.items():
                # build mozi tools from the functions
                mozi_tools_ = self.build_mozi_tools(functions)

                # save to mozi_tools dict
                mozi_tools[mcp_name] = mozi_tools_

            # return
            return mozi_tools
        except Exception as e:
            raise Exception(f"Failed to get function list: {e}") from e
