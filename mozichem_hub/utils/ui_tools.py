# import libs
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
# local
from ..config import (
    cat_face,
    combine_lines,
    ascii_art
)


def print_ascii_art(
    info: Optional[List[str]] = None,
    use_panel: bool = False
):
    """
    Print the ASCII art with a cat face.
    """
    # Create Console
    console = Console()

    cat_lines = cat_face("Hello, I am Mozi. Enjoy your mcp server!")

    # Combine ASCII art and cat face
    if not info:
        ascii_lines = combine_lines([ascii_art], cat_lines)
    else:
        # Combine ASCII art with additional info
        ascii_lines = combine_lines([ascii_art], cat_lines + info)

    # Frame it with a Panel
    if use_panel:
        panel_ascii = Panel(
            Text(ascii_lines, style="blue"),
            title="MoziChemHub MCP Server",
            border_style="white",
            expand=False
        )
        console.print(panel_ascii)
    else:
        # Print without panel
        console.print(Text(ascii_lines, style="blue"))
