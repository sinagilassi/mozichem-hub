# import libs
from typing import Dict, Callable, Optional
# local
from .builder import ToolBuilder
from ..manager import FunctionDispatcher
from ..references import (
    ReferenceThermoDB,
    Reference,
    ReferenceLink
)


class ToolManager(ToolBuilder):
    """
    ToolManager class for managing tools in the MoziChem Hub.
    """
    # NOTE: attributes
    _tools = []

    def __init__(
        self,
        reference_thermodb: ReferenceThermoDB,
        reference: Reference,
        reference_link: ReferenceLink
    ):
        """
        Initialize the ToolManager instance.
        """
        # SECTION: Initialize the Builder
        ToolBuilder().__init__()

        # SECTION: set references
        self._reference_thermodb = reference_thermodb
        self._reference = reference
        self._reference_link = reference_link

        # SECTION: init FunctionDispatcher
        self.FunctionDispatcher_ = FunctionDispatcher(
            reference_thermodb=self._reference_thermodb,
            reference=self._reference,
            reference_link=self._reference_link
        )

    def _retrieve_functions(self) -> Dict[str, Callable]:
        """
        Retrieve the MoziChem functions (local & external).
        """
        try:
            # NOTE: Load function from FunctionDispatcher
            return self.FunctionDispatcher_.retrieve_mozi_tools()
        except Exception as e:
            raise Exception(f"Failed to load MoziChem functions: {e}") from e

    def _build_tools(
        self,
        custom_functions: Optional[Dict[str, Callable]] = None
    ):
        """
        Build the tools for the MoziChem Hub.

        This method is responsible for building the tools that will be
        registered with the MoziChem Hub.

        Parameters
        ----------
        custom_functions : Optional[Dict[str, Callable]], optional
            Custom functions to be included in the tools, by default None

        Returns
        -------
        List[Tool]
            A list of Tool instances built from the MoziChem functions.
        """
        try:
            # SECTION: local resources
            # Retrieve functions
            _functions = self._retrieve_functions()

            # NOTE: Build local tools
            local_tools = self.build_tools(_functions)

            # SECTION: Build external tools
            if custom_functions:
                # NOTE: This is a placeholder for building external tools
                external_tools = self.build_tools(custom_functions)

            # NOTE: Combine local and external tools
            self._tools = local_tools + \
                (external_tools if custom_functions else [])

            # return the tools
            return self._tools
        except Exception as e:
            raise ValueError(f"Failed to build tools: {e}") from e

    def launch(self):
        """
        Launch the ToolManager.

        This method is called to start the ToolManager and prepare it for serving.
        """
        try:
            # SECTION: Build tools
            self._build_tools()
            return self._tools
        except Exception as e:
            raise RuntimeError(f"Failed to launch ToolManager: {e}") from e
