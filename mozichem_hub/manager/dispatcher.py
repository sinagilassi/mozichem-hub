# import libs
from typing import List, Dict, Annotated, Literal, Optional
# locals
from .models import (
    CustomReference
)
from .hub import Hub
from .ptmcore import PTMCore


class Dispatcher(PTMCore):
    """
    Dispatcher class for defining functions in the MoziChem Hub.
    """
    # NOTE: attributes

    def __init__(
        self,
        custom_reference: Optional[CustomReference] = None,
    ):
        """
        Initialize the Dispatcher instance.

        Parameters
        ----------
        thermodb_rule : str
            Rule for initializing the pyThermoLinkDB instance.
        """
        # SECTION: Initialize the Hub
        self.Hub_ = Hub(custom_reference)

        # SECTION: Initialize the ThermoModels instance
        # ptm
        PTMCore.__init__(self, self.Hub_)
