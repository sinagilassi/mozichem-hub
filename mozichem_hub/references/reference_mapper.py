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
from ..models import (
    References,
    ReferenceThermoDB
)
from .referencethermodb_controller import ReferenceThermoDBController
from ..models.resources_models import Component


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

    def _reference_thermodb_generator(
        self,
        references: References
    ) -> ReferenceThermoDB:
        """
        Generate the reference thermodb for the MCP methods.

        Parameters
        ----------
        references : References
            The references object containing the content, config, and link.

        Returns
        -------
        ReferenceThermoDB
            The reference thermodb for the MCP.

        """
        try:
            # NOTE: get the reference thermodb
            return self._generate_references(
                references=references
            )
        except Exception as e:
            logging.error(f"Failed to get reference thermodb: {e}")
            raise RuntimeError("Failed to get reference thermodb.") from e

    def _reference_thermodb_generator_from_reference_content(
        self,
        reference_content: str,
        components: List[Component]
    ) -> ReferenceThermoDB:
        """
        Generate the reference thermodb from the reference content.

        Parameters
        ----------
        reference_content : str
            The reference content to be used for generating the reference thermodb.
        """
        try:
            # NOTE: check if reference content is provided
            if not reference_content:
                raise ValueError(
                    "Reference content is required to generate reference thermodb.")

            # SECTION: init reference thermodb controller
            ReferenceThermoDBController_ = ReferenceThermoDBController(
                reference_content=reference_content
            )

            # NOTE: generate the reference thermodb
            return ReferenceThermoDBController_.\
                generate_components_reference_thermodb(
                    components=components
                )
        except Exception as e:
            logging.error(
                f"Failed to generate reference thermodb from content: {e}")
            raise RuntimeError(
                "Failed to generate reference thermodb from content.") from e

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

        Returns
        -------
        ReferenceThermoDB
            The reference thermodb for the MCP.

        Notes
        -----
        - This method combines the reference content and configuration to generate
        the reference thermodynamic database (thermodb) for the MCP methods.
        - This method is only used before the MCP server starts.
        """
        try:
            # SECTION: check the reference content and config
            # NOTE: standardize the reference content and config
            _references: References = self._reference_input_settings(
                reference_content=reference_content,
                reference_config=reference_config
            )

            # NOTE: set the reference thermodb
            return self._reference_thermodb_generator(
                references=_references
            )
        except Exception as e:
            logging.error(f"Failed to generate reference thermodb: {e}")
            raise RuntimeError("Failed to generate reference thermodb.") from e
