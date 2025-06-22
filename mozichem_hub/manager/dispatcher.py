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


class FunctionDispatcher():
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
        thermodb_rule : str
            Rule for initializing the pyThermoLinkDB instance.
        """
        # SECTION: Initialize the Hub
        self.Hub_ = Hub(
            reference_thermodb=reference_thermodb,
            reference=reference,
            reference_link=reference_link
        )

        # SECTION: Initialize function source
        # ptm
        self.PTMCore_ = PTMCore(self.Hub_)

    def get_functions(self):
        """
        Get all functions available in the MoziChem Hub.

        Returns
        -------
        List[str]
            List of function names.
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
            raise Exception(f"Failed to get function list: {e}") from e
