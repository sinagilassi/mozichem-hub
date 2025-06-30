# import libs
from typing import (
    Optional,
)
# local
from .models import (
    References,
    Reference,
    ReferenceThermoDB
)
from .references_initializer import ReferencesInitializer


class ReferenceServices:
    """
    It initializes and load references, and checks for external references.
    It provides access to the thermodb reference, reference, and reference link.
    """

    def __init__(
        self,
        references: Optional[References] = None,
    ):
        """
        Initialize the ReferenceServices.
        """
        # SECTION: configure the reference
        self.ReferencesInitializer_ = ReferencesInitializer(
            references=references,
        )

        # NOTE: initialize references
        self._reference_thermodb = self._initialize_references()

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

            # return
            return _reference_thermodb
        except Exception as e:
            raise Exception("Failed to initialize references.") from e

    def add_reference(
        self,
        reference: Reference,
        reference_link: str
    ):
        """
        Add a custom reference to the hub.

        Parameters
        ----------
        reference : Reference
            The custom reference to add.
        reference_link : str
            The custom reference link to add.
        """
        self._reference = reference
        self._reference_link = reference_link
