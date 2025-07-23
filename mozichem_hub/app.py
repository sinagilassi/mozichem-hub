# import libs
from fastapi import FastAPI
from typing import (
    Union,
    List,
)
# local
from .api import MoziChemHubAPI
from .docs import MoziChemMCP
from .errors import (
    APICreationError,
    InvalidMCPTypeError,
    InvalidMCPListItemError,
    MCPAdditionError,
    API_CREATION_ERROR_MSG,
    INVALID_MCP_TYPE_ERROR_MSG,
    INVALID_MCP_LIST_ITEM_ERROR_MSG,
    MCP_ADDITION_ERROR_MSG
)


def create_api(
    mcps: Union[MoziChemMCP, List[MoziChemMCP]],
    **kwargs
) -> FastAPI:
    """
    Create a FastAPI instance with optional MCPs.

    Parameters
    ----------
    mcps : MoziChemMCP | List[MoziChemMCP]
        A list of MoziChemMCP instances to be added to the API.
    **kwargs : dict
        Additional keyword arguments for configuration.

    Returns
    -------
    mcp_api : FastAPI
        The FastAPI instance configured with the provided MCPs.

    Notes
    -----
    - If `mcps` is provided, they will be added to the API.
    - The url for each MCP will be `<mcp_name>/mcp/`, where `<mcp_name>` is the name of the MCP.
    For example, if an MCP is named "example-mcp", it will be accessible at `example-mcp/mcp/`.

    Raises
    ------
    InvalidMCPTypeError
        If mcps is neither a MoziChemMCP instance nor a list of MoziChemMCP instances.
    InvalidMCPListItemError
        If any item in the mcps list is not a MoziChemMCP instance.
    MCPAdditionError
        If there's an error adding MCPs to the API.
    APICreationError
        If there's an error creating the API.
    """
    try:
        # SECTION: mcps setup
        if isinstance(mcps, MoziChemMCP):
            mcps = [mcps]
        elif not isinstance(mcps, list):
            raise InvalidMCPTypeError(INVALID_MCP_TYPE_ERROR_MSG)
        else:
            for mcp in mcps:
                if not isinstance(mcp, MoziChemMCP):
                    raise InvalidMCPListItemError(
                        INVALID_MCP_LIST_ITEM_ERROR_MSG)

        # SECTION: create the API
        api = MoziChemHubAPI(**kwargs)

        # NOTE: add MCPs to the API
        if mcps:
            try:
                api.add_mozichem_mcps(mcps)
            except Exception as e:
                raise MCPAdditionError(MCP_ADDITION_ERROR_MSG) from e

        # NOTE: create the FastAPI instance
        mcp_api = api.create_api()

        return mcp_api
    except (
        InvalidMCPTypeError,
        InvalidMCPListItemError,
        MCPAdditionError
    ) as e:
        # Re-raise specific exceptions without modifying the traceback
        raise
    except Exception as e:
        raise APICreationError(API_CREATION_ERROR_MSG) from e
