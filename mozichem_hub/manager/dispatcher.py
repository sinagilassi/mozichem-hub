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
        self.MCP_PTMCore = PTMCore(self.Hub_)

    def _get_mcp_registered(self) -> Dict[str, Any]:
        """
        Get all registered MCPs in the MoziChem Hub.

        Returns
        -------
        Dict[str, Any]
            Dictionary of MCP names and their implementations.
        """
        try:
            # SECTION: get all classes starts with 'MCP_'
            mcp_registered = {
                name: getattr(self, name)
                for name in dir(self)
                if name.startswith("MCP_") and not name.startswith("__")
            }

            # return
            return mcp_registered
        except Exception as e:
            raise Exception(f"Failed to get MCP registered list: {e}") from e

    def _select_mcp_registered(
            self, mcp_name: str):
        """
        Select a specific MCP registered by its name.
        """
        try:
            # SECTION: get all classes starts with 'MCP_'
            mcp_registered = self._get_mcp_registered()

            # SECTION: check if the mcp_name is in the registered list
            if mcp_name not in mcp_registered:
                raise ValueError(
                    f"MCP '{mcp_name}' is not registered in the MoziChem Hub."
                )

            # return the selected MCP class
            return mcp_registered[mcp_name]
        except Exception as e:
            raise Exception(f"Failed to select MCP '{mcp_name}': {e}") from e

    def _select_mcp_by_class(
            self,
            mcp_class: str
    ):
        """
        Select a specific MCP registered by its class name.
        """
        try:
            # SECTION: lookup the class in the registered list
            mcp_selected = next(
                (mcp for mcp in MCP_MODULES if mcp['class'] == mcp_class),
                None
            )

            # check if the mcp_class is found
            if not mcp_selected:
                raise ValueError(
                    f"MCP class '{mcp_class}' is not registered in the MoziChem Hub.")

            # return the selected MCP class
            return mcp_selected
        except Exception as e:
            raise Exception(
                f"Failed to select MCP class '{mcp_class}': {e}") from e

    def _check_availability_mcp_by_class(
            self,
            mcp_class: str
    ) -> bool:
        """
        Check if a specific MCP class is available in the MoziChem Hub.

        Parameters
        ----------
        mcp_class : str
            The class name of the MCP to check.

        Returns
        -------
        bool
            True if the MCP class is available, False otherwise.
        """
        try:
            # SECTION: lookup the class in the registered list
            mcp_selected = self._select_mcp_by_class(mcp_class)

            # return True if found
            return mcp_selected is not None
        except Exception as e:
            raise Exception(
                f"Failed to check MCP class '{mcp_class}': {e}") from e

    def _get_local_functions(
        self, mcp_name: str
    ) -> Dict[str, Callable[..., Any]]:
        """
        Get all local functions registered for the given mcp.

        Returns
        -------
        Dict[str, Callable[..., Any]]
            Dictionary of local function names and their implementations.
        """
        try:
            # SECTION: get function list from all modules
            # NOTE: get all modules from MCP_MODULES
            module_class = next(
                (
                    module["class"]
                    for module in MCP_MODULES if module["name"] == mcp_name
                ),
                None
            )

            # check if module class is found
            if not module_class:
                raise ValueError(f"MCP module '{mcp_name}' not found.")

            # SECTION: get all classes starts with 'MCP_'
            mcp_registered = self._get_mcp_registered()

            # SECTION: iterate over all modules
            for mcp_class_name, mcp_class in mcp_registered.items():
                # NOTE: check if the class is in module_classes
                if mcp_class_name == module_class:
                    # ! function is registered in the module
                    # ! Dict[str, Callable]
                    # add the class to the functions dict
                    return mcp_class.list_functions()

            raise ValueError(
                f"No functions found for MCP module '{mcp_name}'. "
                "Please check if the module is registered correctly."
            )
        except Exception as e:
            raise Exception(f"Failed to get local function list: {e}") from e

    def _get_all_local_functions(
        self
    ) -> Dict[str, Dict[str, Callable[..., Any]]]:
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

            # SECTION: get all classes starts with 'MCP_'
            mcp_registered = self._get_mcp_registered()

            # SECTION: iterate over all modules
            for mcp_class_name, mcp_class in mcp_registered.items():
                # NOTE: lookup the class in the mcp module
                class_check_ = self._check_availability_mcp_by_class(
                    mcp_class_name
                )

                # check if the class is available
                if not class_check_:
                    # ! class is not available, skip
                    continue

                # NOTE: select mcp by class
                mcp_module = self._select_mcp_by_class(mcp_class_name)
                # mcp name
                mcp_name = mcp_module.get('name', None)

                if not mcp_name:
                    raise ValueError(
                        f"MCP module '{mcp_class_name}' does not have a name defined."
                    )

                # ! function is registered in the module
                # ! Dict[str, Callable]
                # add the class to the functions dict
                functions[mcp_name] = mcp_class.list_functions()

            # return
            return functions
        except Exception as e:
            raise Exception(f"Failed to get local function list: {e}") from e

    def retrieve_mozi_tools(self, mcp_name) -> List[MoziTool]:
        """
        Get all mozi tools available in the MoziChem Hub.

        Returns
        -------
        List[str]
            List of function names.
        """
        try:
            # SECTION: get local function from the Hub
            local_functions: Dict[
                str, Callable[..., Any]
            ] = self._get_local_functions(mcp_name)

            # SECTION: convert to MoziTools
            # NOTE: convert local functions to MoziTools
            # build mozi tools from the functions
            mozi_tools = self.build_mozi_tools(mcp_name, local_functions)

            # return
            return mozi_tools
        except Exception as e:
            raise Exception(f"Failed to get function list: {e}") from e

    def retrieve_all_mozi_tools(self) -> Dict[str, List[MoziTool]]:
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
            local_functions: Dict[str, Any] = self._get_all_local_functions()

            # SECTION: convert to MoziTools
            # NOTE: convert local functions to MoziTools

            # looping through each local function
            for mcp_name, functions in local_functions.items():
                # build mozi tools from the functions
                mozi_tools_ = self.build_mozi_tools(mcp_name, functions)

                # save to mozi_tools dict
                mozi_tools[mcp_name] = mozi_tools_

            # return
            return mozi_tools
        except Exception as e:
            raise Exception(f"Failed to get function list: {e}") from e
