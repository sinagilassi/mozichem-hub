# import libs
import logging
from typing import (
    Optional,
    Union,
    Dict,
    List
)
# locals
from .reference_services import ReferenceServices
from .reference_controller import ReferenceController
from .models import (
    References,
    ReferenceThermoDB
)


class ReferenceMapper(ReferenceServices):
    """
    Mapper for transforming and managing references in the MoziChem MCP.
    """
    # NOTE: attributes

    def __init__(
            self
    ):
        """
        Initialize the ReferenceMapper.
        """
        # LINK: initialize the transformer
        ReferenceServices.__init__(self)

    def _reference_input_settings(
        self,
        reference_content: Optional[
            Union[str, List[str]]
        ] = None,
        reference_config: Optional[
            Union[
                str,
                Dict[str, Dict[str, str | Dict[str, str]]]
            ]
        ] = None
    ) -> References:
        """
        Set the reference content and configuration for the MCP.

        Parameters
        ----------
        reference_content : Optional[Union[str, List[str]]]
            Reference content for the MCP.
        reference_config : Optional[Union[str, Dict[str, Dict[str, str]]]]
            Reference configuration for the MCP.

        Returns
        -------
        References
            The references object containing the content, config, and link.
        """
        try:
            # SECTION: standardize the reference content and config
            # NOTE: init the ReferencesAdapter
            ReferenceController_ = ReferenceController(
                reference_content=reference_content,
                reference_config=reference_config
            )

            # NOTE: config conversion
            # ! convert the reference content
            # ! convert the reference config
            # ! build the reference link
            (
                reference_content_,
                reference_config_,
                reference_link_
            ) = ReferenceController_.transformer()

            # NOTE: set reference
            references = References(
                contents=reference_content_,
                config=reference_config_,
                link=reference_link_
            )

            # return
            return references
        except Exception as e:
            logging.error(
                f"Failed to transform reference content and config: {e}"
            )
            raise RuntimeError(
                "Failed to transform reference content and config."
            ) from e

    def _reference_thermodb_settings(
        self,
        references: References
    ) -> ReferenceThermoDB:
        """
        Get the reference thermodb settings for the MCP.

        Returns
        -------
        ReferenceThermoDB
            The reference thermodb settings for the MCP.
        """
        try:
            # NOTE: get the reference thermodb
            return self._generate_references(
                references=references
            )
        except Exception as e:
            logging.error(f"Failed to get reference thermodb: {e}")
            raise RuntimeError("Failed to get reference thermodb.") from e

    def generate_reference_thermodb(
        self,
        reference_content: Optional[
            Union[str, List[str]]
        ] = None,
        reference_config: Optional[
            Union[
                str,
                Dict[str, Dict[str, str | Dict[str, str]]]
            ]
        ] = None
    ) -> ReferenceThermoDB:
        """
        Generate the reference thermodb for the MCP.

        Parameters
        ----------
        reference_content : Optional[Union[str, List[str]]]
            Reference content for the MCP.
        reference_config : Optional[Union[str, Dict[str, Dict[str, str]]]]
            Reference configuration for the MCP.
        """
        try:
            # SECTION: standardize the reference content and config
            _references: References = self._reference_input_settings(
                reference_content=reference_content,
                reference_config=reference_config
            )

            # NOTE: set the reference thermodb
            return self._reference_thermodb_settings(
                references=_references
            )
        except Exception as e:
            logging.error(f"Failed to generate reference thermodb: {e}")
            raise RuntimeError("Failed to generate reference thermodb.") from e

    def _reference_thermodb_from_reference_content(
        self
    ):
        pass
