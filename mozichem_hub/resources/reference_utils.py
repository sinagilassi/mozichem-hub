# import libs
import logging
from typing import (
    Optional,
)
# locals
from ..models import Component


def initialize_custom_reference(
    hub,
    component: Component,
    custom_reference_content: Optional[str],
    custom_reference_config: Optional[str],
):
    """
    Universal helper to initialize the hub with a custom reference if provided.
    Returns a new hub instance if a custom reference is used, otherwise returns the original hub.
    """
    # import libs
    from ..references import ReferenceMapper
    from .hub import Hub

    # set hub
    try:
        # SECTION: reinitialize hub if needed
        # NOTE: select the reference mapper
        if (
            custom_reference_content is not None and
            custom_reference_config is not None
        ):
            # LINK: initialize reference mapper
            ReferenceMapper_ = ReferenceMapper()

            # NOTE: check
            if (
                custom_reference_content == '' or
                custom_reference_config == 'None'
            ):
                raise ValueError(
                    "Custom reference content cannot be empty if custom reference config is provided. Thus, set it to None."
                )

            if (
                custom_reference_config == '' or
                custom_reference_config == 'None'
            ):
                raise ValueError(
                    "Custom reference config cannot be empty if custom reference content is provided. Thus, set it to None."
                )

            # NOTE: build reference_thermodb
            reference_thermodb = \
                ReferenceMapper_.generate_reference_thermodb(
                    reference_content=custom_reference_content,
                    reference_config=custom_reference_config
                )

            # ! reinitialize hub with the new reference thermodb
            return Hub(reference_thermodb)
        elif (
            custom_reference_content is not None and
            custom_reference_config is None
        ):
            # NOTE: check
            if (
                custom_reference_content == '' or
                custom_reference_content == 'None'
            ):
                raise ValueError(
                    "Custom reference content cannot be empty if custom reference config is not provided. Thus, set it to None."
                )

            # LINK: initialize reference mapper
            ReferenceMapper_ = ReferenceMapper()

            # NOTE: build reference_thermodb with content only
            reference_thermodb = \
                ReferenceMapper_.\
                _reference_thermodb_generator_from_reference_content(
                    reference_content=custom_reference_content,
                    components=[component]
                )
            # ! reinitialize hub with the new reference thermodb
            return Hub(reference_thermodb)
        else:
            # NOTE: no custom reference provided, return the original hub
            return hub
    except Exception as e:  # pragma: no cover
        logging.error(f"Failed to initialize custom reference: {e}")
        raise RuntimeError("Failed to initialize custom reference.") from e
