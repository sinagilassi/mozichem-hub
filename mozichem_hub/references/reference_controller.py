# import libs
from typing import (
    Optional,
    Union,
    List,
    Dict
)
import logging
# locals
from .reference_adapter import ReferencesAdapter


class ReferenceController(ReferencesAdapter):
    """
    Controller for transforming and managing references in the MoziChem MCP.
    """
    # NOTE: attributes

    def __init__(
        self,
        reference_content: Optional[
            Union[str, List[str]]
        ] = None,
        reference_config: Optional[
            Union[str, Dict[str, Dict[str, str]]]
        ] = None
    ):
        """
        Initialize the ReferenceController.
        """
        # LINK: initialize the transformer
        ReferencesAdapter.__init__(self)

        # NOTE: set the reference content and config
        self._reference_content = reference_content
        self._reference_config = reference_config

    def transformer(self):
        """
        transformer for the reference content and configuration.
        """
        # Logic to initialize references goes here
        try:
            pass
        except Exception as e:
            logging.error(
                "Failed to transform references. "
                "Please check the provided content and configuration. Error: %s", e
            )

    def _transform_reference_content(self):
        """
        Transform the reference content into a usable format.
        """
        if isinstance(self._reference_content, str):
            return [self._reference_content]
        elif isinstance(self._reference_content, list):
            return self._reference_content
        else:
            logging.warning("Reference content is not in a valid format.")
            return None

    def _transform_reference_config(self):
        """
        Transform the reference configuration into a usable format.
        """
        if isinstance(self.reference_config, str):
            return [self.reference_config]
        elif isinstance(self.reference_config, dict):
            return self.reference_config
        else:
            logging.warning("Reference config is not in a valid format.")
            return None
