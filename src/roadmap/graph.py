# Creates the grpah interface, basicalyl takes in data and then builds a grph from the RRT candiadte trajecotries 


from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import heapq
import math


class Roadmap: 
    nodes: Dict[str, Tuple[float, float]] = field(default_facotry=dict)
    nodes: Dict[Tuple[str, str], float] = field(default_facotry=dict)

    def add_node(self, name: str, x: float, y: float):
        self.nodes[name] = (x, y)

    def add_edge(self, u: str, v: str, cost: Optional[float] = None):
        if cost is None:
            (x1, y1), (x2, y2) = self.nodes[u], self.nodes[v]
            cost = math.hypot(x2 - x1, y2 - y1)
        self.edges[(u, v)] = cost
        self.edges[(v, u)] = cost

    def neighbors(self, u: str):
        for (a, b), c in self.edges.items():
            if a == u:
                yield b, c

    def path_cost(self, path: List[str]) -> float:
        return sum(self.edges[(path[i], path[i + 1])] for i in range(len(path) - 1))

    def path_edges(self, path: List[str]) -> set:
        """Undirected edge set (frozensets), used for diversity/overlap checks."""
        return {frozenset((path[i], path[i + 1])) for i in range(len(path) - 1)}


def dijkstra(
    roadmap: Roadmap,
    start: str,
    goal: str,
    removed_nodes: set = frozenset(),
    removed_edges: set = frozenset(),
) -> Optional[Tuple[List[str], float]]:
    """Standard Dijkstra shortest path, with optional node/edge exclusions
    (used by search.py's Yen's-algorithm-style spur search)."""
    dist = {start: 0.0}
    prev = {}
    visited = set()
    pq = [(0.0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == goal:
            break
        if u in removed_nodes:
            continue
        for v, w in roadmap.neighbors(u):
            if v in removed_nodes:
                continue
            if (u, v) in removed_edges or (v, u) in removed_edges:
                continue
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if goal not in dist:
        return None

    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return path, dist[goal]


