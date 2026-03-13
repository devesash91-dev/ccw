"""
Golden Spiral (الحلزون الذهبي)
================================
Draws the golden spiral constructed from nested golden rectangles.
Each rectangle is divided into a square and a smaller golden rectangle,
and the quarter-circle arc in each square forms the spiral.
"""

from __future__ import annotations
import math


def plot_golden_spiral(
    n_rectangles: int = 10,
    save_path: str | None = None,
    show: bool = True,
) -> None:
    """
    Draw the golden spiral.

    Parameters
    ----------
    n_rectangles : int
        Number of nested rectangles / arc segments to draw.
    save_path : str or None
        If given, save the figure to this path.
    show : bool
        If True, call plt.show().
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    phi = (1 + math.sqrt(5)) / 2

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect("equal")

    # Build the spiral by successive golden rectangles
    x, y = 0.0, 0.0
    width, height = phi, 1.0
    # direction cycle: right, up, left, down
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    arc_starts = [0, 90, 180, 270]  # degrees for each quarter-circle

    colors = plt.cm.viridis([i / n_rectangles for i in range(n_rectangles)])

    for i in range(n_rectangles):
        direction_idx = i % 4
        dx, dy = directions[direction_idx]
        arc_start = arc_starts[direction_idx]

        # Draw the rectangle
        rect = patches.Rectangle(
            (x, y), width, height,
            linewidth=1, edgecolor="black",
            facecolor=colors[i], alpha=0.3,
        )
        ax.add_patch(rect)

        # Determine the square side length and arc centre
        if width > height:
            square_side = height
        else:
            square_side = width

        # Arc centre and radius
        if direction_idx == 0:   # right → square on the left
            arc_cx, arc_cy = x + square_side, y
            radius = square_side
            next_x = x + square_side
            next_y = y + square_side
            next_w = width - square_side
            next_h = height
        elif direction_idx == 1:  # up → square on the bottom
            arc_cx, arc_cy = x + width, y + square_side
            radius = square_side
            next_x = x
            next_y = y + square_side
            next_w = width
            next_h = height - square_side
        elif direction_idx == 2:  # left → square on the right
            arc_cx, arc_cy = x + width - square_side, y + height
            radius = square_side
            next_x = x
            next_y = y
            next_w = width - square_side
            next_h = height
        else:                     # down → square on the top
            arc_cx, arc_cy = x, y + height - square_side
            radius = square_side
            next_x = x
            next_y = y
            next_w = width
            next_h = height - square_side

        arc = patches.Arc(
            (arc_cx, arc_cy), 2 * radius, 2 * radius,
            angle=0, theta1=arc_start, theta2=arc_start + 90,
            color="navy", linewidth=2,
        )
        ax.add_patch(arc)

        x, y = next_x, next_y
        width, height = next_w, next_h

    ax.autoscale_view()
    ax.set_title(
        f"Golden Spiral  |  الحلزون الذهبي (φ ≈ {phi:.6f})",
        fontsize=14,
    )
    ax.axis("off")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
