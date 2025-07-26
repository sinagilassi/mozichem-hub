# import libs
import logging
from typing import (
    List,
    Dict,
    Any,
    Callable
)
# locals
from ..models import (
    ReferenceThermoDB
)
from .hub import Hub
from .mozi_tool_builder import MoziToolBuilder
from .class_builder import MCPClassBuilder
from ..config import MCP_MODULES
from ..models import MoziTool
# class lists
# from .ptmcore import PTMCore
# from .ptfcore import PTFCore
# from .ptdbcore import PTDBCore


class FunctionDispatcher(MoziToolBuilder, MCPClassBuilder):
    """
    Dispatcher class for defining functions in the MoziChem Hub.
    """
    # NOTE: attributes

    def __init__(
        self,
        reference_thermodb: ReferenceThermoDB,
    ):
        """
        Initialize the Dispatcher instance.

        Parameters
        ----------
        reference_thermodb : ReferenceThermoDB
            ReferenceThermoDB instance containing the thermodynamic database.
        reference : Reference
            Reference instance containing the reference data.
        """
        # LINK: Initialize the MoziToolBuilder
        MoziToolBuilder.__init__(self)
        # LINK: Initialize the MCPClassBuilder
        MCPClassBuilder.__init__(self)

        # SECTION: Initialize the Hub
        self.Hub_ = Hub(
            reference_thermodb=reference_thermodb
        )

    def _init_mcp_class(self, mcp_name: str):
        """
        Initialize the MCP class based on the provided mcp_name.

        Parameters
        ----------
        mcp_name : str
            The name of the MCP to initialize.

        Returns
        -------
        Dict[str, Any]
            The initialized MCP class.
        """
        try:
            # SECTION: get mcp information
            mcp_info = self._select_mcp_by_name(mcp_name)

            # NOTE: mcp id
            mcp_id = mcp_info.get('id', None)
            # check
            if not mcp_id:
                raise ValueError(
                    f"MCP '{mcp_name}' does not have an ID defined."
                )

            # SECTION: init the MCP class
            mcp_class = self.get_mcp_class(mcp_id)
            # check if the class is found
            if not mcp_class:
                raise ValueError(
                    f"MCP class '{mcp_id}' is not registered in the MoziChem Hub."
                )

            # return the initialized MCP class
            if isinstance(mcp_class, type):
                return {
                    mcp_name: mcp_class(self.Hub_)
                }
            else:
                return {
                    mcp_name: mcp_class
                }

        except Exception as e:
            raise Exception(
                f"Failed to initialize MCP class '{mcp_name}': {e}") from e

    def _get_mcp_registered(self) -> Dict[str, Any]:
        """
        Get all registered MCPs in the MoziChem Hub.

        Returns
        -------
        Dict[str, Any]
            Dictionary of MCP names and their implementations.
        """
        try:
            # REVIEW: get all classes starts with 'MCP_' from MCP_MODULES
            # SECTION: get all classes starts with 'MCP_'
            # ! method 1
            # mcp_registered = {
            #     name: getattr(self, name)
            #     for name in dir(self)
            #     if name.startswith("MCP_") and not name.startswith("__")
            # }

            # ! method 2
            # mcp_registered = {
            #     mcp['class']: getattr(self, mcp['class'])
            #     for mcp in MCP_MODULES
            #     if 'name' in mcp and 'class' in mcp
            # }

            # ! method 3
            mcp_registered = {
                mcp['class']: self.get_mcp_class(mcp['id'])
                for mcp in MCP_MODULES
                if 'id' in mcp and 'class' in mcp
            }

            # return
            return mcp_registered
        except Exception as e:
            raise Exception(f"Failed to get MCP registered list: {e}") from e

    def _select_mcp_registered(
            self,
            mcp_name: str
    ):
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
    ) -> Dict[str, Any]:
        """
        Select a specific MCP registered by its class name.

        Parameters
        ----------
        mcp_class : str
            The class name of the MCP to select.

        Returns
        -------
        Dict[str, Any]
            The selected MCP information.
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

    def _select_mcp_by_name(
            self,
            mcp_name: str
    ) -> Dict[str, Any]:
        """
        Select a specific MCP registered by its name.

        Parameters
        ----------
        mcp_name : str
            The name of the MCP to select.

        Returns
        -------
        Dict[str, Any]
            The selected MCP.
        """
        try:
            # SECTION: lookup the name in the registered list
            mcp_selected = next(
                (mcp for mcp in MCP_MODULES if mcp['name'] == mcp_name),
                None
            )

            # check if the mcp_name is found
            if not mcp_selected:
                raise ValueError(
                    f"MCP '{mcp_name}' is not registered in the MoziChem Hub.")

            # return the selected MCP class
            return mcp_selected
        except Exception as e:
            raise Exception(
                f"Failed to select MCP '{mcp_name}': {e}") from e

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
        self,
        mcp_name: str
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
                    # ! check mcp_class is a class
                    if isinstance(mcp_class, type):
                        # initialize the class
                        mcp_instance = mcp_class(self.Hub_)
                        return mcp_instance.list_functions()
                    elif hasattr(mcp_class, 'list_functions'):
                        # if it has a method list_functions, call it
                        return mcp_class.list_functions()
                    else:
                        raise ValueError(
                            f"MCP class '{mcp_class_name}' does not have a method 'list_functions'."
                        )

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

    def retrieve_mozi_tools(self, mcp_name: str) -> List[MoziTool]:
        """
        Get all mozi tools available in the MoziChem Hub.

        Parameters
        ----------
        mcp_name : str
            The name of the mcp to retrieve functions for.

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
