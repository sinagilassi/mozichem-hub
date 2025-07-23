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
    """
    Combine ASCII art lines with cat lines, ensuring proper alignment.

    This function makes sure that the text aligns properly with the ASCII art borders
    by calculating appropriate padding.
    """
    # Find the minimum left padding in art_lines (excluding empty lines)
    left_padding = min((len(line) - len(line.lstrip()))
                       for line in art_lines if line.strip())
    left_pad_str = " " * left_padding

    # Find the maximum line length in the ASCII art to determine box width
    max_width = max(len(line) for line in art_lines if line.strip())

    # Ensure cat lines don't exceed the box width (adjust for border if needed)
    padded_cat_lines = []
    for line in cat_lines:
        display_line = left_pad_str + line  # add left padding
        if len(display_line) > max_width:
            display_line = display_line[:max_width]
        padded_cat_lines.append(display_line)

    combined = art_lines + [""] * 2 + padded_cat_lines
    return "\n".join(combined)
