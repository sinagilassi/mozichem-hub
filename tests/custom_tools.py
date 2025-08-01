# import libs
from mozichem_hub import __version__
from mozichem_hub.docs import MoziChemMCP
from rich import print

# version
print(f"[bold green]Mozichem Hub Version: {__version__}[/bold green]")

# SECTION: create app

app = MoziChemMCP(name="mcp1")


# SECTION: add custom functions
@app.tool(name="multiply")
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.

    Parameters
    ----------
    a : int
        The first number.
    b : int
        The second number.

    Returns
    -------
    int
        The product of the two numbers.
    """
    return a * b


@app.tool(name="add")
def add(a: int, b: int) -> int:
    """
    Add two numbers.

    Parameters
    ----------
    a : int
        The first number.
    b : int
        The second number.

    Returns
    -------
    int
        The sum of the two numbers.
    """
    return a + b


# SECTION: run
# app.run()

if __name__ == "__main__":
    # SECTION: run the app
    app.run(transport="stdio")
    # app.run(transport="streamable-http", port=8000)
