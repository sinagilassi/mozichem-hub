# import libs
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
# local
from ..config import ascii_with_cat


def print_ascii_art():
    """
    Print the ASCII art with a cat face.
    """
    # Create Console
    console = Console()

    # Frame it with a Panel
    panel_ascii = Panel(
        Text(ascii_with_cat, style="white"),
        title="MoziChemHub - Custom ASCII",
        border_style="blue",
        expand=False
    )
    console.print(panel_ascii)
