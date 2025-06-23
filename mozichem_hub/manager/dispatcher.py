# import libs
from typing import (
    List,
    Dict,
    Annotated,
    Literal,
    Optional,
    Any
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
        self.PTMCore_ = PTMCore(self.Hub_)

    def _get_local_functions(self) -> Dict[str, Any]:
        """
        Get all local functions available in the MoziChem Hub.

        Returns
        -------
        Dict[str, Any]
            Dictionary of local function names and their implementations.
        """
        try:
            # SECTION: get function list from the Hub
            # function dict 1
            f1: Dict[str, Any] = self.PTMCore_.list_functions()

            # function dict 2
            f2: Dict[str, Any] = self.PTMCore_.list_functions()

            # NOTE: init dict
            functions: Dict[str, Any] = {}
            # add functions to the dict
            functions.update(f1)
            functions.update(f2)

            # return
            return functions
        except Exception as e:
            raise Exception(f"Failed to get local function list: {e}") from e

    def retrieve_mozi_tools(self):
        """
        Get all mozi tools available in the MoziChem Hub.

        Returns
        -------
        List[str]
            List of function names.
        """
        try:
            # SECTION: get local function from the Hub
            local_functions: Dict[str, Any] = self._get_local_functions()

            # SECTION: convert to MoziTools
            # NOTE: convert local functions to MoziTools
            mozi_tools = self.build_mozi_tools(local_functions)

            # NOTE: init dict
            functions: Dict[str, Any] = {}

            # return
            return functions
        except Exception as e:
            raise Exception(f"Failed to get function list: {e}") from e
