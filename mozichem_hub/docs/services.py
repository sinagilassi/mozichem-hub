# import libs
from typing import Optional
# local
from ..references import (
    ReferencesInitializer,
    Reference,
    ReferenceLink,
    ReferenceThermoDB
)


class ReferenceServices:
    """
    It initializes and load references, and checks for external references.
    It provides access to the thermodb reference, reference, and reference link.
    """

    def __init__(
        self,
        reference: Optional[Reference] = None,
        reference_link: Optional[ReferenceLink] = None
    ):
        """
        Initialize the ReferenceServices.
        """
        # SECTION: configure the reference
        self.ReferencesInitializer_ = ReferencesInitializer(
            reference,
            reference_link
        )

        # NOTE: reference thermodb
        self._reference_thermodb = \
            self.ReferencesInitializer_._get_reference_thermodb()
        # NOTE: reference
        self._reference = self.ReferencesInitializer_._get_reference()
        # NOTE: reference link
        self._reference_link = \
            self.ReferencesInitializer_._get_reference_link()

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
