# import libs
import logging
from typing import (
    Optional,
    List,
    Tuple,
    Dict
)
from pyThermoDB.models import ComponentConfig, ComponentRule
# locals
from ..models import Component, ReferenceThermoDB, ComponentReferenceThermoDB, ReferencesThermoDB
from .hub import Hub
from ..utils import create_component_id
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
    ignore_state_props: Optional[List[str]] = None
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
    ignore_state_props : Optional[List[str]], optional
        List of properties to ignore state for, by default None.

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
            reference_thermodb: ReferencesThermoDB = \
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

            # init components reference thermodb list
            components_reference_thermodb: List[ComponentReferenceThermoDB] = [
            ]

            # SECTION: build component reference thermodb
            # NOTE: set component
            if isinstance(components, list):
                # check if list is empty
                if len(components) == 0:
                    raise ValueError("Components list is empty.")

                # NOTE: method 1
                components_reference_thermodb: List[ComponentReferenceThermoDB] = \
                    ReferenceMapper_.\
                    components_reference_thermodb_generator_from_reference_content(
                        components=components,
                        reference_content=custom_reference_content,
                        ignore_state_props=ignore_state_props
                )

            elif isinstance(components, Component):
                components = [components]
                # NOTE: method 2 (with ignore_state_props)
                reference_thermodb__: ComponentReferenceThermoDB = \
                    ReferenceMapper_.\
                    component_reference_thermodb_generator_from_reference_mapper(
                        component=components[0],
                        reference_content=custom_reference_content,
                        ignore_state_props=ignore_state_props
                    )
                components_reference_thermodb = [reference_thermodb__]
            else:
                raise TypeError(
                    "Components must be a Component or a list of Components.")

            # NOTE: build references thermodb
            reference_thermodb: ReferencesThermoDB = to_references_thermodb(
                components_reference_thermodb=components_reference_thermodb
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


def to_references_thermodb(
        components_reference_thermodb: List[ComponentReferenceThermoDB]
) -> ReferencesThermoDB:
    """
    Convert a list of ComponentReferenceThermoDB to a single ReferencesThermoDB.

    Parameters
    ----------
    components_reference_thermodb : List[ComponentReferenceThermoDB]
        List of ComponentReferenceThermoDB instances.

    Returns
    -------
    ReferencesThermoDB
        A single ReferencesThermoDB instance containing all references and contents.
    """
    try:
        # SECTION: convert to ReferencesThermoDB
        reference: Dict[str, Dict[str, List[str]]] = {}
        contents: Dict[str, List[str]] = {}
        configs: Dict[str, Dict[str, ComponentConfig]] = {}
        rules: Dict[str, Dict[str, ComponentRule]] = {}
        labels: Dict[str, List[str]] = {}
        ignore_labels: Dict[str, List[str]] = {}
        ignore_props: Dict[str, List[str]] = {}

        # NOTE: iterate over components_reference_thermodb
        for component_ref in components_reference_thermodb:
            # ! component id
            component_id_ = create_component_id(
                component=component_ref.component
            )
            # >> component name-state
            component_name_state = component_id_.name_state
            # >> component formula-state
            component_formula_state = component_id_.formula_state

            # components ids
            component_ids = [
                component_name_state,
                component_formula_state,
            ]

            # ! iterate over component ids
            for component_id in component_ids:
                # check if component_name already exists
                if component_id in reference:
                    continue  # skip if already exists

                # ! required fields
                # merge reference
                reference[component_id] = component_ref.reference_thermodb.reference
                # merge contents
                contents[component_id] = component_ref.reference_thermodb.contents
                # merge configs
                configs[component_id] = component_ref.reference_thermodb.configs
                # merge rules
                rules[component_id] = component_ref.reference_thermodb.rules

                # ! NOTE: merge labels, ignore_labels, ignore_props
                # merge labels
                labels[component_id] = component_ref.reference_thermodb.labels or []
                # merge ignore_labels
                ignore_labels[component_id] = component_ref.reference_thermodb.ignore_labels or [
                ]
                # merge ignore_props
                ignore_props[component_id] = component_ref.reference_thermodb.ignore_props or [
                ]

            # NOTE: reset component ids
            component_ids = []

        # NOTE: return ReferencesThermoDB
        return ReferencesThermoDB(
            reference=reference,
            contents=contents,
            configs=configs,
            rules=rules,
            labels=labels,
            ignore_labels=ignore_labels,
            ignore_props=ignore_props
        )
    except Exception as e:  # pragma: no cover
        logging.error(f"Failed to convert to ReferencesThermoDB: {e}")
        raise e
