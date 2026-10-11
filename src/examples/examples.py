import sys
import os

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


if __name__ == "__main__":
    rm = build_roadmap()
    results = diverse_roadmap_search(rm, "S", "G", k=3, max_overlap=0.4)

    print(f"Found {len(results)} diverse path(s):\n")
    for i, (path, cost) in enumerate(results, 1):
        print(f"  Path {i} (cost={cost:.2f}): {' -> '.join(path)}")
