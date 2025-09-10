# import libs
import logging
from typing import (
    Optional,
    Union,
    Dict,
    List,
    Literal
)
from pyThermoDB.references import component_reference_mapper
from pyThermoDB.models import ComponentReferenceThermoDB as ComponentReferenceThermoDB_ptdb
from pyThermoDB.models import Component as ptdbComponent
from pyThermoDB.models import ComponentConfig, ComponentRule
# locals
from .reference_services import ReferenceServices
from .reference_controller import ReferenceController
from ..models import (
    References,
    ReferenceThermoDB,
    ComponentsReferenceThermoDB,
    ComponentReferenceThermoDB,
)
from .referencethermodb_controller import ReferenceThermoDBController
from ..models.resources_models import Component

# NOTE: logger
logger = logging.getLogger(__name__)


class ReferenceMapper(ReferenceServices):
    """
    Mapper for transforming and managing references in the MoziChem MCP.
    """
    # NOTE: attributes

    def __init__(
            self
    ):
        """
        Initialize the ReferenceMapper.
        """
        # LINK: initialize the transformer
        ReferenceServices.__init__(self)

    def _reference_input_settings(
        self,
        reference_content: Optional[
            Union[str, List[str]]
        ] = None,
        reference_config: Optional[
            Union[
                str,
                Dict[str, Dict[str, ComponentConfig]]
            ]
        ] = None
    ) -> References:
        """
        Set the reference content and configuration for the MCP.

        Parameters
        ----------
        reference_content : Optional[Union[str, List[str]]]
            Reference content for the MCP.
        reference_config : Optional[Union[str, Dict[str, Dict[str, str]], Dict[str, Dict[str, ComponentConfig]]]]
            Reference configuration for the MCP.

        Returns
        -------
        References
            The references object containing the content, config, and link.
        """
        try:
            # SECTION: standardize the reference content and config
            # NOTE: init the ReferencesAdapter
            ReferenceController_ = ReferenceController(
                reference_content=reference_content,
                reference_config=reference_config
            )

            # NOTE: config conversion
            # ! convert the reference content
            # ! convert the reference config
            # ! build the reference link
            (
                reference_content_,
                reference_config_,
                reference_link_
            ) = ReferenceController_.transformer()

            # NOTE: set reference
            references = References(
                contents=reference_content_,
                config=reference_config_,
                link=reference_link_
            )

            # return
            return references
        except Exception as e:
            logging.error(
                f"Failed to transform reference content and config: {e}"
            )
            raise RuntimeError(
                "Failed to transform reference content and config."
            ) from e

    def _reference_thermodb_generator(
        self,
        references: References
    ) -> ReferenceThermoDB:
        """
        Generate the reference thermodb for the MCP methods.

        Parameters
        ----------
        references : References
            The references object containing the content, config, and link.

        Returns
        -------
        ReferenceThermoDB
            The reference thermodb for the MCP.

        """
        try:
            # NOTE: get the reference thermodb
            return self._generate_references(
                references=references
            )
        except Exception as e:
            logging.error(f"Failed to get reference thermodb: {e}")
            raise RuntimeError("Failed to get reference thermodb.") from e

    def generate_reference_thermodb(
        self,
        reference_content: Optional[
            Union[str, List[str]]
        ] = None,
        reference_config: Optional[
            Union[
                str,
                Dict[str, Dict[str, ComponentConfig]]
            ]
        ] = None
    ) -> ReferenceThermoDB:
        """
        Generate the reference thermodb for the MCP.

        Parameters
        ----------
        reference_content : Optional[Union[str, List[str]]]
            Reference content for the MCP.
        reference_config : Optional[Union[str, Dict[str, Dict[str, ComponentConfig]]]]
            Reference configuration for the MCP.

        Returns
        -------
        ReferenceThermoDB
            The reference thermodb for the MCP.

        Notes
        -----
        - This method combines the reference content and configuration to generate
        the reference thermodynamic database (thermodb) for the MCP methods.
        - This method is only used before the MCP server starts.
        """
        try:
            # SECTION: check the reference content and config
            # NOTE: standardize the reference content and config
            _references: References = self._reference_input_settings(
                reference_content=reference_content,
                reference_config=reference_config
            )

            # NOTE: set the reference thermodb
            return self._reference_thermodb_generator(
                references=_references
            )
        except Exception as e:
            logging.error(f"Failed to generate reference thermodb: {e}")
            raise RuntimeError("Failed to generate reference thermodb.") from e

    def components_reference_thermodb_generator_from_reference_content(
        self,
        components: List[Component],
        reference_content: str,
        component_key: Literal['Name-State', 'Formula-State'] = 'Name-State',
        **kwargs
    ) -> ComponentsReferenceThermoDB:
        """
        Generate the reference thermodb from the reference content.

        Parameters
        ----------
        components : List[Component]
            List of components for which the reference thermodb is generated.
        reference_content : str
            The reference content to be used for generating the reference thermodb.
        **kwargs
            Additional keyword arguments.
            - ignore_state_props: Optional[List[str]] = None
                List of properties to ignore state for, if any.

        Returns
        -------
        ComponentsReferenceThermoDB
            The reference thermodb generated from the reference content.

        Notes
        -----
        This method is used to generate the reference thermodynamic database
        (thermodb) from the provided reference content and components.
        It is only used after the MCP server starts and is not used
        before the server starts.
        One of the method arguments is custom reference content,
        which is a string containing the reference data.
        """
        try:
            # NOTE: check if reference content is provided
            if not reference_content:
                raise ValueError(
                    "Reference content is required to generate reference thermodb.")

            # SECTION: init reference thermodb controller
            ReferenceThermoDBController_ = ReferenceThermoDBController(
                reference_content=reference_content
            )

            # NOTE: generate the reference thermodb
            return ReferenceThermoDBController_.\
                generate_components_reference_thermodb(
                    components=components
                )
        except Exception as e:
            logging.error(
                f"Failed to generate reference thermodb from content: {e}")
            raise RuntimeError(
                "Failed to generate reference thermodb from content.") from e

    def component_reference_thermodb_generator_from_reference_mapper(
        self,
        component: Component,
        reference_content: str,
        component_key: Literal['Name-State', 'Formula-State'] = 'Name-State',
        **kwargs
    ) -> ComponentReferenceThermoDB:
        """
        Generate the component thermodb from the reference content.

        Parameters
        ----------
        component : Component
            The component for which the component thermodb is generated.
        reference_content : str
            The reference content to be used for generating the component thermodb.
        **kwargs
            Additional keyword arguments.
            - component_key: Optional[str] = 'Name-State'
                Key to identify the component in the reference content, by default 'Name-State'.
            - ignore_state_props: Optional[List[str]] = None
                List of properties to ignore state for, if any.

        Returns
        -------
        ComponentReferenceThermoDB
            The component thermodb generated from the reference content.

        Notes
        -----
        This method is used to generate the component thermodynamic database
        (thermodb) from the provided reference content and component.
        It is only used after the MCP server starts and is not used
        before the server starts.
        One of the method arguments is custom reference content,
        which is a string containing the reference data.
        """
        try:
            # SECTION: inputs check
            # NOTE: get ignore_state_props from kwargs
            ignore_state_props: Optional[List[str]] = kwargs.get(
                'ignore_state_props', None
            )

            # check
            if ignore_state_props is None or not isinstance(ignore_state_props, list):
                ignore_state_props = []

            # NOTE: check if reference content is provided
            if not reference_content:
                raise ValueError(
                    "Reference content is required to generate component thermodb.")

            # SECTION: convert component to ptdbComponent
            ptdb_component = ptdbComponent(
                name=component.name,
                formula=component.formula,
                state=component.state
            )

            # NOTE: component ids
            component_name_state = f"{component.name}-{component.state}"
            component_formula_state = f"{component.formula}-{component.state}"

            # SECTION: generate the component reference thermodb
            component_reference_thermodb: ComponentReferenceThermoDB_ptdb = \
                component_reference_mapper(
                    component=ptdb_component,
                    reference_content=reference_content,
                    component_key=component_key,
                    ignore_state_props=ignore_state_props
                )

            # NOTE: extract
            reference_: Dict[
                str, List[str]
            ] = component_reference_thermodb.reference_thermodb.reference
            contents_: List[
                str
            ] = component_reference_thermodb.reference_thermodb.contents
            configs_: Dict[
                str, ComponentConfig
            ] = component_reference_thermodb.reference_thermodb.configs
            rules_: Dict[
                str, ComponentRule
            ] = component_reference_thermodb.reference_thermodb.rules
            labels_: Optional[
                List[str]
            ] = component_reference_thermodb.reference_thermodb.labels
            ignore_labels_: Optional[
                List[str]
            ] = component_reference_thermodb.reference_thermodb.ignore_labels
            ignore_props_: Optional[
                List[str]
            ] = component_reference_thermodb.reference_thermodb.ignore_props

            # NOTE: >> build component thermodb
            component_reference_thermodb_ = ComponentReferenceThermoDB(
                component=component,
                reference_thermodb=ReferenceThermoDB(
                    reference=reference_,
                    contents=contents_,
                    configs=configs_,
                    rules=rules_,
                    labels=labels_,
                    ignore_labels=ignore_labels_,
                    ignore_props=ignore_props_
                )
            )

            # NOTE: reference thermodb
            return component_reference_thermodb_

        except Exception as e:
            logging.error(
                f"Failed to generate component thermodb from content: {e}")
            raise RuntimeError(
                "Failed to generate component thermodb from content.") from e
