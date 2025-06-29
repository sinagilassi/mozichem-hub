# import libs
from typing import (
    Optional,
    Tuple,
    Dict,
    List,
    Union)
# local
from .reference import REFERENCE_CONTENT
from .config import REFERENCE_CONFIGS
from .link import REFERENCE_LINK
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
            local_reference_content, local_reference_config = \
                self.__load_local_reference()

            # NOTE: load local rules
            local_link_config = self.__load_link_config()

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
            reference, reference_content = self.__generate_reference_thermodb(
                local_reference_content=local_reference_content,
                local_reference_config=local_reference_config,
                external_references=external_references
            )

            # NOTE: set default reference content and config
            reference_config = REFERENCE_CONFIGS
            rule = REFERENCE_LINK

            # return
            return reference, reference_content, reference_config, rule
        except Exception as e:
            raise ValueError(
                f"Failed to analyze custom reference: {e}") from e

    def __load_local_reference(self):
        """
        Load the local reference content, configuration, and rule.

        Returns
        -------
        str | Dict[str, Dict[str, ComponentPropertySource]]
            The local reference content, configuration, and rule.
        """
        try:
            # Load the local reference content
            reference_content = REFERENCE_CONTENT

            # Load the local reference configuration
            reference_config = REFERENCE_CONFIGS

            return reference_content, reference_config
        except Exception as e:
            raise ValueError(f"Failed to load local reference: {e}") from e

    def __load_reference_link(self) -> str:
        """
        Load the link config for the reference.

        Returns
        -------
        str
            The rule for the reference.
        """
        try:
            return REFERENCE_LINK
        except Exception as e:
            raise ValueError(f"Failed to load rules: {e}") from e

    def __generate_reference_thermodb(
        self,
        local_reference_content: str,
        local_reference_config: Dict[str, ComponentReferenceConfig],
        external_references: References
    ) -> ReferenceThermoDB:
        """
        Generate the ReferenceThermoDB object.

        Parameters
        ----------
        local_reference_content : str
            The local reference content.
        local_reference_config : Dict[str, Dict[str, str]]
            The local reference configuration.
        external_references : References
            The external references to be included in the ReferenceThermoDB.

        """
        try:
            # NOTE: extract the reference content from the external references
            external_references_content = external_references.contents if external_references.contents else []

            # NOTE: extract the reference config from the external references
            external_references_config = external_references.config if external_references.config else {}

            # SECTION: merge local and external references
            # Combine local reference content with external references

            # Create the ReferenceThermoDB object
            reference_thermodb = ReferenceThermoDB(
                reference=[local_reference_content] +
                external_references_content,
                config={
                    **local_reference_config,
                    **external_references_config
                }
            )
            return reference_thermodb
        except Exception as e:
            raise ValueError(
                f"Failed to generate ReferenceThermoDB: {e}") from e

    def _get_reference(
        self,
    ) -> References:
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
            return References(
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
