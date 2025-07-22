# import libs
import logging
from typing import (
    Optional,
    List
)
# locals
from ..models import Component
from .hub import Hub


def initialize_custom_reference(
    hub: Hub,
    components: Component | List[Component],
    custom_reference_content: Optional[str],
    custom_reference_config: Optional[str],
) -> Hub:
    """
    Universal helper to initialize the hub with a custom reference if provided.
    Returns a new hub instance if a custom reference is used, otherwise returns the original hub.

    Parameters
    ----------
    hub : Hub
        The original hub instance.
    components : Component | List[Component]
        The component or list of components for which the custom reference is being set.
    custom_reference_content : Optional[str]
        Custom reference content provided by the user.
    custom_reference_config : Optional[str]
        Custom reference configuration provided by the user.

    Returns
    -------
    Hub
        A new hub instance initialized with the custom reference if provided, otherwise the original hub.
    """
    # import libs
    from ..references import ReferenceMapper

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
            if isinstance(custom_reference_content, str):
                # empty string check
                if (
                    custom_reference_content.strip() == '' or  # empty string
                    custom_reference_content == 'None' or  # 'None' string
                    len(custom_reference_content) == 0  # empty string
                ):
                    raise ValueError(
                        "Custom reference content cannot be empty. Thus, set it to None."
                    )
            else:
                raise TypeError(
                    "Custom reference content must be a string."
                )

            # NOTE: check
            if isinstance(custom_reference_config, str):
                # empty string check
                if (
                    custom_reference_config.strip() == '' or  # empty string
                    custom_reference_config == 'None' or  # 'None' string
                    len(custom_reference_config) == 0  # empty string
                ):
                    raise ValueError(
                        "Custom reference config cannot be empty. Thus, set it to None."
                    )
            else:
                raise TypeError(
                    "Custom reference config must be a string."
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
            if isinstance(custom_reference_content, str):
                # empty string check
                if (
                    custom_reference_content.strip() == '' or  # empty string
                    custom_reference_content == 'None' or  # 'None' string
                    len(custom_reference_content) == 0  # empty string
                ):
                    raise ValueError(
                        (
                            "Custom reference content cannot be empty. "
                            "Thus, set it to None."
                        )
                    )
            else:
                raise TypeError(
                    "Custom reference content must be a string."
                )

            # NOTE: check
            if isinstance(custom_reference_config, str):
                # empty string check
                if (
                    custom_reference_config.strip() == '' or  # empty string
                    custom_reference_config == 'None' or  # 'None' string
                    len(custom_reference_config) == 0  # empty string
                ):
                    custom_reference_config = None

            # LINK: initialize reference mapper
            ReferenceMapper_ = ReferenceMapper()

            # NOTE: set component
            if isinstance(components, Component):
                components = [components]

            # NOTE: build reference_thermodb with content only
            reference_thermodb = \
                ReferenceMapper_.\
                _reference_thermodb_generator_from_reference_content(
                    reference_content=custom_reference_content,
                    components=components
                )
            # ! reinitialize hub with the new reference thermodb
            return Hub(reference_thermodb)
        else:
            # NOTE: no custom reference provided, return the original hub
            return hub
    except Exception as e:  # pragma: no cover
        logging.error(f"Failed to initialize custom reference: {e}")
        raise RuntimeError("Failed to initialize custom reference.") from e
