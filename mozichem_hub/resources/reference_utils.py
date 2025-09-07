# import libs
import logging
from typing import (
    Optional,
    List,
    Tuple
)
# locals
from ..models import Component, ReferenceThermoDB
from .hub import Hub
from ..errors import (
    CustomReferenceInitializationError,
    EmptyReferenceContentError,
    EmptyReferenceConfigError,
    InvalidReferenceContentTypeError,
    InvalidReferenceConfigTypeError,
    CUSTOM_REFERENCE_INIT_ERROR_MSG
)


def set_custom_reference(
    custom_reference_content: Optional[str],
    custom_reference_config: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    """
    Set custom reference content and configuration for the hub.
    If the content or config is empty, 'None' (string), then it will be set to None (bool).

    Parameters
    ----------
    custom_reference_content : str
        Custom reference content provided by the user.
    custom_reference_config : str
        Custom reference configuration provided by the user.

    Returns
    -------
    tuple
        A tuple containing the custom reference content and configuration.
    """
    try:
        # SECTION: check None values (string)
        # NOTE: check if custom_reference_content is None
        if custom_reference_content == 'None':  # set to 'None' string
            custom_reference_content = None  # set to None (bool)
        # NOTE: check if custom_reference_config is None
        if custom_reference_config == 'None':  # set to 'None' string
            custom_reference_config = None  # set to None (bool)

        # SECTION: check empty strings
        if (
            isinstance(custom_reference_content, str) and
            isinstance(custom_reference_config, str)
        ):
            # NOTE: check if custom_reference_content is empty
            if (
                custom_reference_content.strip() == '' or  # empty string
                len(custom_reference_content) == 0  # empty string
            ):
                # set to None (bool)
                custom_reference_content = None

            # NOTE: check if custom_reference_config is empty
            if (
                custom_reference_config.strip() == '' or  # empty string
                len(custom_reference_config) == 0  # empty string
            ):
                # set to None (bool)
                custom_reference_config = None

        # return the custom reference content and config
        return custom_reference_content, custom_reference_config

    except (
        EmptyReferenceContentError,
        EmptyReferenceConfigError,
    ) as e:
        logging.error(f"Empty reference content/config: {e}")
        return None, None
    except (
        InvalidReferenceContentTypeError,
        InvalidReferenceConfigTypeError,
    ) as e:
        logging.error(f"Invalid reference content/config type: {e}")
        raise e


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

    # SECTION: set custom reference
    # NOTE: set custom reference content and config
    custom_reference_content, custom_reference_config = \
        set_custom_reference(
            custom_reference_content=custom_reference_content,
            custom_reference_config=custom_reference_config
        )

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

            # NOTE: build reference_thermodb
            reference_thermodb: ReferenceThermoDB = \
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
            # LINK: initialize reference mapper
            ReferenceMapper_ = ReferenceMapper()

            # NOTE: set component
            if isinstance(components, Component):
                components = [components]

            # NOTE: build reference_thermodb with content only
            reference_thermodb: ReferenceThermoDB = \
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
        raise CustomReferenceInitializationError(
            CUSTOM_REFERENCE_INIT_ERROR_MSG) from e
