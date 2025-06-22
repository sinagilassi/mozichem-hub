# import libs
from typing import (
    Optional,
    Dict,
    List,
    Callable
)
# local
from .registry import RegistryMixin
from .server import MoziServer
from ..tools import ToolManager
from ..references import (
    ReferencesInitializer,
    Reference,
    ReferenceLink
)


class MoziChemHub(RegistryMixin):
    """
    This is the main entry point for the MoziChem Hub application.
    It initializes the MoziChemHub instance and prepares it for serving.
    custom reference and link can be passed to the MoziChemHub instance.
    """

    def __init__(
            self,
            name: str = "MoziChemHub",
            reference: Optional[Reference] = None,
            reference_link: Optional[ReferenceLink] = None,
            **kwargs
    ):
        """
        Initialize the MoziChemHub.

        Parameters
        ----------
        name : str
            Name of the hub, default is "MoziChemHub".
        reference : Optional[Reference]
            Custom reference for the hub, default is None. It includes
            - content: str
            - config: dict
        reference_link : Optional[ReferenceLink]
            Custom reference link for the hub, default is None.
        **kwargs : dict
            Additional keyword arguments for hub configuration.
        """
        # NOTE: set
        self._name = name
        self._reference = reference
        self._reference_link = reference_link

        # SECTION: initialize the registry
        RegistryMixin().__init__()

        # SECTION: configure the reference
        self.ReferencesInitializer_ = ReferencesInitializer(
            reference,
            reference_link
        )

        # SECTION: initialize the MoziServer
        self.MoziServer_ = MoziServer(name=name)

        # SECTION: initialize tool manager
        self.ToolManager_ = ToolManager()

    @property
    def name(self) -> str:
        """
        Get the name of the hub.
        """
        return self._name

    @property
    def reference_content(self) -> Reference:
        """
        Get the reference of the hub.
        """
        return self.ReferencesInitializer_._get_reference()

    @property
    def reference_link(self) -> ReferenceLink:
        """
        Get the reference link of the hub.
        """
        return self.ReferencesInitializer_._get_reference_link()

    def __launch(self):
        """
        Launch the MoziChem Hub.

        This method is called to start the hub and prepare it for serving.
        """
        try:
            # NOTE: manage tools
            # collect the registered tools
            custom_tools: Dict[str, Callable] = self.methods

            # NOTE: build the tools
            # build the tools using the ToolManager
            tools = self.ToolManager_._build_tools(
                custom_tools=custom_tools
            )

            # NOTE: build the mcp server with the registered tools
            mcp = self.MoziServer_._build_mcp(
                tools=tools
            )

            return mcp
        except Exception as e:
            raise RuntimeError(f"Failed to launch {self.name}: {e}") from e

    def run(self, verbose: bool = True):
        """
        Run the MoziChem Hub.

        """
        try:
            # NOTE: Check if verbose is enabled
            if verbose:
                print(f"Running {self.name}...")

            # NOTE: Additional launch logic can be added here
            self.__launch()
        except Exception as e:
            raise RuntimeError(f"Failed to run {self.name}: {e}") from e
