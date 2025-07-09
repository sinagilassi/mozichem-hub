# constants

ascii_art = """
███╗   ███╗ ██████╗ ███████╗██╗ ██████╗██╗  ██╗███████╗███╗   ███╗██╗  ██╗██╗   ██╗██████╗
████╗ ████║██╔═══██╗╚══███╔╝██║██╔════╝██║  ██║██╔════╝████╗ ████║██║  ██║██║   ██║██╔══██╗
██╔████╔██║██║   ██║  ███╔╝ ██║██║     ███████║█████╗  ██╔████╔██║███████║██║   ██║██████╔╝
██║╚██╔╝██║██║   ██║ ███╔╝  ██║██║     ██╔══██║██╔══╝  ██║╚██╔╝██║██╔══██║██║   ██║██╔══██╗
██║ ╚═╝ ██║╚██████╔╝███████╗██║╚██████╗██║  ██║███████╗██║ ╚═╝ ██║██║  ██║╚██████╔╝██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝
"""

# Add a cat face below the ASCII art
cat = [
    "    /\\_/\\   Hello, I am Mozi. Enjoy your mcp server!",
    "   ( o.o )",
    "    > ^ <"
]


ascii_with_cat = ascii_art + "\n\n" + "\n".join(cat)


def cat_face(desc):
    """Cat face with description on the first line"""
    cat = [
        f"    /\\_/\\   {desc}",
        "   ( o.o )",
        "    > ^ <"
    ]
    return cat


def combine_lines(art_lines, cat_lines):
    combined = art_lines + ["" for _ in range(2)] + cat_lines
    return "\n".join(combined)
