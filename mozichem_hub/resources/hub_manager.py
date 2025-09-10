# import libs
import logging
from typing import (
    Dict,
    List,
)
from pyThermoDB.models import ComponentConfig, ComponentRule, CustomReference
# locals
from ..models import (
    ReferencesThermoDB,
)
from ..errors import (
    HubComponentReferenceConfigError,
    HubComponentReferenceRuleError,
    HUB_COMPONENT_REFERENCE_CONFIG_ERROR_MSG,
    HUB_COMPONENT_REFERENCE_RULE_ERROR_MSG,
)

# NOTE: logger
logger = logging.getLogger(__name__)

# NOTE: type


class HubManager():
    """
    Manager class for Hub operations.
    """

    def __init__(
            self,
            references_thermodb: ReferencesThermoDB
    ) -> None:
        # SECTION: set
        self.references_thermodb = references_thermodb

        # LINK: set the references
        self.reference: Dict[
            str,
            Dict[str, List[str]]
        ] = references_thermodb.reference
        # LINK: content of the reference thermodynamic database
        # ! [not used]
        self.reference_contents: Dict[
            str, List[str]
        ] = references_thermodb.contents
        # LINK: configuration for the thermodynamic database
        # ! [consists ALL and component-specific configurations]
        self.reference_configs: Dict[
            str, Dict[str, ComponentConfig]
        ] = references_thermodb.configs
        # LINK: rule for the thermodynamic database
        # ! [consists ALL and component-specific configurations]
        self.thermodb_rules: Dict[
            str, Dict[str, ComponentRule]
        ] = references_thermodb.rules
        # LINK: labels to use in the reference config
        self.labels: Dict[
            str, List[str]
        ] = references_thermodb.labels or {}
        # LINK: labels to ignore in the reference config
        self.ignore_labels: Dict[str, List[str]] = \
            references_thermodb.ignore_labels or {}
        # LINK: properties to ignore in the reference config
        self.ignore_props: Dict[str, List[str]] = \
            references_thermodb.ignore_props or {}

    def _set_component_reference(
        self,
        component_id: str
    ) -> CustomReference:
        """
        Set the reference for a specific component.

        Parameters
        ----------
        component_id : str
            The ID of the component for which to set the reference.

        Returns
        -------
        CustomReference
            The reference for the specified component.
        """
        logger.debug(f"Setting reference for component: {component_id}")

        try:
            # SECTION: get the reference for the component
            component_reference = self.reference.get(
                component_id,
                None
            )

            # NOTE: if not found, get ALL
            if component_reference is None:
                logger.debug(
                    f"Component '{component_id}' reference not found, "
                    "using ALL reference"
                )
                component_reference = self.reference.get(
                    'ALL',
                    None
                )

                # check if ALL is also not found
                if component_reference is None:
                    error_msg = (
                        f"Component '{component_id}' not found in "
                        "the reference."
                    )
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            # SECTION: return the reference
            logger.debug(
                f"Reference set successfully for component: {component_id}"
            )
            return component_reference

        except Exception as e:
            logger.error(
                f"Failed to set component reference for '{component_id}': {e}"
            )
            raise HubComponentReferenceConfigError(
                HUB_COMPONENT_REFERENCE_CONFIG_ERROR_MSG
            ) from e

    def _set_component_reference_config(
        self,
        component_id: str
    ) -> Dict[str, ComponentConfig]:
        """
        Set the reference configuration for a specific component.
        Parameters
        ----------
        component_id : str
            The ID of the component for which to set the reference
            configuration.
        Returns
        -------
        Dict[str, Dict[str, str]]
            The reference configuration for the specified component.
        """
        logger.debug(f"Setting reference config for component: {component_id}")

        try:
            # SECTION: get the reference configuration for the component
            component_reference_config = self.reference_configs.get(
                component_id,
                None
            )

            # NOTE: if not found, get ALL
            if component_reference_config is None:
                logger.debug(
                    f"Component '{component_id}' config not found, "
                    "using ALL config"
                )
                component_reference_config = self.reference_configs.get(
                    'ALL',
                    None
                )

                # check if ALL is also not found
                if component_reference_config is None:
                    error_msg = (
                        f"Component '{component_id}' not found in "
                        "the reference configuration."
                    )
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            # SECTION: return the reference configuration
            logger.debug(
                f"Reference config set successfully for "
                f"component: {component_id}"
            )
            return component_reference_config

        except Exception as e:
            logger.error(
                f"Failed to set component reference config for "
                f"'{component_id}': {e}"
            )
            raise HubComponentReferenceConfigError(
                HUB_COMPONENT_REFERENCE_CONFIG_ERROR_MSG
            ) from e

    def _set_component_reference_rule(
        self,
        component_id: str
    ) -> Dict[str, ComponentRule]:
        """
        Set the reference rule for a specific component.

        Parameters
        ----------
        component_id : str
            The ID of the component for which to set the reference rule.

        Returns
        -------
        Dict[str, Dict[str, str]]
            The reference rule for the specified component, or None if not
            found.
        """
        logger.debug(f"Setting reference rule for component: {component_id}")

        try:
            # SECTION: get the reference rule for the component
            component_reference_rule = self.thermodb_rules.get(
                component_id,
                None
            )

            # NOTE: if not found, get ALL
            if component_reference_rule is None:
                logger.debug(
                    f"Component '{component_id}' rule not found, "
                    "using ALL rule"
                )
                component_reference_rule = self.thermodb_rules.get(
                    'ALL',
                    None
                )

                # check if ALL is also not found
                if component_reference_rule is None:
                    error_msg = (
                        f"Component '{component_id}' not found in "
                        "the reference rule."
                    )
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            logger.debug(
                f"Reference rule set successfully for "
                f"component: {component_id}"
            )
            return component_reference_rule

        except Exception as e:
            logger.error(
                f"Failed to set component reference rule for "
                f"'{component_id}': {e}"
            )
            raise HubComponentReferenceRuleError(
                HUB_COMPONENT_REFERENCE_RULE_ERROR_MSG
            ) from e

    def _set_component_ignore_labels(
        self,
        component_id: str
    ) -> List[str]:
        """
        Set the ignore labels for a specific component.

        Parameters
        ----------
        component_id : str
            The ID of the component for which to set the ignore labels.

        Returns
        -------
        List[str]
            The ignore labels for the specified component.
        """
        logger.debug(f"Setting ignore labels for component: {component_id}")

        try:
            # SECTION: get the ignore labels for the component
            component_ignore_labels = self.ignore_labels.get(
                component_id,
                None
            )

            # NOTE: if not found, get ALL
            if component_ignore_labels is None:
                logger.debug(
                    f"Component '{component_id}' ignore labels not found, "
                    "using ALL ignore labels"
                )
                component_ignore_labels = self.ignore_labels.get(
                    'ALL',
                    []
                )

            # SECTION: if still None, set to empty list
            if component_ignore_labels is None:
                component_ignore_labels = []

            logger.debug(
                f"Ignore labels set successfully for "
                f"component: {component_id}"
            )

            # return
            return component_ignore_labels

        except Exception as e:
            logger.error(
                f"Failed to set component ignore labels for "
                f"'{component_id}': {e}"
            )
            raise HubComponentReferenceConfigError(
                HUB_COMPONENT_REFERENCE_CONFIG_ERROR_MSG
            ) from e
