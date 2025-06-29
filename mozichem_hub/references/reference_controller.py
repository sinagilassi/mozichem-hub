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
from .models import ComponentPropertySource


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
            # SECTION: transform the reference content
            reference_content = self.__transform_reference_content()

            # SECTION: transform the reference config
        except Exception as e:
            logging.error(
                "Failed to transform references. "
                "Please check the provided content and configuration. Error: %s", e
            )

    def __transform_reference_content(self) -> List[str]:
        """
        Transform the reference content into a list of strings.
        """
        try:
            # NOTE: init
            res = []

            # NOTE: check
            if isinstance(self._reference_content, str):
                # add the content to the result list
                res.append(self._reference_content)
            elif isinstance(self._reference_content, list):
                # iterate over the list and add the content to the result list
                for content in self._reference_content:
                    if isinstance(content, str):
                        res.append(content)
                    else:
                        logging.warning(
                            "Invalid content type in reference content list: %s", type(
                                content)
                        )
            else:
                logging.error(
                    "Invalid reference content type: %s. Expected str or list of str.",
                    type(self._reference_content)
                )

            # NOTE: return the result
            return res
        except Exception as e:
            logging.error(
                "Failed to transform reference content. "
                "Please check the provided content. Error: %s", e
            )
            return []

    def __transform_reference_config(
        self
    ) -> Dict[str, Dict[str, ComponentPropertySource]]:
        """
        Transform the reference configuration into the required format.
        """
        try:
            # NOTE: init the reference config
            res: Dict[str, Dict[str, ComponentPropertySource]] = {}

            # NOTE: check if the reference config is a string
            if isinstance(self._reference_config, str):
                # convert the string to a dictionary
                res = self.from_str(self._reference_config)
            elif isinstance(self._reference_config, dict):
                pass
            else:
                logging.error(
                    "Invalid reference config type: %s. Expected str or dict.",
                    type(self._reference_config)
                )

            # NOTE: return the result
            return res
        except Exception as e:
            logging.error(
                "Failed to transform reference config. "
                "Please check the provided configuration. Error: %s", e
            )
            return {}
