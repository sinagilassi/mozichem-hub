# import libs
from typing import (
    Optional,
    Dict,
    List,
    Union
)
# local
from ..references import (
    ReferencesInitializer,
    References,
    Reference,
    ReferenceLink,
    ReferenceThermoDB,
    ComponentReferenceConfig
)


class ReferenceServices:
    """
    It initializes and load references, and checks for external references.
    It provides access to the thermodb reference, reference, and reference link.
    """

    def __init__(
        self,
        references: Optional[References] = None,
        reference_link: Optional[ReferenceLink] = None,
        component_reference_config: Optional[
            Union[
                ComponentReferenceConfig,
                List[ComponentReferenceConfig]
            ]
        ] = None,
    ):
        """
        Initialize the ReferenceServices.
        """
        # SECTION: configure the reference
        self.ReferencesInitializer_ = ReferencesInitializer(
            reference,
            reference_link
        )

        # NOTE: initialize references
        self._reference_thermodb, self._reference, self._reference_link = \
            self._initialize_references()

    @property
    def reference(self) -> Reference:
        """
        Get the reference of the hub.
        """
        return self._reference

    @property
    def reference_link(self) -> ReferenceLink:
        """
        Get the reference link of the hub.
        """
        return self._reference_link

    @property
    def reference_thermodb(self) -> ReferenceThermoDB:
        """
        Get the reference thermodb of the hub.
        """
        return self._reference_thermodb

    def _initialize_references(self):
        """
        Initialize the references.
        """
        try:
            # NOTE: reference thermodb
            _reference_thermodb = \
                self.ReferencesInitializer_._get_reference_thermodb()

            # NOTE: reference
            _reference = self.ReferencesInitializer_._get_reference()

            # NOTE: reference link
            _reference_link = \
                self.ReferencesInitializer_._get_reference_link()

            # return
            return _reference_thermodb, _reference, _reference_link
        except Exception as e:
            raise Exception("Failed to initialize references.") from e

    def add_reference(
        self,
        reference: Reference,
        reference_link: ReferenceLink
    ):
        """
        Add a custom reference to the hub.

        Parameters
        ----------
        reference : Reference
            The custom reference to add.
        reference_link : ReferenceLink
            The custom reference link to add.
        """
        self._reference = reference
        self._reference_link = reference_link
