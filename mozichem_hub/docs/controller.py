# import libs
from typing import (
    Optional,
    Union,
    List
)
import logging
# locals


class ReferenceController:
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
            Union[str, List[str]]
        ] = None,
    ):
        # NOTE: reference_content and reference_config are optional
        self.reference_content = reference_content
        self.reference_config = reference_config

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
        if isinstance(self.reference_content, str):
            return [self.reference_content]
        elif isinstance(self.reference_content, list):
            return self.reference_content
        else:
            logging.warning("Reference content is not in a valid format.")
            return None

    def _transform_reference_config(self):
        """
        Transform the reference configuration into a usable format.
        """
        if isinstance(self.reference_config, str):
            return [self.reference_config]
        elif isinstance(self.reference_config, list):
            return self.reference_config
        else:
            logging.warning("Reference config is not in a valid format.")
            return None
