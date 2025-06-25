# import libs
from typing import (
    Optional,
    Tuple,
    Dict,
    List,
    Union)
# local
from .reference import REFERENCE
from .config import REFERENCE_CONFIG
from .rules import THERMODB_RULES
from .models import (
    References,
    Reference,
    ReferenceLink,
    ComponentReferenceConfig,
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
        references: Optional[References] = None,
        reference_link: Optional[ReferenceLink] = None,
        component_reference_config: Optional[
            Dict[str, ComponentReferenceConfig]
        ] = None
    ):
        """
        Initialize the references.
        """
        # NOTE:
        # component reference config
        self._component_reference_config = component_reference_config

        # SECTION: set reference
        (
            self._reference,  # ! PyThermoDB reference
            self._reference_content,  # ! PyThermoDB reference
            self._reference_config,  # ! PyThermoDB reference configuration
            self._rule  # ! PyThermoLinkDB rule
        ) = self.initialize_references(references, reference_link)

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
        references: Optional[References] = None,
        reference_link: Optional[ReferenceLink] = None
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
            # SECTION: local reference
            # NOTE: load local reference
            local_reference = self._load_local_reference()

            # NOTE: load local rules
            local_rules = self._load_rules()

            # SECTION: external reference
            # init
            external_references = References(contents=[], config={})
            external_reference_link = None

            # NOTE: load external reference
            if references is not None:
                # set external reference
                external_references = references

            # NOTE: load external reference link
            if reference_link is not None:
                # set external reference link
                external_reference_link = reference_link

            # SECTION: set default reference
            reference_ = ReferenceThermoDB(
                reference={
                    "reference": [
                        REFERENCE, external_references.contents
                    ]
                }
            )

            # NOTE: set default reference content and config
            reference_content = REFERENCE
            reference_config = REFERENCE_CONFIG
            rule = THERMODB_RULES

            # return
            return reference_, reference_content, reference_config, rule
        except Exception as e:
            raise ValueError(
                f"Failed to analyze custom reference: {e}") from e

    def _load_local_reference(self):
        """
        Load the local reference content, configuration, and rule.

        Returns
        -------
        Tuple[str, Dict[str, Dict[str, str]]]
            The local reference content, configuration, and rule.
        """
        try:
            # Load the local reference content
            reference_content = REFERENCE

            # Load the local reference configuration
            reference_config = REFERENCE_CONFIG

            return reference_content, reference_config
        except Exception as e:
            raise ValueError(f"Failed to load local reference: {e}") from e

    def _load_rules(self) -> str:
        """
        Load the rules for the reference.

        Returns
        -------
        str
            The rule for the reference.
        """
        try:
            return THERMODB_RULES
        except Exception as e:
            raise ValueError(f"Failed to load rules: {e}") from e

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
