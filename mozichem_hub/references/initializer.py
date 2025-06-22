# import libs
from typing import Optional, Tuple, Dict, List, Union
# local
from .reference import REFERENCE
from .config import REFERENCE_CONFIG
from .rules import THERMODB_RULES
from .models import (
    Reference,
    ReferenceLink,
    ReferenceThermoDB
)


class ReferencesInitializer:
    """
    This class is responsible for setting up the necessary references
    that will be used throughout the hub.
    """

    # NOTE: attributes

    def __init__(
        self,
        custom_reference: Optional[Reference] = None,
        custom_reference_link: Optional[ReferenceLink] = None
    ):
        """
        Initialize the references.
        """
        # SECTION: set reference
        (
            self._reference,  # ! PyThermoDB reference
            self._reference_content,  # ! PyThermoDB reference
            self._reference_config,  # ! PyThermoDB reference configuration
            self._rule  # ! PyThermoLinkDB rule
        ) = self.initialize_references(custom_reference, custom_reference_link)

    @property
    def reference_content(self) -> str:
        """
        Get the reference content.
        """
        return self._reference_content

    @property
    def reference_config(self) -> Dict[str, Dict[str, str]]:
        """
        Get the reference configuration.
        """
        return self._reference_config

    @property
    def rule(self) -> str:
        """
        Get the reference rule.
        """
        return self._rule

    def initialize_references(
        self,
        custom_reference: Optional[Reference] = None,
        custom_reference_link: Optional[ReferenceLink] = None
    ) -> Tuple[
        ReferenceThermoDB,
        str,
        Dict[str, Dict[str, str]],
        str
    ]:
        """
        Analyze the custom reference for the ThermoHub.

        Returns
        -------
        dict
            The custom reference dictionary.
        """
        try:
            # NOTE: set default reference
            reference = ReferenceThermoDB(
                reference={
                    "reference": [REFERENCE]
                }
            )

            # NOTE: set default reference content and config
            reference_content = REFERENCE
            reference_config = REFERENCE_CONFIG
            rule = THERMODB_RULES

            # return
            return reference, reference_content, reference_config, rule
        except Exception as e:
            raise ValueError(
                f"Failed to analyze custom reference: {e}") from e

    def _get_reference(
        self,
    ) -> Reference:
        """
        Get the reference content and config.

        Parameters
        ----------
        prop : str
            The property to select the reference content for.

        Returns
        -------
        List[str]
            The list of reference content for the given property.
        """
        try:
            return Reference(
                content=self._reference_content,
                config=self._reference_config
            )
        except Exception as e:
            raise ValueError(f"Failed to select reference content: {e}") from e

    def _get_reference_link(
        self,
    ) -> ReferenceLink:
        """
        Get the reference link.

        Returns
        -------
        ReferenceLink
            The reference link.
        """
        try:
            return ReferenceLink(rule=self._rule)
        except Exception as e:
            raise ValueError(f"Failed to select reference link: {e}") from e

    def _get_reference_thermodb(
        self,
    ) -> ReferenceThermoDB:
        """
        Get the reference thermodynamic database.

        Returns
        -------
        ReferenceThermoDB
            The reference thermodynamic database.
        """
        try:
            return self._reference
        except Exception as e:
            raise ValueError(
                f"Failed to select reference thermodynamic database: {e}") from e
