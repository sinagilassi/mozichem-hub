# import libs
from typing import (
    Optional,
)
# local
from .models import (
    References,
    ReferenceThermoDB
)
from .references_initializer import ReferencesInitializer


class ReferenceServices:
    """
    It initializes and load references, and checks for external references.
    It provides access to the thermodb reference, reference, and reference link.
    """

    def __init__(self):
        """
        Initialize the ReferenceServices.
        """
        pass

    def _generate_references(
        self,
        references: Optional[References] = None
    ) -> ReferenceThermoDB:
        """
        Initialize the references.

        Notes
        -----
        - If the user provides a custom reference, it will be used.
        - If the user does not provide a custom reference, the default references will be used.
        """
        try:
            # SECTION: configure the reference
            self.ReferencesInitializer_ = ReferencesInitializer(
                references=references,
            )

            # NOTE: reference thermodb
            _reference_thermodb: ReferenceThermoDB = \
                self.ReferencesInitializer_._get_reference_thermodb()

            # return
            return _reference_thermodb
        except Exception as e:
            raise Exception("Failed to initialize references.") from e

    def _set_custom_references(
        self,
        references: References,
    ):
        """
        Add a custom reference to the mcp server.

        Parameters
        ----------
        references : References
            The custom references to be added to the mcp server.

        Returns
        -------
        None
        """
        pass
