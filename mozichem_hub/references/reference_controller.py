# import libs
import logging
from typing import (
    Optional,
    Union,
    List,
    Dict,
    Tuple,
)
from pythermodb_settings.models import ComponentConfig
# locals
from .reference_adapter import ReferencesAdapter
from ..models import ComponentPropertySource


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
            Union[
                str,
                Dict[str, Dict[str, ComponentConfig]]
            ]
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

    def transformer(
        self
    ) -> Tuple[
        Union[List[str], None],
        Union[Dict[str, Dict[str, ComponentPropertySource]], None],
        Union[str, None]
    ]:
        """
        transformer for the reference content and configuration.
        """
        # Logic to initialize references goes here
        try:
            # SECTION: transform the reference content
            reference_content = self.__transform_reference_content()

            # SECTION: transform the reference config
            reference_config = self.__transform_reference_config()

            # SECTION: build the reference link
            reference_link = self.__build_reference_link(
                reference_config,
            )

            # result
            return (
                reference_content,
                reference_config,
                reference_link
            )
        except Exception as e:
            logging.error(
                "Failed to transform references. "
                "Please check the provided content and configuration. Error: %s", e
            )
            raise

    def __transform_reference_content(self) -> Union[List[str], None]:
        """
        Transform the reference content into a list of strings.
        """
        try:
            # SECTION: no reference content provided
            if self._reference_content is None:
                return None

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
                return None

            # NOTE: return the result
            return res
        except Exception as e:
            logging.error(
                "Failed to transform reference content. "
                "Please check the provided content. Error: %s", e
            )
            return None

    def __transform_reference_config(
        self
    ) -> Union[
        Dict[str, Dict[str, ComponentPropertySource]], None
    ]:
        """
        Transform the reference configuration into the required format.
        """
        try:

            # SECTION: no reference config provided
            if self._reference_config is None:
                logging.warning("No reference config provided.")
                return None

            # SECTION: reference config is provided
            # NOTE: init the reference config
            res: Dict[str, Dict[str, ComponentPropertySource]] = {}

            # NOTE: check if the reference config is a string
            if isinstance(self._reference_config, str):
                # ! convert the string to a dictionary
                res = self.config_from_str(self._reference_config)
            elif isinstance(self._reference_config, dict):
                # ! if it's already a dictionary to the required dictionary format
                res = self.config_from_dict(self._reference_config)
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
            return None

    def __build_reference_link(
        self,
        reference_config: Optional[
            Dict[str, Dict[str, ComponentPropertySource]]
        ] = None
    ) -> Optional[str]:
        """
        Build the reference link for the MCP server.

        Parameters
        ----------
        reference_config : Dict[str, Dict[str, ComponentPropertySource]]
            The reference configuration to build the link from.

        Returns
        -------
        Optional[str]
            The reference link if provided, otherwise None.
        """
        try:
            # SECTION: reference config is empty
            if not reference_config:
                logging.warning(
                    "Reference config is empty. No link will be built.")
                return None

            # SECTION: build the reference link
            reference_link = self.build_reference_link(reference_config)

            # NOTE: check the result format
            if reference_link is not None:
                # convert the reference link to a string
                reference_link = self.str_from_reference_link(reference_link)

            # return the reference link
            return reference_link
        except Exception as e:
            logging.error(
                "Failed to build reference link. "
                "Please check the provided configuration. Error: %s", e
            )
            return None
