import sys
import os

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from roadmap.graph import Roadmap
from roadmap.search import diverse_roadmap_search


def build_roadmap() -> Roadmap:
    rm = Roadmap()
    coords = {
        "S":  (0, 0),
        "A1": (2, 4), "A2": (4, 4), "A3": (6, 4),      # north corridor
        "B1": (2, 0), "B2": (4, 0), "B3": (6, 0),      # middle corridor
        "C1": (2, -4), "C2": (4, -4), "C3": (6, -4),   # south corridor
        "X1": (4, 2), "X2": (4, -2),                   # cross-links
        "G":  (8, 0),
    }
    for name, (x, y) in coords.items():
        rm.add_node(name, x, y)

    edges = [
        ("S", "A1"), ("A1", "A2"), ("A2", "A3"), ("A3", "G"),
        ("S", "B1"), ("B1", "B2"), ("B2", "B3"), ("B3", "G"),
        ("S", "C1"), ("C1", "C2"), ("C2", "C3"), ("C3", "G"),
        ("A2", "X1"), ("X1", "B2"),
        ("B2", "X2"), ("X2", "C2"),
    ]
    for u, v in edges:
        rm.add_edge(u, v)

    return rm


def plot_results(rm: Roadmap, results, start: str, goal: str) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))

    # All roadmap edges (each undirected edge drawn once), in light gray
    drawn = set()
    for (u, v) in rm.edges:
        key = frozenset((u, v))
        if key in drawn:
            continue
        drawn.add(key)
        (x1, y1), (x2, y2) = rm.nodes[u], rm.nodes[v]
        ax.plot([x1, x2], [y1, y2], color="lightgray", linewidth=1.5, zorder=1)

    # Each diverse path in its own color
    colors = ["tab:green", "tab:purple", "tab:orange", "tab:red", "tab:blue"]
    for i, (path, cost) in enumerate(results):
        xs = [rm.nodes[n][0] for n in path]
        ys = [rm.nodes[n][1] for n in path]
        ax.plot(xs, ys, color=colors[i % len(colors)], linewidth=3.5, alpha=0.8,
                label=f"Path {i + 1} (cost {cost:.2f})", zorder=2)

    # Nodes and labels
    for name, (x, y) in rm.nodes.items():
        is_endpoint = name in (start, goal)
        ax.scatter(x, y, s=180 if is_endpoint else 90,
                   color="black" if is_endpoint else "white",
                   edgecolors="black", zorder=3)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=9)

    ax.set_title("Diverse roadmap search")
    ax.set_aspect("equal")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    rm = build_roadmap()
    results = diverse_roadmap_search(rm, "S", "G", k=3, max_overlap=0.4)

    print(f"Found {len(results)} diverse path(s):\n")
    for i, (path, cost) in enumerate(results, 1):
        print(f"  Path {i} (cost={cost:.2f}): {' -> '.join(path)}")

    plot_results(rm, results, "S", "G")
